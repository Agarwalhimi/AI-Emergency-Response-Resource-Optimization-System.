import os
from pathlib import Path
import sys
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for, session

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from database.db import (
    add_emergency, all_emergencies, init_db, recent, stats, init_auth_db,
    authenticate_user, create_user, reset_emergencies, update_emergency_status
)
from dsa.graph import all_locations, shortest_path
from dsa.priority_queue import EmergencyPriorityQueue
from dsa.resource_manager import ResourceManager
from ml.predict import model_accuracy, predict_priority

app = Flask(__name__, template_folder=str(ROOT / "templates"), static_folder=str(ROOT / "frontend" / "static"))
app.secret_key = os.environ.get("SECRET_KEY", "emergency-ai-college-demo-secret-2026")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,
    PERMANENT_SESSION_LIFETIME=86400,
)

init_db()
init_auth_db()
resource_manager = ResourceManager()
queue = EmergencyPriorityQueue()


@app.context_processor
def inject_user():
    return {"current_user": session.get("user")}


PUBLIC_ENDPOINTS = {"login", "register", "static"}


@app.before_request
def allow_academic_demo_access():
    # Option B: this is a no-login academic demo. The landing page is public,
    # and every module can be opened directly from its navigation links.
    return None


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter both email and password.", "error")
            return render_template("login.html", email=email), 400

        user = authenticate_user(email, password)

        if user is None:
            flash("Incorrect email or password. Please try again.", "error")
            return render_template("login.html", email=email), 401

        # Store only JSON-serializable user data in the Flask session.
        session.clear()
        session["user"] = {
            "id": int(user["id"]),
            "name": str(user["full_name"]),
            "email": str(user["email"]),
        }
        session.permanent = True

        # Always send a successful login to the dashboard.
        next_url = request.args.get("next", "")
        if next_url and next_url.startswith("/") and not next_url.startswith("//"):
            return redirect(next_url)
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user" in session:
        return redirect(url_for("dashboard"))

    full_name = ""
    email = ""

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if len(full_name) < 2:
            flash("Please enter your full name.", "error")
        elif "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            flash("Please enter a valid email address.", "error")
        elif len(password) < 6:
            flash("Password must contain at least 6 characters.", "error")
        elif password != confirm:
            flash("Passwords do not match.", "error")
        else:
            user_id = create_user(full_name, email, password)
            if user_id is None:
                flash("An account with this email already exists. Try signing in instead.", "error")
            else:
                # Auto-login after successful registration so the user goes straight to Dashboard.
                user = authenticate_user(email, password)
                if user is None:
                    flash("Account was created, but automatic sign-in failed. Please sign in manually.", "error")
                    return redirect(url_for("login"))

                session.clear()
                session["user"] = {
                    "id": int(user["id"]),
                    "name": str(user["full_name"]),
                    "email": str(user["email"]),
                }
                session.permanent = True
                flash(f"Welcome, {user['full_name']}! Account created successfully.", "success")
                return redirect(url_for("dashboard"))

    return render_template("register.html", full_name=full_name, email=email)


@app.post("/logout")
def logout():
    # Kept as a compatibility route for older bookmarks/templates.
    session.clear()
    return redirect(url_for("landing"))

def queue_existing():
    for row in all_emergencies():
        queue.push(f"E-{row['id']:03d}", row["priority"], row["location"])

queue_existing()

@app.context_processor
def inject_globals():
    return {"locations": all_locations()}

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", stats=stats(), recent=recent(), model_accuracy=model_accuracy(), queue_size=len(queue))

@app.route("/emergency")
def emergency():
    return render_template("emergency.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        form = {
            "Type": request.form["Type"],
            "Location": request.form["Location"],
            "Injury": request.form["Injury"],
            "Fire": request.form["Fire"],
            "MedicalCondition": request.form["MedicalCondition"],
            "People": int(request.form["People"]),
            "ResponseTime": int(request.form.get("ResponseTime", 15)),
        }
        if form["People"] < 1 or form["People"] > 1000:
            raise ValueError("People affected must be between 1 and 1000.")
        priority = predict_priority(form)
        resource = resource_manager.assign(form["Type"], priority, form["Location"])
        route, distance = ([], None)
        if resource:
            route, distance = shortest_path(resource["location"], form["Location"])
        record = dict(form)
        record.update({
            "Priority": priority,
            "resource_id": resource["resource_id"] if resource else None,
            "resource_name": resource["name"] if resource else None,
            "route": " → ".join(route) if route else "No route available",
            "distance": distance,
            "status": "Dispatched" if resource else "Waiting for Resource",
        })
        emergency_id = add_emergency(record)
        queue_item_id = f"E-{emergency_id:03d}"
        queue.push(queue_item_id, priority, form["Location"])
        # The queue is used for priority ordering. Once a resource is dispatched,
        # the current case is considered processed and removed from the active queue.
        if resource:
            queue.pop()
        return render_template("result.html", record=record, emergency_id=queue_item_id, resource=resource, route=route, distance=distance)
    except (KeyError, ValueError) as exc:
        flash(str(exc), "error")
        return redirect(url_for("emergency"))
    except Exception:
        app.logger.exception("Emergency analysis failed")
        flash("The emergency could not be analyzed. Check that the ML dependencies/model are available and try again.", "error")
        return redirect(url_for("emergency"))

@app.route("/resources")
def resources():
    return render_template("resources.html", resources=resource_manager.resources)

@app.post("/resources/<resource_id>/release")
def release_resource(resource_id):
    released = resource_manager.release(resource_id)
    resource_manager.save()
    if released:
        update_emergency_status(resource_id, "Completed")
        flash(f"{released['name']} is available again and the linked response was marked completed.", "success")
    return redirect(url_for("resources"))

@app.route("/routes")
def routes():
    locations = all_locations()
    return render_template(
        "routes.html", locations=locations, route=[], distance=None,
        selected_start=locations[0] if locations else "",
        selected_destination=locations[1] if len(locations) > 1 else (locations[0] if locations else ""),
    )

@app.post("/find-route")
def find_route():
    locations = all_locations()
    start = request.form.get("start", "")
    destination = request.form.get("destination", "")
    if start not in locations or destination not in locations:
        flash("Please choose valid start and destination locations.", "error")
        return render_template("routes.html", locations=locations, route=[], distance=None,
                               selected_start=start, selected_destination=destination), 400
    if start == destination:
        flash("Start and destination must be different locations.", "error")
        return render_template("routes.html", locations=locations, route=[], distance=None,
                               selected_start=start, selected_destination=destination), 400
    route, distance = shortest_path(start, destination)
    return render_template("routes.html", locations=locations, route=route, distance=distance,
                           selected_start=start, selected_destination=destination)

@app.route("/history")
def history():
    return render_template("history.html", emergencies=all_emergencies())

@app.route("/settings")
def settings():
    return render_template(
        "settings.html",
        model_accuracy=model_accuracy(),
        resource_count=len(resource_manager.resources),
        available_count=len(resource_manager.available()),
        emergency_count=stats()["total"],
    )

@app.post("/settings/reset")
def reset_demo_data():
    reset_emergencies()
    resource_manager.reset()
    queue.clear()
    flash("Demo data has been reset. All resources are available and emergency history is empty.", "success")
    return redirect(url_for("dashboard"))

@app.get("/api/queue")
def api_queue():
    items = [{"id": item.emergency_id, "priority": item.priority, "location": item.location} for item in queue.items()]
    return jsonify(items)

@app.get("/api/stats")
def api_stats():
    data = stats()
    data["available_resources"] = len(resource_manager.available())
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

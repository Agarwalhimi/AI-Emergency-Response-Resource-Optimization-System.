from pathlib import Path
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DB_FILE = Path(__file__).resolve().parent / "app.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS emergencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emergency_type TEXT NOT NULL,
            location TEXT NOT NULL,
            injury TEXT NOT NULL,
            fire TEXT NOT NULL,
            medical_condition TEXT NOT NULL,
            people INTEGER NOT NULL,
            response_time INTEGER NOT NULL,
            priority TEXT NOT NULL,
            resource_id TEXT,
            resource_name TEXT,
            route TEXT,
            distance REAL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_emergency(record):
    conn = get_connection()
    cur = conn.execute("""
        INSERT INTO emergencies
        (emergency_type, location, injury, fire, medical_condition, people,
         response_time, priority, resource_id, resource_name, route, distance,
         status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["Type"], record["Location"], record["Injury"], record["Fire"],
        record["MedicalCondition"], record["People"], record["ResponseTime"],
        record["Priority"], record.get("resource_id"), record.get("resource_name"),
        record.get("route"), record.get("distance"), record.get("status", "Dispatched"),
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def recent(limit=8):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM emergencies ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def all_emergencies():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM emergencies ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def stats():
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM emergencies").fetchone()[0]
    active = conn.execute("SELECT COUNT(*) FROM emergencies WHERE status = 'Dispatched'").fetchone()[0]
    critical = conn.execute("SELECT COUNT(*) FROM emergencies WHERE priority = 'Critical'").fetchone()[0]
    conn.close()
    return {"total": total, "active": active, "critical": critical}


def init_auth_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    # Demo account for college presentation/testing.
    demo = conn.execute("SELECT id FROM users WHERE email = ?", ("admin@emergency.ai",)).fetchone()
    if not demo:
        conn.execute(
            "INSERT INTO users (full_name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            ("Admin User", "admin@emergency.ai", generate_password_hash("admin123"), datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
    conn.commit()
    conn.close()


def create_user(full_name, email, password):
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO users (full_name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (full_name.strip(), email.strip().lower(), generate_password_hash(password), datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def authenticate_user(email, password):
    conn = get_connection()
    row = conn.execute(
        "SELECT id, full_name, email, password_hash FROM users WHERE email = ?",
        (email.strip().lower(),)
    ).fetchone()
    conn.close()
    if row and check_password_hash(row["password_hash"], password):
        return dict(row)
    return None


def update_emergency_status(resource_id, status):
    conn = get_connection()
    conn.execute("UPDATE emergencies SET status = ? WHERE resource_id = ? AND status = 'Dispatched'", (status, resource_id))
    conn.commit()
    conn.close()


def reset_emergencies():
    conn = get_connection()
    conn.execute("DELETE FROM emergencies")
    conn.commit()
    conn.close()

# AI Emergency Response & Resource Optimization

A complete college-level academic prototype that combines **Machine Learning + Data Structures + Dijkstra's Algorithm + Flask** for emergency decision support.

## Core workflow

Emergency Input → ML Priority Prediction → Priority Queue → Resource Assignment → Dijkstra Shortest Route → Response Result → History

## What the project demonstrates

- User registration and session-based login
- Professional responsive dashboard
- Emergency reporting form
- ML classification into Low / Medium / High / Critical
- Heap-based priority queue for emergency ordering
- Resource assignment for ambulance, fire engine and rescue team
- Graph representation of a simulated road network
- Dijkstra shortest-path routing
- SQLite storage of emergency history and users
- Resource release after dispatch
- Route planner page
- History and system settings pages
- Automated tests for the core algorithms and authentication flow

## Technology

- Python 3.10+
- Flask
- Scikit-learn + Pandas + Joblib
- HTML, CSS, JavaScript
- SQLite
- Priority Queue (heap)
- Graph + Dijkstra

## Important academic scope

This is an **academic simulation/prototype**, not a real emergency dispatch system. Emergency records, resource positions and road distances are simulated/predefined for demonstrating the algorithms safely.

## Run on Windows

1. Extract the ZIP.
2. Open Command Prompt/PowerShell in the project folder.
3. Run:

```text
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

4. Open `http://127.0.0.1:5000`

The application creates the SQLite database automatically and creates the demo account on first start.

### Demo login

- Email: `admin@emergency.ai`
- Password: `admin123`

You can also create a new account from the registration page.

## Demo flow for presentation

1. Login with the demo account.
2. Open **Report Emergency**.
3. Select Fire/Medical/Accident and enter the emergency details.
4. Click **Analyze & Generate Response**.
5. The system predicts a priority using the ML model.
6. The priority is inserted into the priority queue.
7. An available matching resource is selected.
8. Dijkstra calculates the shortest route from the resource location to the emergency location.
9. The result page shows priority, assigned resource, route, distance and status.
10. Open **History** to show the stored record.
11. Open **Resources** to show the assigned unit as Busy and release it afterward.
12. Open **Route Optimization** to demonstrate Dijkstra independently.

## Project structure

```text
AI-Emergency-Optimization/
├── app.py
├── run.bat
├── requirements.txt
├── README.md
├── backend/
│   └── app.py
├── database/
│   └── db.py
├── ml/
│   ├── train_model.py
│   ├── predict.py
│   └── emergency_model.joblib
├── dsa/
│   ├── priority_queue.py
│   ├── resource_manager.py
│   └── graph.py
├── data/
│   ├── emergencies.csv
│   └── resources.csv
├── templates/
├── frontend/static/
├── docs/
└── tests/
```

## Troubleshooting

- If a browser shows an old page, stop the previous Flask process and run the project again.
- If the saved ML model is incompatible with the installed scikit-learn version, the application automatically retrains it from `data/emergencies.csv`.
- If you want a clean demo database, delete `database/app.db` while the application is stopped and restart it.

## Academic disclaimer

The system is intended only to demonstrate the integration of ML classification, DSA-based resource management and graph-based route optimization in a college project. It should not be used for real emergency response.

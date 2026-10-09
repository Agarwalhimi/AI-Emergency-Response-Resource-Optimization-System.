# College Demo Guide

## 1. Start

```bash
pip install -r requirements.txt
python backend/app.py
```

Open `http://127.0.0.1:5000`.

## 2. Best emergency demo

Use these values:

- Emergency Type: Fire
- Location: Raipur
- Injury Level: Severe
- People Affected: 8
- Fire Involved: Yes
- Medical Condition: Stable
- Response Time: 5 minutes

Expected behavior: a high-priority result (typically Critical for this sample dataset), a fire engine is selected, and Dijkstra shows the shortest route from the resource base to the emergency location.

## 3. Show the modules

1. Dashboard — project overview and system modules.
2. Report Emergency — input form and ML workflow.
3. Analysis Result — priority + resource + route.
4. Resources — resource pool and release action.
5. Route Optimization — manually demonstrate Dijkstra.
6. History — SQLite records.
7. Settings — model and prototype limitations.

## 4. Explain in viva

### ML
The model is a Random Forest classifier trained on the included sample emergency dataset. Categorical fields are one-hot encoded and numerical fields are passed as numeric features.

### DSA
The emergency priority queue uses a heap. Critical emergencies receive the highest queue priority, followed by High, Medium, and Low.

### Resource optimization
The Resource Manager first prefers the resource type associated with the emergency and then compares simulated graph distances to choose the nearest available unit.

### Dijkstra
The graph contains simulated locations and weighted roads. Dijkstra's algorithm finds the minimum total distance between the resource location and emergency location.

### Database
SQLite stores each analyzed emergency, predicted priority, assigned resource, route, distance, status, and timestamp.

## 5. Scope statement

This is an academic decision-support prototype. It does not dispatch real emergency services, use real GPS, access live traffic, or connect to government/emergency APIs.

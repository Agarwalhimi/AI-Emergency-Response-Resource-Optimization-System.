import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.app import app
from dsa.graph import shortest_path
from dsa.priority_queue import EmergencyPriorityQueue
from ml.predict import predict_priority


def test_priority_queue_order():
    pq = EmergencyPriorityQueue()
    pq.push("E1", "Low")
    pq.push("E2", "Critical")
    pq.push("E3", "High")
    assert pq.pop().emergency_id == "E2"
    assert pq.pop().emergency_id == "E3"
    assert pq.pop().emergency_id == "E1"


def test_dijkstra():
    path, distance = shortest_path("Central Hospital", "Raipur")
    assert path[0] == "Central Hospital"
    assert path[-1] == "Raipur"
    assert distance == 6.0


def test_ml_prediction_returns_valid_class():
    data = {"Type":"Fire","People":8,"Injury":"Severe","Fire":"Yes","MedicalCondition":"Stable","ResponseTime":5}
    assert predict_priority(data) in {"Low", "Medium", "High", "Critical"}


def test_landing_and_modules_open_without_login():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Make every response" in response.data
    assert b"Get Started" in response.data

    for path in ["/dashboard", "/emergency", "/resources", "/routes", "/history", "/settings"]:
        assert client.get(path).status_code == 200


def test_emergency_submission_saves_record():
    client = app.test_client()
    response = client.post("/analyze", data={
        "Type": "Fire", "Location": "ISBT", "Injury": "Severe",
        "Fire": "Yes", "MedicalCondition": "Stable", "People": "5", "ResponseTime": "10"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert (b"Emergency" in response.data) or (b"emergency" in response.data.lower())

from dsa.graph import shortest_path
from dsa.priority_queue import EmergencyPriorityQueue
from dsa.resource_manager import ResourceManager
from ml.predict import predict_priority

path, distance = shortest_path("Central Hospital", "Raipur")
assert path == ["Central Hospital", "Clock Tower", "Raipur"]
assert distance == 6.0

queue = EmergencyPriorityQueue()
queue.push("E1", "Low")
queue.push("E2", "Critical")
queue.push("E3", "High")
assert [queue.pop().emergency_id for _ in range(3)] == ["E2", "E3", "E1"]

prediction = predict_priority({"Type":"Fire","People":8,"Injury":"Severe","Fire":"Yes","MedicalCondition":"Stable","ResponseTime":5})
assert prediction in {"Low", "Medium", "High", "Critical"}

resource = ResourceManager().assign("Fire", prediction, "Raipur")
assert resource and resource["type"] == "FIRE ENGINE"
print("Core smoke test: PASS")

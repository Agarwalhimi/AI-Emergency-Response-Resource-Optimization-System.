from pathlib import Path
import csv
from dsa.graph import shortest_path

BASE_DIR = Path(__file__).resolve().parent.parent
RESOURCE_FILE = BASE_DIR / "data" / "resources.csv"

RESOURCE_BY_EMERGENCY = {
    "Fire": "FIRE ENGINE",
    "Accident": "AMBULANCE",
    "Medical": "AMBULANCE",
    "Flood": "RESCUE TEAM",
    "Rescue": "RESCUE TEAM",
}

class ResourceManager:
    def __init__(self, csv_path=RESOURCE_FILE):
        self.csv_path = Path(csv_path)
        self.resources = []
        self.load()

    def load(self):
        with self.csv_path.open(newline="", encoding="utf-8") as file:
            self.resources = list(csv.DictReader(file))

    def available(self):
        return [r for r in self.resources if r["status"] == "Available"]

    def assign(self, emergency_type: str, priority: str, emergency_location: str):
        preferred = RESOURCE_BY_EMERGENCY.get(emergency_type, "RESCUE TEAM")
        candidates = [r for r in self.resources if r["status"] == "Available" and r["type"] == preferred]
        # Never dispatch the wrong resource type. If the required unit is busy,
        # the case remains waiting instead of receiving an unsuitable vehicle.
        if not candidates:
            return None

        scored = []
        for resource in candidates:
            try:
                _, distance = shortest_path(resource["location"], emergency_location)
            except ValueError:
                distance = 999
            scored.append((distance if distance is not None else 999, resource))
        scored.sort(key=lambda item: item[0])
        selected = scored[0][1]
        selected["status"] = "Busy"
        return selected.copy()

    def release(self, resource_id: str):
        for resource in self.resources:
            if resource["resource_id"] == resource_id:
                resource["status"] = "Available"
                return resource.copy()
        return None

    def reset(self):
        self.load()
        for resource in self.resources:
            resource["status"] = "Available"
        self.save()

    def save(self):
        fields = ["resource_id", "type", "name", "location", "status"]
        with self.csv_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(self.resources)

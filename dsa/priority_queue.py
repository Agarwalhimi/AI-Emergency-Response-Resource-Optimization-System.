import heapq
from dataclasses import dataclass, field
from typing import Any

PRIORITY_VALUE = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}

@dataclass(order=True)
class QueueItem:
    sort_index: int
    sequence: int
    emergency_id: str = field(compare=False)
    priority: str = field(compare=False)
    location: str = field(compare=False, default="")

class EmergencyPriorityQueue:
    """Max-priority queue implemented with Python's heap structure."""
    def __init__(self):
        self._heap = []
        self._sequence = 0

    def push(self, emergency_id: str, priority: str, location: str = ""):
        self._sequence += 1
        value = PRIORITY_VALUE.get(priority, 1)
        heapq.heappush(self._heap, QueueItem(-value, self._sequence, emergency_id, priority, location))

    def pop(self):
        if not self._heap:
            return None
        return heapq.heappop(self._heap)

    def peek(self):
        return self._heap[0] if self._heap else None

    def items(self):
        return sorted(self._heap)

    def clear(self):
        self._heap.clear()
        self._sequence = 0

    def __len__(self):
        return len(self._heap)

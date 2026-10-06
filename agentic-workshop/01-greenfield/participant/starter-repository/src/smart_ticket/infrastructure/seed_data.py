from datetime import datetime
from smart_ticket.domain.models import Trip

def build_seed_trips() -> dict[str, Trip]:
    rows = [("T001", "台北", "台中", 700, 20),
            ("T002", "台北", "高雄", 1500, 8),
            ("T003", "台中", "高雄", 800, 0),
            ("T004", "高雄", "台北", 1500, 12)]
    departure = datetime.fromisoformat("2030-01-15T09:00:00+08:00")
    arrival = datetime.fromisoformat("2030-01-15T12:00:00+08:00")
    return {tid: Trip(tid, origin, destination, departure, arrival, fare, seats)
            for tid, origin, destination, fare, seats in rows}

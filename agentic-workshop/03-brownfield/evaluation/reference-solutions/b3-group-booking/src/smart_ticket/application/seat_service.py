from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.models import Passenger
from smart_ticket.domain.records import SeatAssignment
from smart_ticket.infrastructure.store import InMemoryStore

class SeatService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def plan(self, booking_id: str, trip_id: str, passengers: list[Passenger]) -> list[SeatAssignment]:
        used = {assignment.seat_id for records in self.store.seat_assignments.values()
                for assignment in records if assignment.trip_id == trip_id}
        free = [f"S{i:03d}" for i in range(1, self.store.seat_capacity[trip_id] + 1)
                if f"S{i:03d}" not in used]
        if len(free) < len(passengers):
            raise DomainError("INSUFFICIENT_SEATS", "Insufficient available seats", 409)
        return [self.assignment(booking_id, passenger.passenger_id, trip_id, seat)
                for passenger, seat in zip(passengers, free)]

    def reserve(self, booking_id: str, trip_id: str, assignments: list[SeatAssignment]) -> None:
        self.store.seat_assignments[booking_id] = assignments
        self.store.trips[trip_id].available_seats -= len(assignments)

    def release(self, booking_id: str) -> None:
        assignments = self.store.seat_assignments.pop(booking_id, [])
        if assignments:
            self.store.trips[assignments[0].trip_id].available_seats += len(assignments)

    @staticmethod
    def assignment(booking_id: str, passenger_id: str, trip_id: str, seat_id: str) -> SeatAssignment:
        index = int(seat_id[1:]) - 1
        position = index % 20 + 1
        return SeatAssignment(booking_id, passenger_id, trip_id, seat_id,
                              f"C{index // 20 + 1:03d}", (position - 1) // 4 + 1,
                              (position - 1) % 4 + 1, position)

    def plan_group(self, booking_id: str, trip_id: str, passengers: list[Passenger]) -> list[SeatAssignment]:
        """Find a complete contiguous segment inside one carriage, without mutation."""
        used = {assignment.seat_id for records in self.store.seat_assignments.values()
                for assignment in records if assignment.trip_id == trip_id}
        count = len(passengers)
        capacity = self.store.seat_capacity[trip_id]
        for start in range(1, capacity - count + 2):
            end = start + count - 1
            if (start - 1) // 20 != (end - 1) // 20:
                continue
            seats = [f"S{i:03d}" for i in range(start, end + 1)]
            if not any(seat in used for seat in seats):
                return [self.assignment(booking_id, passenger.passenger_id, trip_id, seat)
                        for passenger, seat in zip(passengers, seats)]
        raise DomainError("CONSECUTIVE_SEATS_UNAVAILABLE", "No complete consecutive seat segment", 409)

from smart_ticket.domain.fare_policy import FarePolicy
from smart_ticket.domain.models import Booking, Passenger
from smart_ticket.infrastructure.store import InMemoryStore

class BookingService:
    def __init__(self, store: InMemoryStore, fare_policy: FarePolicy) -> None:
        self.store = store
        self.fare_policy = fare_policy

    def create(self, trip_id: str, passengers: list[Passenger]) -> Booking:
        # TODO(GREENFIELD, BOOKING-001, BOOKING-002, BOOKING-003): Validate booking inputs.
        # TODO(GREENFIELD, FARE-003, BOOKING-004, BOOKING-005): Calculate total and reserve seats.
        raise NotImplementedError("Booking creation is not implemented in G0")

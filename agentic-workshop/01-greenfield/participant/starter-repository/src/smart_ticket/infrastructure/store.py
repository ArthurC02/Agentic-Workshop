from smart_ticket.domain.models import Booking, Order, Trip
from smart_ticket.infrastructure.seed_data import build_seed_trips

class InMemoryStore:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.trips: dict[str, Trip] = build_seed_trips()
        self.bookings: dict[str, Booking] = {}
        self.orders: dict[str, Order] = {}

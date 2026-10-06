from threading import RLock
from smart_ticket.domain.models import Booking, Order, Trip
from smart_ticket.infrastructure.seed_data import build_seed_trips

class InMemoryStore:
    """Lightweight Trip/Booking/Order repository adapter with shared mutation lock."""
    def __init__(self) -> None:
        self.lock = RLock()
        self.reset()

    def reset(self) -> None:
        with self.lock:
            self.trips: dict[str, Trip] = build_seed_trips()
            self.bookings: dict[str, Booking] = {}
            self.orders: dict[str, Order] = {}

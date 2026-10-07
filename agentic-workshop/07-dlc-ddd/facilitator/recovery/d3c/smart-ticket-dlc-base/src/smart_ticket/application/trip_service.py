from smart_ticket.domain.models import Trip
from smart_ticket.domain.repositories import TicketRepositories

class TripService:
    def __init__(self, store: TicketRepositories) -> None:
        self.store = store

    def query(self, origin: str | None = None, destination: str | None = None) -> list[Trip]:
        # TRIP-001, TRIP-002: sellable trips with exact optional filters.
        return [trip for trip in self.store.trips.values()
                if trip.available_seats > 0
                and (origin is None or trip.origin == origin)
                and (destination is None or trip.destination == destination)]

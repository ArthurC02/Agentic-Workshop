from copy import deepcopy
from uuid import uuid4
from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.fare_policy import FarePolicy
from smart_ticket.domain.models import Booking, BookingStatus, Passenger
from smart_ticket.domain.repositories import TicketRepositories

class BookingService:
    def __init__(self, store: TicketRepositories, fare_policy: FarePolicy) -> None:
        self.store = store
        self.fare_policy = fare_policy

    def create(self, trip_id: str, passengers: list[Passenger]) -> Booking:
        with self.store.lock:
            trip = self.store.trips.get(trip_id)
            if trip is None:
                raise DomainError("TRIP_NOT_FOUND", "Trip not found", 404)
            # BOOKING-001, BOOKING-002, BOOKING-003: validate before mutation.
            if not 1 <= len(passengers) <= 4:
                raise DomainError("INVALID_PASSENGER_COUNT", "Booking requires 1 to 4 passengers", 409)
            if len(passengers) > trip.available_seats:
                raise DomainError("INSUFFICIENT_SEATS", "Insufficient available seats", 409)
            # FARE-003: calculate all passenger fares before committing reservation.
            total = sum(self.fare_policy.calculate(trip.base_fare, passenger.passenger_type)
                        for passenger in passengers)
            booking = Booking(str(uuid4()), trip_id, deepcopy(passengers), total,
                              BookingStatus.PENDING_PAYMENT)
            # BOOKING-004, BOOKING-005: one lock guards the successful state change.
            self.store.bookings[booking.booking_id] = booking
            trip.available_seats -= len(passengers)
            return booking

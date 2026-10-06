from copy import deepcopy
from uuid import uuid4
from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.fare_policy import FarePolicy
from smart_ticket.domain.discounts import DiscountPolicy
from smart_ticket.domain.models import Booking, BookingStatus, Passenger
from smart_ticket.infrastructure.store import InMemoryStore
from smart_ticket.application.member_service import MemberService
from smart_ticket.application.seat_service import SeatService
from smart_ticket.application.audit_service import AuditService

class BookingService:
    def __init__(self, store: InMemoryStore, fare_policy: FarePolicy) -> None:
        self.store = store
        self.fare_policy = fare_policy
        self.discount_policy = DiscountPolicy(fare_policy)
        self.seats = SeatService(store)
        self.audit = AuditService(store)
        self.members = MemberService(store)

    def get(self, booking_id: str) -> Booking:
        booking = self.store.bookings.get(booking_id)
        if booking is None:
            raise DomainError("BOOKING_NOT_FOUND", "Booking not found", 404)
        return booking

    def create(self, trip_id: str, passengers: list[Passenger], member_id: str | None = None) -> Booking:
        with self.store.lock:
            trip = self.store.trips.get(trip_id)
            if trip is None:
                raise DomainError("TRIP_NOT_FOUND", "Trip not found", 404)
            if not 1 <= len(passengers) <= 4:
                raise DomainError("INVALID_PASSENGER_COUNT", "Booking requires 1 to 4 passengers", 409)
            if len(passengers) > trip.available_seats:
                raise DomainError("INSUFFICIENT_SEATS", "Insufficient available seats", 409)
            member = self.members.get(member_id) if member_id is not None else None
            total = sum(self.discount_policy.calculate(trip.base_fare, passenger.passenger_type,
                        member, self.store.clock.today, trip.departure_time.date()).amount
                        for passenger in passengers)
            booking = Booking(str(uuid4()), trip_id, deepcopy(passengers), total,
                              BookingStatus.PENDING_PAYMENT, member_id=member_id)
            assignments = self.seats.plan(booking.booking_id, trip_id, passengers)
            self.store.bookings[booking.booking_id] = booking
            self.seats.reserve(booking.booking_id, trip_id, assignments)
            booking.seat_ids = [assignment.seat_id for assignment in assignments]
            self.audit.record(booking.booking_id, "BOOKING_CREATED")
            return booking

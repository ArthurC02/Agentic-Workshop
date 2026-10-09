from copy import deepcopy
from uuid import uuid4
from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.fare_policy import FarePolicy
from smart_ticket.domain.discounts import DiscountPolicy
from smart_ticket.domain.models import (MAX_GROUP_SIZE, MIN_GROUP_SIZE, AppliedDiscount, Booking, BookingStatus,
                                        Passenger)
from smart_ticket.infrastructure.store import InMemoryStore
from smart_ticket.application.member_service import MemberService
from smart_ticket.application.seat_service import SeatService
from smart_ticket.application.audit_service import AuditService

class GroupBookingService:
    def __init__(self, store: InMemoryStore, fare_policy: FarePolicy | None = None) -> None:
        self.store = store
        self.discount_policy = DiscountPolicy(fare_policy or FarePolicy())
        self.members = MemberService(store)
        self.seats = SeatService(store)
        self.audit = AuditService(store)

    def create(self, trip_id: str, passengers: list[Passenger], member_id: str | None = None,
               redeemed_points: int = 0) -> Booking:
        with self.store.lock:
            trip = self.store.trips.get(trip_id)
            if trip is None:
                raise DomainError("TRIP_NOT_FOUND", "Trip not found", 404)
            if not MIN_GROUP_SIZE <= len(passengers) <= MAX_GROUP_SIZE:
                raise DomainError("INVALID_GROUP_SIZE",
                                  f"Group requires {MIN_GROUP_SIZE} to {MAX_GROUP_SIZE} passengers", 409)
            if len(passengers) > trip.available_seats:
                raise DomainError("INSUFFICIENT_SEATS", "Insufficient available seats", 409)
            member = self.members.get(member_id) if member_id is not None else None
            results = [self.discount_policy.calculate(trip.base_fare, passenger.passenger_type,
                       member, self.store.clock.today, trip.departure_time.date())
                       for passenger in passengers]
            applied = [AppliedDiscount(passenger.passenger_id, result.discount_type,
                       result.rate, result.amount) for passenger, result in zip(passengers, results)]
            booking_id = str(uuid4())
            assignments = self.seats.plan_group(booking_id, trip_id, passengers)
            booking = Booking(booking_id, trip_id, deepcopy(passengers),
                              sum(result.amount for result in results), BookingStatus.PENDING_PAYMENT,
                              member_id=member_id, seat_ids=[item.seat_id for item in assignments],
                              applied_discounts=applied, booking_type="GROUP", assigned_seats=assignments,
                              redeemed_points=redeemed_points)
            self.members.reserve_points(booking)
            # All validation, pricing, allocation planning and points reservation completed before commit.
            self.store.bookings[booking_id] = booking
            self.seats.reserve(booking_id, trip_id, assignments)
            self.audit.record(booking_id, "GROUP_BOOKING_CREATED")
            return booking

from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.models import AppliedDiscount, Booking, BookingStatus
from smart_ticket.domain.fare_policy import FarePolicy
from smart_ticket.domain.discounts import DiscountPolicy
from smart_ticket.infrastructure.store import InMemoryStore
from smart_ticket.application.booking_service import BookingService
from smart_ticket.application.member_service import MemberService
from smart_ticket.application.seat_service import SeatService
from smart_ticket.application.audit_service import AuditService
from smart_ticket.application.notification_service import NotificationService

class ChangeBookingService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store
        self.seats = SeatService(store)
        self.audit = AuditService(store)
        self.notifications = NotificationService(store)
        self.discount_policy = DiscountPolicy(FarePolicy())

    def change(self, booking_id: str, trip_id: str) -> Booking:
        with self.store.lock:
            booking = BookingService(self.store, FarePolicy()).get(booking_id)
            if booking.booking_type == "GROUP":
                raise DomainError("GROUP_CHANGE_NOT_SUPPORTED", "Group change is outside supported scope", 409)
            if booking.status != BookingStatus.PAID:
                raise DomainError("BOOKING_NOT_CHANGEABLE", "Only paid bookings can be changed", 409)
            target = self.store.trips.get(trip_id)
            if target is None:
                raise DomainError("TRIP_NOT_FOUND", "Trip not found", 404)
            if trip_id == booking.trip_id:
                raise DomainError("SAME_TRIP", "Target trip must differ", 409)
            if len(booking.passengers) > target.available_seats:
                raise DomainError("INSUFFICIENT_SEATS", "Insufficient available seats", 409)
            member = MemberService(self.store).get(booking.member_id) if booking.member_id else None
            results = [self.discount_policy.calculate(target.base_fare, passenger.passenger_type,
                       member, self.store.clock.today, target.departure_time.date())
                       for passenger in booking.passengers]
            total = sum(result.amount for result in results)
            applied_discounts = [AppliedDiscount(passenger.passenger_id, result.discount_type,
                                 result.rate, result.amount)
                                 for passenger, result in zip(booking.passengers, results)]
            assignments = self.seats.plan(booking_id, trip_id, booking.passengers)
            difference = total - booking.total_fare
            self.seats.release(booking_id)
            self.seats.reserve(booking_id, trip_id, assignments)
            booking.trip_id = trip_id
            booking.total_fare = total
            booking.applied_discounts = applied_discounts
            booking.fare_difference = difference
            booking.seat_ids = [assignment.seat_id for assignment in assignments]
            self.audit.record(booking_id, "BOOKING_CHANGED", f"fare_difference={difference}")
            self.notifications.record(booking_id, "BOOKING_CHANGED")
            return booking

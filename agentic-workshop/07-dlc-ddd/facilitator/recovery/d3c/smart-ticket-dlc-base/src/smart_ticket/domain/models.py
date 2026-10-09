from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from smart_ticket.domain.records import SeatAssignment
from smart_ticket.domain.members import points_value
from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.cancellation import PassengerCancellation, cancellation_fee, cancellation_fee_percent

MIN_GROUP_SIZE = 5    # GROUP-001; a partly cancelled group may not drop below it either (PCR-005)
MAX_GROUP_SIZE = 20   # GROUP-002

class PassengerType(StrEnum):
    ADULT = "ADULT"
    STUDENT = "STUDENT"

class BookingStatus(StrEnum):
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"

class PaymentStatus(StrEnum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

@dataclass
class Trip:
    trip_id: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    base_fare: int
    available_seats: int

@dataclass
class Passenger:
    passenger_id: str
    name: str
    passenger_type: PassengerType

@dataclass
class AppliedDiscount:
    passenger_id: str
    discount_type: str
    rate: int
    amount: int

@dataclass
class Booking:
    booking_id: str
    trip_id: str
    passengers: list[Passenger]
    total_fare: int
    status: BookingStatus
    member_id: str | None = None
    seat_ids: list[str] = field(default_factory=list)
    fare_difference: int = 0
    applied_discounts: list[AppliedDiscount] = field(default_factory=list)
    booking_type: str = "INDIVIDUAL"
    assigned_seats: list[SeatAssignment] = field(default_factory=list)
    redeemed_points: int = 0
    cancelled_passenger_ids: list[str] = field(default_factory=list)

    @property
    def payable_amount(self) -> int:
        """PTS-007, PTS-009: what the gateway charges; total_fare stays the discounted total."""
        return self.total_fare - points_value(self.redeemed_points)

    @property
    def active_passenger_ids(self) -> list[str]:
        return [p.passenger_id for p in self.passengers if p.passenger_id not in self.cancelled_passenger_ids]

    def cancel_passengers(self, passenger_ids: list[str], days_before_departure: int) -> PassengerCancellation:
        """PCR-001 to PCR-005, PCR-008, PCR-009: the only way a passenger leaves a paid group.

        Every refusal comes before any change (PCR-011). Each cancelled fare splits exactly into
        fee + refund and total_fare never changes, so refunds + fees + active fares = Order.amount.
        """
        if self.booking_type != "GROUP" or self.redeemed_points:
            raise DomainError("PARTIAL_CANCEL_NOT_SUPPORTED",
                              "Only group bookings without redeemed points can cancel passengers", 409)
        if self.status != BookingStatus.PAID:
            raise DomainError("BOOKING_NOT_REFUNDABLE", "Only paid bookings can be refunded", 409)
        if not passenger_ids or len(set(passenger_ids)) != len(passenger_ids):
            raise DomainError("INVALID_PASSENGER_IDS", "List at least one passenger, each once", 422)
        percent = cancellation_fee_percent(days_before_departure)
        active = self.active_passenger_ids
        for passenger_id in passenger_ids:
            if passenger_id in self.cancelled_passenger_ids:
                raise DomainError("PASSENGER_ALREADY_CANCELLED", f"Passenger {passenger_id} is already cancelled", 409)
            if passenger_id not in active:
                raise DomainError("PASSENGER_NOT_FOUND", f"Passenger {passenger_id} is not in this booking", 404)
        if 0 < len(active) - len(passenger_ids) < MIN_GROUP_SIZE:
            raise DomainError("GROUP_BELOW_MINIMUM",
                              f"A group keeps at least {MIN_GROUP_SIZE} active passengers, or none", 409)
        fares = [line.amount for line in self.applied_discounts if line.passenger_id in passenger_ids]
        fee = sum(cancellation_fee(fare, percent) for fare in fares)
        self.cancelled_passenger_ids += passenger_ids
        self.assigned_seats = [seat for seat in self.assigned_seats if seat.passenger_id not in passenger_ids]
        self.seat_ids = [seat.seat_id for seat in self.assigned_seats]
        if not self.active_passenger_ids:
            self.status = BookingStatus.REFUNDED
        return PassengerCancellation(list(passenger_ids), fee, sum(fares) - fee)

    def refund_in_full(self) -> list[str]:
        """REFUND-001, REFUND-002, PCR-012: the whole booking at once, only if nobody was cancelled before."""
        if self.status != BookingStatus.PAID or self.cancelled_passenger_ids:
            raise DomainError("BOOKING_NOT_REFUNDABLE", "Only paid bookings with no cancelled passengers can be refunded in full", 409)
        self.cancelled_passenger_ids = self.active_passenger_ids
        self.status = BookingStatus.REFUNDED
        self.seat_ids = []
        self.assigned_seats = []
        return list(self.cancelled_passenger_ids)

@dataclass
class Order:
    order_id: str
    booking_id: str
    amount: int
    payment_status: PaymentStatus

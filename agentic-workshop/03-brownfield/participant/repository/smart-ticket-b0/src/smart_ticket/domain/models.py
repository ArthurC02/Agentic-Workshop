from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

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
class Booking:
    booking_id: str
    trip_id: str
    passengers: list[Passenger]
    total_fare: int
    status: BookingStatus
    member_id: str | None = None
    seat_ids: list[str] = field(default_factory=list)
    fare_difference: int = 0

@dataclass
class Order:
    order_id: str
    booking_id: str
    amount: int
    payment_status: PaymentStatus

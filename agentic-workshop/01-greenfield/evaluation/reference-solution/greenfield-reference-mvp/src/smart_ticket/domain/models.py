from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

class PassengerType(StrEnum):
    ADULT = "ADULT"
    STUDENT = "STUDENT"

class BookingStatus(StrEnum):
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAID = "PAID"
    CANCELLED = "CANCELLED"

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

@dataclass
class Order:
    order_id: str
    booking_id: str
    amount: int
    payment_status: PaymentStatus

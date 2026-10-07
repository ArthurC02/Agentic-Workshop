from datetime import datetime
from pydantic import BaseModel, ConfigDict
from smart_ticket.domain.models import BookingStatus, PassengerType, PaymentStatus

class DomainResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class PassengerRequest(DomainResponse):
    passenger_id: str
    name: str
    passenger_type: PassengerType

class BookingRequest(BaseModel):
    trip_id: str
    passengers: list[PassengerRequest]
    member_id: str | None = None

class TripResponse(DomainResponse):
    trip_id: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    base_fare: int
    available_seats: int

class AppliedDiscountResponse(DomainResponse):
    passenger_id: str
    discount_type: str
    rate: int
    amount: int

class AssignedSeatResponse(DomainResponse):
    booking_id: str
    passenger_id: str
    trip_id: str
    seat_id: str
    carriage_id: str
    row_number: int
    seat_number: int
    position: int

class BookingResponse(DomainResponse):
    booking_id: str
    trip_id: str
    passengers: list[PassengerRequest]
    total_fare: int
    status: BookingStatus
    member_id: str | None = None
    seat_ids: list[str] = []
    fare_difference: int = 0
    applied_discounts: list[AppliedDiscountResponse] = []
    booking_type: str = "INDIVIDUAL"
    assigned_seats: list[AssignedSeatResponse] = []

class OrderResponse(DomainResponse):
    order_id: str
    booking_id: str
    amount: int
    payment_status: PaymentStatus

class ChangeRequest(BaseModel):
    target_trip_id: str

class MemberResponse(DomainResponse):
    member_id: str
    member_type: str
    points_balance: int

class RefundResponse(DomainResponse):
    refund_id: str
    booking_id: str
    amount: int

class NotificationResponse(DomainResponse):
    notification_id: str
    booking_id: str
    event: str
    created_at: datetime

class AuditResponse(DomainResponse):
    audit_id: str
    booking_id: str
    event: str
    created_at: datetime
    detail: str

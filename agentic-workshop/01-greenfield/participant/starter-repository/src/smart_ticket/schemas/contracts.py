from datetime import datetime
from pydantic import BaseModel, ConfigDict
from smart_ticket.domain.models import BookingStatus, PassengerType, PaymentStatus

class DomainResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class PassengerRequest(BaseModel):
    passenger_id: str
    name: str
    passenger_type: PassengerType

class BookingRequest(BaseModel):
    trip_id: str
    passengers: list[PassengerRequest]

class TripResponse(DomainResponse):
    trip_id: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    base_fare: int
    available_seats: int

class BookingResponse(DomainResponse):
    booking_id: str
    trip_id: str
    passengers: list[PassengerRequest]
    total_fare: int
    status: BookingStatus

class OrderResponse(DomainResponse):
    order_id: str
    booking_id: str
    amount: int
    payment_status: PaymentStatus

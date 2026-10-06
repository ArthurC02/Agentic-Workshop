from fastapi import APIRouter
from smart_ticket.schemas.contracts import BookingRequest, BookingResponse, OrderResponse, TripResponse
from smart_ticket.domain.models import Passenger
from smart_ticket.api import dependencies

router = APIRouter()

@router.get("/trips", response_model=list[TripResponse])
def query_trips(origin: str | None = None, destination: str | None = None) -> list[TripResponse]:
    return [TripResponse.model_validate(trip)
            for trip in dependencies.trip_service.query(origin, destination)]

@router.post("/bookings", response_model=BookingResponse, status_code=201)
def create_booking(request: BookingRequest) -> BookingResponse:
    passengers = [Passenger(**passenger.model_dump()) for passenger in request.passengers]
    return BookingResponse.model_validate(dependencies.booking_service.create(request.trip_id, passengers))

@router.post("/bookings/{booking_id}/pay", response_model=OrderResponse)
def pay_booking(booking_id: str) -> OrderResponse:
    return OrderResponse.model_validate(dependencies.payment_service.pay(booking_id))

@router.get("/orders/{order_id}", response_model=OrderResponse)
def query_order(order_id: str) -> OrderResponse:
    return OrderResponse.model_validate(dependencies.order_service.get(order_id))

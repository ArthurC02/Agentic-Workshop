from fastapi import APIRouter, HTTPException
from smart_ticket.schemas.contracts import BookingRequest, BookingResponse, OrderResponse, TripResponse
from smart_ticket.api import dependencies

router = APIRouter()

@router.get("/trips", response_model=list[TripResponse])
def query_trips(origin: str | None = None, destination: str | None = None) -> list[TripResponse]:
    # TODO(GREENFIELD, TRIP-001, TRIP-002): Connect query schema to TripService.
    raise HTTPException(501, "Trip query is not implemented in G0")

@router.post("/bookings", response_model=BookingResponse, status_code=201)
def create_booking(request: BookingRequest) -> BookingResponse:
    # TODO(GREENFIELD, BOOKING-001, BOOKING-005): Map request to domain and BookingService.
    raise HTTPException(501, "Booking creation is not implemented in G0")

@router.post("/bookings/{booking_id}/pay", response_model=OrderResponse)
def pay_booking(booking_id: str) -> OrderResponse:
    # TODO(GREENFIELD, PAYMENT-001, ORDER-001): Connect payment and response mapping.
    raise HTTPException(501, "Payment is not implemented in G0")

@router.get("/orders/{order_id}", response_model=OrderResponse)
def query_order(order_id: str) -> OrderResponse:
    # TODO(GREENFIELD, ORDER-001, ORDER-002): Connect OrderService and missing-order error.
    raise HTTPException(501, "Order query is not implemented in G0")

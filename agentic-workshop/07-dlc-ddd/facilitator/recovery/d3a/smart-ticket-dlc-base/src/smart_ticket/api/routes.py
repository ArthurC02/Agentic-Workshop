from fastapi import APIRouter
from smart_ticket.schemas.contracts import (BookingRequest, BookingResponse, InvoiceResponse, OrderResponse,
                                          PaymentRequest, TripResponse)
from smart_ticket.domain.models import Passenger
from smart_ticket.domain.invoicing import InvoiceBuyer
from smart_ticket.api import dependencies

router = APIRouter()

@router.get("/trips", response_model=list[TripResponse])
def query_trips(origin: str | None = None, destination: str | None = None) -> list[TripResponse]:
    return [TripResponse.model_validate(trip)
            for trip in dependencies.trip_service.query(origin, destination)]

@router.post("/bookings", response_model=BookingResponse, status_code=201)
def create_booking(request: BookingRequest) -> BookingResponse:
    passengers = [Passenger(**passenger.model_dump()) for passenger in request.passengers]
    return BookingResponse.model_validate(dependencies.booking_service.create(request.trip_id, passengers, request.member_id))

def invoice_buyer(request: PaymentRequest | None) -> InvoiceBuyer:
    """EINV-012/013: validated before anything is charged."""
    if request is None or request.invoice is None:
        return InvoiceBuyer()
    return InvoiceBuyer(**request.invoice.model_dump())

@router.post("/bookings/{booking_id}/pay", response_model=OrderResponse)
def pay_booking(booking_id: str, request: PaymentRequest | None = None) -> OrderResponse:
    return OrderResponse.model_validate(
        dependencies.payment_service.pay(booking_id, invoice_buyer(request)))

@router.get("/orders/{order_id}", response_model=OrderResponse)
def query_order(order_id: str) -> OrderResponse:
    return OrderResponse.model_validate(dependencies.order_service.get(order_id))

from smart_ticket.schemas.contracts import (ChangeRequest, MemberResponse, RefundResponse,
                                          NotificationResponse, AuditResponse)

@router.get("/bookings/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: str) -> BookingResponse:
    return BookingResponse.model_validate(dependencies.booking_service.get(booking_id))

@router.get("/members/{member_id}", response_model=MemberResponse)
def get_member(member_id: str) -> MemberResponse:
    return MemberResponse.model_validate(dependencies.member_service.get(member_id))

@router.post("/bookings/{booking_id}/change", response_model=BookingResponse)
def change_booking(booking_id: str, request: ChangeRequest) -> BookingResponse:
    return BookingResponse.model_validate(dependencies.change_service.change(booking_id, request.target_trip_id))

@router.post("/bookings/{booking_id}/refund", response_model=RefundResponse)
def refund_booking(booking_id: str) -> RefundResponse:
    return RefundResponse.model_validate(dependencies.refund_service.refund(booking_id))

@router.get("/bookings/{booking_id}/notifications", response_model=list[NotificationResponse])
def get_notifications(booking_id: str) -> list[NotificationResponse]:
    return [NotificationResponse.model_validate(entry)
            for entry in dependencies.notification_service.list_for(booking_id)]

@router.get("/bookings/{booking_id}/audit-log", response_model=list[AuditResponse])
def get_audit_log(booking_id: str) -> list[AuditResponse]:
    return [AuditResponse.model_validate(entry)
            for entry in dependencies.audit_service.list_for(booking_id)]

@router.post("/group-bookings", response_model=BookingResponse, status_code=201)
def create_group_booking(request: BookingRequest) -> BookingResponse:
    passengers = [Passenger(**passenger.model_dump()) for passenger in request.passengers]
    return BookingResponse.model_validate(dependencies.group_booking_service.create(
        request.trip_id, passengers, request.member_id))

@router.post("/group-bookings/{booking_id}/pay", response_model=OrderResponse)
def pay_group_booking(booking_id: str, request: PaymentRequest | None = None) -> OrderResponse:
    return OrderResponse.model_validate(
        dependencies.payment_service.pay_group(booking_id, invoice_buyer(request)))

@router.get("/orders/{order_id}/invoice", response_model=InvoiceResponse)
def get_invoice(order_id: str) -> InvoiceResponse:
    return InvoiceResponse.model_validate(dependencies.invoicing_service.get(order_id))

@router.post("/orders/{order_id}/invoice/retry", response_model=InvoiceResponse)
def retry_invoice(order_id: str) -> InvoiceResponse:
    """EINV-007: for a scheduler or an operator; ISSUED and FAILED return unchanged."""
    return InvoiceResponse.model_validate(dependencies.invoicing_service.issue(order_id))

from smart_ticket.application.booking_service import BookingService
from smart_ticket.application.order_service import OrderService
from smart_ticket.application.payment_service import PaymentService
from smart_ticket.application.trip_service import TripService
from smart_ticket.domain.fare_policy import FarePolicy
from smart_ticket.infrastructure.payment_gateway import MockPaymentGateway
from smart_ticket.infrastructure.store import InMemoryStore

store = InMemoryStore()
gateway = MockPaymentGateway()
trip_service = TripService(store)
booking_service = BookingService(store, FarePolicy())
payment_service = PaymentService(store, gateway)
order_service = OrderService(store)

def reset_state() -> None:
    store.reset()
    gateway.reset()

from smart_ticket.domain.models import Order
from smart_ticket.infrastructure.payment_gateway import MockPaymentGateway
from smart_ticket.infrastructure.store import InMemoryStore

class PaymentService:
    def __init__(self, store: InMemoryStore, gateway: MockPaymentGateway) -> None:
        self.store = store
        self.gateway = gateway

    def pay(self, booking_id: str) -> Order:
        # TODO(GREENFIELD, PAYMENT-001, PAYMENT-003): Validate payment state.
        # TODO(GREENFIELD, PAYMENT-002, ORDER-001, ORDER-002): Apply successful payment and create order.
        raise NotImplementedError("Payment use case is not implemented in G0")

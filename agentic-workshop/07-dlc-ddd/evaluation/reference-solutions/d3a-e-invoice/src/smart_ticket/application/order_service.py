from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.models import Order
from smart_ticket.domain.repositories import TicketRepositories

class OrderService:
    def __init__(self, store: TicketRepositories) -> None:
        self.store = store

    def get(self, order_id: str) -> Order:
        # ORDER-001, ORDER-002: query persisted payment transaction.
        order = self.store.orders.get(order_id)
        if order is None:
            raise DomainError("ORDER_NOT_FOUND", "Order not found", 404)
        return order

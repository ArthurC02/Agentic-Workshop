from smart_ticket.domain.models import Order
from smart_ticket.infrastructure.store import InMemoryStore

class OrderService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def get(self, order_id: str) -> Order:
        # TODO(GREENFIELD, ORDER-001, ORDER-002): Retrieve order or report missing resource.
        raise NotImplementedError("Order query is not implemented in G0")

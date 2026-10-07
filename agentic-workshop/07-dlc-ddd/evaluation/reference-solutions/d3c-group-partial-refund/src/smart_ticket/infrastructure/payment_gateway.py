from smart_ticket.domain.models import PaymentStatus

class MockPaymentGateway:
    """Deterministic local adapter. Set next_result to FAILED in tests."""
    def __init__(self) -> None:
        self.next_result = PaymentStatus.SUCCESS

    def reset(self) -> None:
        self.next_result = PaymentStatus.SUCCESS

    def charge(self, booking_id: str, amount: int) -> PaymentStatus:
        return self.next_result

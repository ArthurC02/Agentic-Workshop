from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.invoicing import (Invoice, InvoiceBuyer, InvoiceIssuer, InvoiceStatus,
                                           request_for_order)
from smart_ticket.domain.models import Booking, Order, Trip
from smart_ticket.infrastructure.store import InMemoryStore
from smart_ticket.application.audit_service import AuditService
from smart_ticket.application.notification_service import NotificationService


class InvoicingService:
    def __init__(self, store: InMemoryStore, issuer: InvoiceIssuer) -> None:
        self.store = store
        self.issuer = issuer
        self.audit = AuditService(store)
        self.notifications = NotificationService(store)

    def open(self, order: Order, booking: Booking, trip: Trip, buyer: InvoiceBuyer) -> Invoice:
        """EINV-001: record the duty to invoice this Order. Called once, inside the payment lock;
        PAYMENT-003 already guarantees one Order per Booking, so no second invoice can be opened."""
        request = request_for_order(order.order_id, order.amount, self.store.clock.today, buyer,
                                    trip.origin, trip.destination, len(booking.passengers))
        invoice = Invoice(booking.booking_id, request)
        self.store.invoices[order.order_id] = invoice
        return invoice

    def issue(self, order_id: str) -> Invoice:
        """First attempt and the retry operation (EINV-007): same order_id every time."""
        with self.store.lock:
            invoice = self.get(order_id)
            if invoice.status is not InvoiceStatus.PENDING:
                return invoice   # EINV-011: ISSUED (or FAILED) never calls the provider again
        # Outside the store lock: the provider may take up to its call timeout.
        result = self.issuer.issue(invoice.request)
        with self.store.lock:
            before = invoice.status
            invoice.record(result)
            if before is InvoiceStatus.PENDING:
                self._report_settlement(invoice)
            return invoice

    def get(self, order_id: str) -> Invoice:
        invoice = self.store.invoices.get(order_id)
        if invoice is None:
            raise DomainError("INVOICE_NOT_FOUND", "Invoice not found", 404)
        return invoice

    def _report_settlement(self, invoice: Invoice) -> None:
        """EINV-014: only a transition out of PENDING is reported; PENDING failures stay quiet."""
        if invoice.status is InvoiceStatus.ISSUED:
            self.audit.record(invoice.booking_id, "INVOICE_ISSUED", invoice.invoice_number)
            self.notifications.record(invoice.booking_id, "INVOICE_ISSUED")
        elif invoice.status is InvoiceStatus.FAILED:
            self.audit.record(invoice.booking_id, "INVOICE_FAILED",
                              f"error={invoice.last_error} attempts={invoice.attempts}")

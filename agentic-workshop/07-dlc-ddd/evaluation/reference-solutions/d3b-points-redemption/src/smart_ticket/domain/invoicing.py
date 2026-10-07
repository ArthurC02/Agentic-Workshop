"""Invoicing Context: one e-invoice per paid Order (EINV-001 to EINV-014).

Knows nothing about the e-invoice provider: it talks to it only through the
InvoiceIssuer Port below. Provider codes, timeout and transport live in
infrastructure/einvoice_provider.py.
"""
import re
from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from typing import Protocol
from smart_ticket.domain.errors import DomainError

VAT_RATE_PERCENT = 5        # fares are VAT-inclusive
MAX_ISSUE_ATTEMPTS = 5      # provider calls per invoice, the first one included (EINV-008)

BUSINESS_ID_PATTERN = re.compile(r"[0-9]{8}")                # 統一編號
MOBILE_BARCODE_PATTERN = re.compile(r"/[0-9A-Z.+\-]{7}")     # 手機條碼載具


def split_vat(total_amount: int) -> tuple[int, int]:
    """EINV-003: sales = round(total / 1.05) half-up, tax = total - sales; integers only."""
    gross_percent = 100 + VAT_RATE_PERCENT
    sales_amount, remainder = divmod(total_amount * 100, gross_percent)
    if remainder * 2 >= gross_percent:
        sales_amount += 1
    return sales_amount, total_amount - sales_amount


@dataclass(frozen=True)
class InvoiceBuyer:
    """EINV-012/013: a business ID (with company name) or a mobile barcode, never both."""
    business_id: str | None = None
    company_name: str | None = None
    mobile_barcode: str | None = None

    def __post_init__(self) -> None:
        if self.business_id is not None and self.mobile_barcode is not None:
            raise _invalid("Provide either a business ID or a mobile barcode, not both")
        if self.business_id is not None and not BUSINESS_ID_PATTERN.fullmatch(self.business_id):
            raise _invalid("Business ID must be 8 digits")
        if self.business_id is not None and not self.company_name:
            raise _invalid("Business ID requires a company name")
        if self.mobile_barcode is not None and not MOBILE_BARCODE_PATTERN.fullmatch(self.mobile_barcode):
            raise _invalid("Mobile barcode must be '/' followed by 7 of 0-9 A-Z . + -")


def _invalid(message: str) -> DomainError:
    return DomainError("INVALID_INVOICE_INFO", message, 422)


@dataclass(frozen=True)
class InvoiceLine:
    description: str
    quantity: int
    unit_price: int
    amount: int


@dataclass(frozen=True)
class InvoiceRequest:
    """What Invoicing asks the provider to issue, in our own terms. order_id is the idempotency key."""
    order_id: str
    issue_date: date
    buyer: InvoiceBuyer
    line: InvoiceLine
    sales_amount: int
    tax_amount: int
    total_amount: int


def request_for_order(order_id: str, order_amount: int, issue_date: date, buyer: InvoiceBuyer,
                      origin: str, destination: str, passenger_count: int) -> InvoiceRequest:
    """EINV-003/004: one line per Order, total = Order.amount, unit price floored."""
    line = InvoiceLine(f"{origin}-{destination} 車票", passenger_count,
                       order_amount // passenger_count, order_amount)
    sales_amount, tax_amount = split_vat(order_amount)
    return InvoiceRequest(order_id, issue_date, buyer, line, sales_amount, tax_amount, order_amount)


class IssueOutcome(StrEnum):
    """The only distinctions Invoicing needs from the provider."""
    ISSUED = "ISSUED"            # we have an invoice number (new or previously issued)
    REJECTED = "REJECTED"        # permanent: retrying the same request cannot succeed
    UNAVAILABLE = "UNAVAILABLE"  # temporary or unknown: safe to retry with the same order_id


@dataclass(frozen=True)
class IssueResult:
    outcome: IssueOutcome
    invoice_number: str | None = None
    error: str | None = None


class InvoiceIssuer(Protocol):
    """Port: issue the invoice described by the request. Never raises for provider failures."""
    def issue(self, request: InvoiceRequest) -> IssueResult: ...


class InvoiceStatus(StrEnum):
    PENDING = "PENDING"
    ISSUED = "ISSUED"
    FAILED = "FAILED"


@dataclass
class Invoice:
    booking_id: str
    request: InvoiceRequest
    status: InvoiceStatus = InvoiceStatus.PENDING
    invoice_number: str | None = None
    attempts: int = 0
    last_error: str | None = None

    @property
    def order_id(self) -> str:
        return self.request.order_id

    def record(self, result: IssueResult) -> None:
        """EINV-006 to EINV-011: apply one provider answer. A settled invoice never changes."""
        if self.status is not InvoiceStatus.PENDING:
            return
        self.attempts += 1
        if result.outcome is IssueOutcome.ISSUED:
            self.status = InvoiceStatus.ISSUED
            self.invoice_number = result.invoice_number
            return
        self.last_error = result.error
        if result.outcome is IssueOutcome.REJECTED or self.attempts >= MAX_ISSUE_ATTEMPTS:
            self.status = InvoiceStatus.FAILED

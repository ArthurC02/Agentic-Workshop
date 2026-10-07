"""Adapter for the e-invoice provider. The only module that knows its wire format and codes."""
from dataclasses import dataclass
from smart_ticket.domain.invoicing import InvoiceIssuer, InvoiceRequest, IssueOutcome, IssueResult

CALL_TIMEOUT_SECONDS = 3
ISSUED_CODES = {"0000", "2001"}       # 2001 = already issued for this merchant_order_no
REJECTED_CODES = {"1001", "1002"}     # field format / business ID check failed
TRANSPORT_FAILURES = {TimeoutError: "TIMEOUT", ConnectionError: "CONNECTION_FAILED"}


class EInvoiceProviderAdapter(InvoiceIssuer):
    """Translates InvoiceRequest to the provider's request and its answer to an IssueResult."""
    def __init__(self, transport: "SimulatedEInvoiceProvider") -> None:
        self.transport = transport

    def issue(self, request: InvoiceRequest) -> IssueResult:
        try:
            reply = self.transport.post_issue(to_provider_payload(request), timeout=CALL_TIMEOUT_SECONDS)
        except (TimeoutError, ConnectionError) as error:
            # Outcome unknown: the provider may have issued it. Retrying with the same
            # merchant_order_no is safe because the provider answers 2001 for a duplicate.
            return IssueResult(IssueOutcome.UNAVAILABLE, error=TRANSPORT_FAILURES[type(error)])
        code = reply["code"]
        if code in ISSUED_CODES:
            return IssueResult(IssueOutcome.ISSUED, invoice_number=reply["invoice_number"])
        if code in REJECTED_CODES:
            return IssueResult(IssueOutcome.REJECTED, error=code)
        return IssueResult(IssueOutcome.UNAVAILABLE, error=code)   # 9001 and any unknown code


def to_provider_payload(request: InvoiceRequest) -> dict:
    buyer = request.buyer
    payload = {
        "merchant_order_no": request.order_id,
        "issue_date": request.issue_date.isoformat(),
        "items": [{"description": request.line.description, "quantity": request.line.quantity,
                   "unit_price": request.line.unit_price, "amount": request.line.amount}],
        "sales_amount": request.sales_amount,
        "tax_amount": request.tax_amount,
        "total_amount": request.total_amount,
    }
    if buyer.business_id is not None:
        payload |= {"buyer_ban": buyer.business_id, "buyer_name": buyer.company_name}
    if buyer.mobile_barcode is not None:
        payload |= {"carrier_type": "MOBILE_BARCODE", "carrier_id": buyer.mobile_barcode}
    return payload


@dataclass
class SimulatedReply:
    code: str                 # provider code to answer, or "DOWN" for a refused connection
    latency_seconds: float = 0


class SimulatedEInvoiceProvider:
    """Stands in for the provider's HTTPS endpoint; no network. Tests queue replies.

    ponytail: a real transport (httpx.post(url, json=payload, timeout=timeout)) replaces
    only this class; EInvoiceProviderAdapter and everything above it stay unchanged.
    """
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.replies: list[SimulatedReply] = []
        self.received: list[dict] = []
        self.issued: dict[str, str] = {}   # merchant_order_no -> invoice_number

    def queue(self, code: str, latency_seconds: float = 0) -> None:
        self.replies.append(SimulatedReply(code, latency_seconds))

    def post_issue(self, payload: dict, timeout: float) -> dict:
        self.received.append(payload)
        reply = self.replies.pop(0) if self.replies else SimulatedReply("0000")
        if reply.code == "DOWN":
            raise ConnectionError("provider unreachable")
        answer = self._answer(payload["merchant_order_no"], reply.code)
        if reply.latency_seconds > timeout:
            raise TimeoutError("no answer within timeout")   # the provider still did the work
        return answer

    def _answer(self, order_no: str, code: str) -> dict:
        if code != "0000":
            return {"code": code}
        if order_no in self.issued:
            return {"code": "2001", "invoice_number": self.issued[order_no]}
        self.issued[order_no] = f"AB{len(self.issued) + 10000001:08d}"
        return {"code": "0000", "invoice_number": self.issued[order_no], "random_number": "1234"}

"""Acceptance tests for requirement card 01 (EINV-001 to EINV-015).

The provider is SimulatedEInvoiceProvider (EINV-015): tests queue its replies
("0000", "2001", "1001", "1002", "9001", "DOWN") and a latency to simulate timeouts.
"""
import re
import threading
from datetime import date
import pytest
from smart_ticket.api import dependencies
from smart_ticket.domain.invoicing import (Invoice, InvoiceBuyer, InvoiceLine, InvoiceRequest,
                                           IssueOutcome, IssueResult)
from smart_ticket.domain.models import BookingStatus
from smart_ticket.infrastructure.einvoice_provider import EInvoiceProviderAdapter, SimulatedEInvoiceProvider

ADULT = {"passenger_id": "A", "name": "Adult", "passenger_type": "ADULT"}
STUDENT = {"passenger_id": "S", "name": "Student", "passenger_type": "STUDENT"}


@pytest.fixture
def provider():
    return dependencies.invoice_provider


@pytest.fixture
def book(client):
    def create(passengers=(ADULT,), member_id=None, group=False):
        body = {"trip_id": "T001", "passengers": list(passengers), "member_id": member_id}
        response = client.post("/group-bookings" if group else "/bookings", json=body)
        assert response.status_code == 201, response.text
        return response.json()
    return create


@pytest.fixture
def pay(client):
    def run(booking, invoice=None, expected=200):
        prefix = "/group-bookings" if booking["booking_type"] == "GROUP" else "/bookings"
        body = None if invoice is None else {"invoice": invoice}
        response = client.post(f"{prefix}/{booking['booking_id']}/pay", json=body)
        assert response.status_code == expected, response.text
        return response.json()
    return run


@pytest.fixture
def invoice_of(client):
    def get(order_id):
        response = client.get(f"/orders/{order_id}/invoice")
        assert response.status_code == 200, response.text
        return response.json()
    return get


@pytest.fixture
def retry(client):
    def run(order_id):
        response = client.post(f"/orders/{order_id}/invoice/retry")
        assert response.status_code == 200, response.text
        return response.json()
    return run


def group_of(count):
    return [{"passenger_id": f"G{i}", "name": f"G{i}", "passenger_type": "ADULT"} for i in range(count)]


def test_einv_001_individual_and_group_payment_each_issue_one_invoice(book, pay, invoice_of, provider):
    individual = pay(book())
    group = pay(book(group_of(5), group=True))
    assert invoice_of(individual["order_id"])["status"] == "ISSUED"
    assert invoice_of(group["order_id"])["status"] == "ISSUED"
    assert [p["merchant_order_no"] for p in provider.received] == [individual["order_id"], group["order_id"]]
    assert provider.received[1]["items"][0]["quantity"] == 5   # whole group on one invoice


@pytest.mark.parametrize("reply", ["9001", "1001", "1002", "DOWN"])
def test_einv_002_invoice_failure_never_affects_payment(client, book, pay, invoice_of, provider, memory_store, reply):
    booking = book()
    provider.queue(reply)
    order = pay(booking)                                     # still 200
    assert order["amount"] == 700
    assert memory_store.bookings[booking["booking_id"]].status == BookingStatus.PAID
    assert client.get(f"/orders/{order['order_id']}").json()["amount"] == 700
    assert invoice_of(order["order_id"])["status"] in {"PENDING", "FAILED"}


def test_einv_002_provider_timeout_never_affects_payment(book, pay, invoice_of, provider, memory_store):
    booking = book(group_of(5), group=True)
    provider.queue("9001", latency_seconds=10)
    order = pay(booking)
    assert order["amount"] == 3500
    assert memory_store.bookings[booking["booking_id"]].status == BookingStatus.PAID
    assert invoice_of(order["order_id"])["status"] == "PENDING"


class LockProbe:
    """Issuer stand-in that records whether another thread could take the store lock during the call."""
    def __init__(self):
        self.lock_free_during_call = []

    def issue(self, request):
        acquired = []
        def probe():
            got = dependencies.store.lock.acquire(timeout=1)
            acquired.append(got)
            if got:
                dependencies.store.lock.release()
        thread = threading.Thread(target=probe)
        thread.start()
        thread.join()
        self.lock_free_during_call.append(acquired[0])
        return IssueResult(IssueOutcome.ISSUED, invoice_number="AB00000001")


@pytest.mark.parametrize("group", [False, True])
def test_einv_002_provider_is_called_outside_the_store_lock(book, pay, monkeypatch, group):
    probe = LockProbe()
    monkeypatch.setattr(dependencies.invoicing_service, "issuer", probe)
    pay(book(group_of(5), group=True) if group else book())
    assert probe.lock_free_during_call == [True]


@pytest.mark.parametrize("passengers, member_id, group, sales, tax", [
    ((ADULT,), None, False, 667, 33),              # 700
    (group_of(5), None, True, 3333, 167),          # 3,500
    ((ADULT,), "M002", False, 633, 32),            # 665 (corporate 95%)
])
def test_einv_003_vat_split_from_order_amount(book, pay, provider, passengers, member_id, group, sales, tax):
    order = pay(book(passengers, member_id, group))
    payload = provider.received[0]
    assert payload["total_amount"] == order["amount"]
    assert (payload["sales_amount"], payload["tax_amount"]) == (sales, tax)
    assert all(type(payload[key]) is int for key in ("sales_amount", "tax_amount", "total_amount"))


@pytest.mark.parametrize("passengers, unit_price", [
    ((ADULT, STUDENT), 612),                                 # 1,225 / 2 = 612.5
    ((ADULT, dict(ADULT, passenger_id="A2"), STUDENT), 641), # 1,925 / 3 = 641.67 (rounding would give 642)
])
def test_einv_004_single_line_with_route_quantity_and_floored_unit_price(book, pay, provider, passengers, unit_price):
    order = pay(book(passengers))
    assert provider.received[0]["items"] == [
        {"description": "台北-台中 車票", "quantity": len(passengers),
         "unit_price": unit_price, "amount": order["amount"]}]


def test_einv_005_timeout_after_provider_issued_does_not_create_a_second_invoice(book, pay, retry, provider):
    provider.queue("0000", latency_seconds=5)                # provider issues, answer arrives too late
    order = pay(book())
    first = retry(order["order_id"])
    retry(order["order_id"])
    assert first["status"] == "ISSUED"
    assert list(provider.issued) == [order["order_id"]]       # exactly one invoice at the provider
    assert first["invoice_number"] == provider.issued[order["order_id"]]
    assert {p["merchant_order_no"] for p in provider.received} == {order["order_id"]}


def test_einv_006_invoice_status_is_queryable_by_order_id(client, book, pay, invoice_of, retry, provider):
    provider.queue("9001")
    order = pay(book())
    pending = invoice_of(order["order_id"])
    assert (pending["status"], pending["invoice_number"]) == ("PENDING", None)
    issued = retry(order["order_id"])
    assert issued == invoice_of(order["order_id"])
    assert issued["status"] == "ISSUED"
    assert re.fullmatch(r"[A-Z]{2}[0-9]{8}", issued["invoice_number"])
    assert client.get("/orders/MISSING/invoice").status_code == 404


def test_einv_007_temporary_failures_stay_pending_with_attempts_and_last_error(book, pay, invoice_of, retry, provider):
    provider.queue("9001")
    provider.queue("DOWN")
    provider.queue("0000", latency_seconds=4)
    order = pay(book())
    assert (invoice_of(order["order_id"])["attempts"], invoice_of(order["order_id"])["last_error"]) == (1, "9001")
    assert (retry(order["order_id"])["attempts"], invoice_of(order["order_id"])["last_error"]) == (2, "CONNECTION_FAILED")
    third = retry(order["order_id"])
    assert (third["status"], third["attempts"], third["last_error"]) == ("PENDING", 3, "TIMEOUT")
    assert retry(order["order_id"])["status"] == "ISSUED"
    assert {p["merchant_order_no"] for p in provider.received} == {order["order_id"]}


@pytest.mark.parametrize("latency, status", [(3, "ISSUED"), (3.5, "PENDING")])
def test_einv_007_a_call_times_out_after_3_seconds(book, pay, invoice_of, provider, latency, status):
    provider.queue("0000", latency_seconds=latency)
    order = pay(book())
    assert invoice_of(order["order_id"])["status"] == status


def test_einv_008_fifth_failed_call_fails_the_invoice_and_stops_retrying(book, pay, invoice_of, retry, provider):
    for _ in range(5):
        provider.queue("9001")
    order = pay(book())
    for _ in range(3):
        retry(order["order_id"])
    assert (invoice_of(order["order_id"])["status"], invoice_of(order["order_id"])["attempts"]) == ("PENDING", 4)
    assert retry(order["order_id"])["status"] == "FAILED"
    after = retry(order["order_id"])
    assert (after["status"], after["attempts"]) == ("FAILED", 5)
    assert len(provider.received) == 5


@pytest.mark.parametrize("code", ["1001", "1002"])
def test_einv_009_permanent_failure_fails_immediately_without_retry(book, pay, invoice_of, retry, provider, code):
    provider.queue(code)
    order = pay(book())
    invoice = invoice_of(order["order_id"])
    assert (invoice["status"], invoice["attempts"], invoice["last_error"]) == ("FAILED", 1, code)
    assert retry(order["order_id"])["status"] == "FAILED"
    assert len(provider.received) == 1


def test_einv_010_duplicate_answer_2001_marks_issued_with_original_number(book, pay, retry, provider):
    provider.queue("0000", latency_seconds=5)                # issued at the provider, answer lost
    order = pay(book())
    original = provider.issued[order["order_id"]]
    invoice = retry(order["order_id"])
    assert (invoice["status"], invoice["invoice_number"]) == ("ISSUED", original)


def test_einv_011_issued_invoice_is_never_reissued_or_renumbered(book, pay, invoice_of, retry, provider):
    order = pay(book())
    issued = invoice_of(order["order_id"])
    assert retry(order["order_id"]) == issued
    assert len(provider.received) == 1
    invoice = dependencies.store.invoices[order["order_id"]]
    invoice.record(IssueResult(IssueOutcome.ISSUED, invoice_number="ZZ99999999"))   # a late answer
    assert invoice.invoice_number == issued["invoice_number"]


@pytest.mark.parametrize("invoice, expected, absent", [
    ({"business_id": "12345678", "company_name": "Acme Ltd"},
     {"buyer_ban": "12345678", "buyer_name": "Acme Ltd"}, {"carrier_type", "carrier_id"}),
    ({"mobile_barcode": "/AB+.-12"},
     {"carrier_type": "MOBILE_BARCODE", "carrier_id": "/AB+.-12"}, {"buyer_ban", "buyer_name"}),
    (None, {}, {"buyer_ban", "buyer_name", "carrier_type", "carrier_id"}),
])
def test_einv_012_optional_business_id_or_mobile_barcode(book, pay, provider, invoice, expected, absent):
    pay(book(), invoice)
    payload = provider.received[0]
    assert expected.items() <= payload.items()
    assert not absent & payload.keys()


@pytest.mark.parametrize("invoice", [
    {"business_id": "1234567", "company_name": "Acme"},
    {"business_id": "1234567A", "company_name": "Acme"},
    {"business_id": "12345678"},
    {"mobile_barcode": "/abc1234"},
    {"mobile_barcode": "/ABC123"},
    {"mobile_barcode": "ABC12345"},
    {"business_id": "12345678", "company_name": "Acme", "mobile_barcode": "/ABC1234"},
])
def test_einv_013_invalid_invoice_info_rejects_payment_before_charging(book, pay, provider, memory_store, monkeypatch, invoice):
    charges = []
    monkeypatch.setattr(dependencies.gateway, "charge", lambda *args: charges.append(args))
    booking = book()
    response = pay(booking, invoice, expected=422)
    assert response["error"]["code"] == "INVALID_INVOICE_INFO"
    assert memory_store.bookings[booking["booking_id"]].status == BookingStatus.PENDING_PAYMENT
    assert not memory_store.orders and not charges and not provider.received


def test_einv_014_issued_and_failed_are_audited_pending_is_silent(client, book, pay, retry, provider):
    def events(booking, kind):
        return [(e["event"], e.get("detail")) for e in client.get(f"/bookings/{booking['booking_id']}/{kind}").json()
                if e["event"].startswith("INVOICE")]
    issued = book()
    provider.queue("9001")
    order = pay(issued)
    assert events(issued, "audit-log") == [] and events(issued, "notifications") == []   # PENDING: quiet
    number = retry(order["order_id"])["invoice_number"]
    assert events(issued, "audit-log") == [("INVOICE_ISSUED", number)]
    assert events(issued, "notifications") == [("INVOICE_ISSUED", None)]
    failed = book()
    provider.queue("1002")
    pay(failed)
    [(event, detail)] = events(failed, "audit-log")
    assert event == "INVOICE_FAILED" and "1002" in detail
    assert events(failed, "notifications") == []


REQUEST = InvoiceRequest("O1", date(2030, 1, 14), InvoiceBuyer(), InvoiceLine("台北-台中 車票", 1, 700, 700), 667, 33, 700)


@pytest.mark.parametrize("code, latency, outcome, detail", [
    ("0000", 0, IssueOutcome.ISSUED, None),
    ("1001", 0, IssueOutcome.REJECTED, "1001"),
    ("1002", 0, IssueOutcome.REJECTED, "1002"),
    ("9001", 0, IssueOutcome.UNAVAILABLE, "9001"),
    ("DOWN", 0, IssueOutcome.UNAVAILABLE, "CONNECTION_FAILED"),
    ("9001", 4, IssueOutcome.UNAVAILABLE, "TIMEOUT"),
])
def test_einv_015_adapter_maps_every_simulated_provider_answer(code, latency, outcome, detail):
    transport = SimulatedEInvoiceProvider()
    transport.queue(code, latency)
    result = EInvoiceProviderAdapter(transport).issue(REQUEST)
    assert result.outcome is outcome
    assert (result.error if outcome is not IssueOutcome.ISSUED else None) == detail


def test_einv_015_adapter_maps_2001_to_the_original_invoice_number():
    transport = SimulatedEInvoiceProvider()
    first = EInvoiceProviderAdapter(transport).issue(REQUEST)
    again = EInvoiceProviderAdapter(transport).issue(REQUEST)
    assert again == IssueResult(IssueOutcome.ISSUED, invoice_number=first.invoice_number)


def test_einv_015_application_uses_the_simulated_provider_only():
    assert type(dependencies.invoicing_service.issuer.transport) is SimulatedEInvoiceProvider

"""Run the plugin's counterfactual for every new D3a rule and save the JSON output."""
import json
import subprocess
import sys
from pathlib import Path

# Usage (from anywhere):
#   py -3.13 -X utf8 evidence/run_counterfactuals.py <path-to-venv-python.exe> <path-to-domain-memory/scripts/registry_tools.py> [case ...]
# Optional case names run only those cases (default: all).
# Paths passed to cmd.exe must be absolute Windows paths (see the spike report's Windows pitfalls).
PY, TOOL = (str(Path(arg).resolve()) for arg in sys.argv[1:3])
REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "evidence" / "counterfactual"
DOMAIN = r"src\smart_ticket\domain\invoicing.py"
ADAPTER = r"src\smart_ticket\infrastructure\einvoice_provider.py"
SERVICE = r"src\smart_ticket\application\invoicing_service.py"
PAYMENT = r"src\smart_ticket\application\payment_service.py"
T = r"tests\integration\test_e_invoice.py"

def test(k):
    return f'"{PY}" -X utf8 -m pytest -q -p no:cacheprovider {T} -k "{k}"'

CASES = [
    ("invoice-issued-after-payment", "EINV-001", PAYMENT, "self.invoicing.issue(order.order_id)", "pass", "einv_001"),
    ("group-whole-booking-one-invoice-line", "EINV-001", DOMAIN, 'InvoiceLine(f"{origin}-{destination} 車票", passenger_count,',
     'InvoiceLine(f"{origin}-{destination} 車票", 1,', "einv_001"),
    ("status-values-queryable", "EINV-006", DOMAIN, 'PENDING = "PENDING"', 'PENDING = "WAITING"', "einv_006"),
    ("unknown-order-invoice-404", "EINV-006", SERVICE, '"Invoice not found", 404)', '"Invoice not found", 400)', "einv_006"),
    ("vat-rate", "EINV-003", DOMAIN, "VAT_RATE_PERCENT = 5 ", "VAT_RATE_PERCENT = 6 ", "einv_003"),
    ("vat-half-up-rounding", "EINV-003", DOMAIN, "if remainder * 2 >= gross_percent:", "if remainder >= gross_percent:", "einv_003"),
    ("unit-price-floor", "EINV-004", DOMAIN, "order_amount // passenger_count", "-(-order_amount // passenger_count)", "einv_004"),
    # survived until the 3-passenger case (1,925 / 3) was added: 1,225 / 2 rounds to 612 under banker's rounding
    ("unit-price-floor-vs-round", "EINV-004", DOMAIN, "order_amount // passenger_count", "round(order_amount / passenger_count)", "einv_004"),
    ("retry-cap-number", "EINV-008", DOMAIN, "MAX_ISSUE_ATTEMPTS = 5 ", "MAX_ISSUE_ATTEMPTS = 6 ", "einv_008"),
    ("retry-cap-comparison", "EINV-008", DOMAIN, "self.attempts >= MAX_ISSUE_ATTEMPTS", "self.attempts > MAX_ISSUE_ATTEMPTS", "einv_008"),
    ("permanent-failure-no-retry", "EINV-009", DOMAIN, "result.outcome is IssueOutcome.REJECTED or ", "", "einv_009"),
    ("timeout-3-seconds", "EINV-007", ADAPTER, "CALL_TIMEOUT_SECONDS = 3", "CALL_TIMEOUT_SECONDS = 4", "einv_007"),
    ("idempotency-merchant-order-no", "EINV-005", ADAPTER, '"merchant_order_no": request.order_id,',
     '"merchant_order_no": __import__("uuid").uuid4().hex,', "einv_005"),
    ("duplicate-2001-is-issued", "EINV-010", ADAPTER, 'ISSUED_CODES = {"0000", "2001"}', 'ISSUED_CODES = {"0000"}', "einv_010"),
    ("issued-not-resent", "EINV-011", SERVICE, "if invoice.status is not InvoiceStatus.PENDING:", "if False:", "einv_011"),
    ("issued-number-immutable", "EINV-011", DOMAIN, "if self.status is not InvoiceStatus.PENDING:", "if False:", "einv_011"),
    ("failure-isolation-timeout", "EINV-002", ADAPTER, "except (TimeoutError, ConnectionError) as error:",
     "except (ConnectionError,) as error:", "einv_002"),
    ("failure-isolation-busy-is-an-outcome", "EINV-002", ADAPTER,
     "return IssueResult(IssueOutcome.UNAVAILABLE, error=code)", "raise RuntimeError(code)", "einv_002"),
    ("no-provider-call-under-lock", "EINV-002", SERVICE, "result = self.issuer.issue(invoice.request)",
     "with self.store.lock: result = self.issuer.issue(invoice.request)", "outside_the_store_lock"),
    ("validation-business-id-8-digits", "EINV-013", DOMAIN, 'r"[0-9]{8}"', 'r"[0-9]{7,8}"', "einv_013"),
    ("validation-mobile-barcode", "EINV-013", DOMAIN, 'r"/[0-9A-Z.+\\-]{7}"', 'r"/[0-9A-Za-z.+\\-]{6,7}"', "einv_013"),
    ("validation-either-not-both", "EINV-013", DOMAIN,
     "if self.business_id is not None and self.mobile_barcode is not None:", "if False:", "einv_013"),
    ("validation-company-name-required", "EINV-013", DOMAIN,
     "if self.business_id is not None and not self.company_name:", "if False:", "einv_013"),
    ("audit-failed-with-code", "EINV-014", SERVICE, 'f"error={invoice.last_error} attempts={invoice.attempts}"',
     'f"attempts={invoice.attempts}"', "einv_014"),
    ("notify-issued", "EINV-014", SERVICE, 'self.notifications.record(invoice.booking_id, "INVOICE_ISSUED")',
     "None", "einv_014"),
]

OUT.mkdir(parents=True, exist_ok=True)
rows = []
ONLY = set(sys.argv[3:])
for name, ac, file, find, replace, k in CASES:
    if ONLY and name not in ONLY:
        continue
    proc = subprocess.run([sys.executable, "-X", "utf8", TOOL, "counterfactual", "--repo-root", str(REPO),
                           "--file", file, "--find", find, "--replace", replace,
                           "--test-command", test(k), "--timeout", "120"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError:
        result = {"raw_stdout": proc.stdout, "stderr": proc.stderr}
    result["rule"], result["acceptance_criterion"], result["exit_code"] = name, ac, proc.returncode
    (OUT / f"{name}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    rows.append((ac, name, result.get("verdict", "?"), proc.returncode))
    print(ac, name, result.get("verdict"), proc.returncode, proc.stderr[-300:] if proc.returncode else "")
print(sum(r[2] == "killed" for r in rows), "/", len(rows), "killed")

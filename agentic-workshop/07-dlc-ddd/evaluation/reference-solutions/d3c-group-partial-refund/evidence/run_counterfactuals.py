"""Run the plugin's counterfactual for every new D3c rule and save the JSON output."""
import json
import subprocess
import sys
from pathlib import Path

# Usage (from anywhere):
#   py -3.13 -X utf8 evidence/run_counterfactuals.py <path-to-venv-python.exe> <path-to-domain-memory/scripts/registry_tools.py>
# Paths passed to cmd.exe must be absolute Windows paths (see the spike report's Windows pitfalls).
PY, TOOL = (str(Path(arg).resolve()) for arg in sys.argv[1:3])
REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "evidence" / "counterfactual"
MODELS = r"src\smart_ticket\domain\models.py"
CANCELLATION = r"src\smart_ticket\domain\cancellation.py"
REFUND_SVC = r"src\smart_ticket\application\refund_service.py"
SEAT_SVC = r"src\smart_ticket\application\seat_service.py"
CONTRACTS = r"src\smart_ticket\schemas\contracts.py"
T = r"tests\integration\test_partial_cancellation.py"
NL = "\n"   # the files mutated here use LF (untouched application files keep d3b's CRLF)


def test(k):
    return f'"{PY}" -X utf8 -m pytest -q -p no:cacheprovider {T} -k "{k}"'


DECIDE = "cancellation = booking.cancel_passengers(passenger_ids, (departure - self.store.clock.today).days)"
RELEASE = "self.seats.release_passengers(booking_id, booking.trip_id, cancellation.passenger_ids)"
NOTIFY = 'self.notifications.record(booking_id, "PASSENGERS_CANCELLED")'
LOCKED = f"with self.store.lock:{NL}            booking = BookingService(self.store, FarePolicy()).get(booking_id){NL}            departure"
UNLOCKED = f"if True:{NL}            booking = BookingService(self.store, FarePolicy()).get(booking_id){NL}            departure"

CASES = [
    ("group-only", "PCR-001", MODELS, 'if self.booking_type != "GROUP" or self.redeemed_points:',
     "if self.redeemed_points:", "pcr_001"),
    ("points-excluded", "PCR-001", MODELS, 'if self.booking_type != "GROUP" or self.redeemed_points:',
     'if self.booking_type != "GROUP":', "pcr_001"),
    ("paid-only", "PCR-001", MODELS, "if self.status != BookingStatus.PAID:", "if False:", "pcr_001"),
    ("empty-list-422", "PCR-002", MODELS, "if not passenger_ids or len(set(passenger_ids))",
     "if len(set(passenger_ids))", "pcr_002"),
    ("duplicate-ids-422", "PCR-002", MODELS,
     "if not passenger_ids or len(set(passenger_ids)) != len(passenger_ids):", "if not passenger_ids:", "pcr_002"),
    ("passenger-not-found", "PCR-002", MODELS, "if passenger_id not in active:", "if False:", "pcr_002"),
    ("already-cancelled", "PCR-002", MODELS, "if passenger_id in self.cancelled_passenger_ids:", "if False:", "pcr_002"),
    ("window-closes-at-d0", "PCR-003", CANCELLATION, "((14, 10), (7, 20), (1, 30))", "((14, 10), (7, 20), (0, 30))", "pcr_003"),
    ("band-14-days", "PCR-004", CANCELLATION, "((14, 10), (7, 20), (1, 30))", "((15, 10), (7, 20), (1, 30))", "pcr_004"),
    ("band-7-days", "PCR-004", CANCELLATION, "((14, 10), (7, 20), (1, 30))", "((14, 10), (8, 20), (1, 30))", "pcr_004"),
    ("rate-10", "PCR-004", CANCELLATION, "((14, 10), (7, 20), (1, 30))", "((14, 11), (7, 20), (1, 30))", "pcr_004"),
    ("rate-20", "PCR-004", CANCELLATION, "((14, 10), (7, 20), (1, 30))", "((14, 10), (7, 21), (1, 30))", "pcr_004"),
    ("rate-30", "PCR-004", CANCELLATION, "((14, 10), (7, 20), (1, 30))", "((14, 10), (7, 20), (1, 31))", "pcr_004"),
    ("band-inclusive", "PCR-004", CANCELLATION, "if days_before_departure >= min_days:",
     "if days_before_departure > min_days:", "pcr_004"),
    ("fee-floor-vs-round", "PCR-004", CANCELLATION, "return fare * percent // 100",
     "return round(fare * percent / 100)", "pcr_004"),
    ("fee-per-passenger", "PCR-004", MODELS, "fee = sum(cancellation_fee(fare, percent) for fare in fares)",
     "fee = cancellation_fee(sum(fares), percent)", "pcr_004"),
    ("fee-on-own-fare", "PCR-004", MODELS,
     "fares = [line.amount for line in self.applied_discounts if line.passenger_id in passenger_ids]",
     "fares = [self.total_fare // len(self.passengers)] * len(passenger_ids)", "pcr_004"),
    ("days-off-by-one", "PCR-004", REFUND_SVC, "(departure - self.store.clock.today).days)",
     "(departure - self.store.clock.today).days + 1)", "pcr_003 or pcr_004"),
    # equivalent under the seed: the Clock reads 09:00 and every trip departs 09:00, so whole days agree
    ("days-by-datetime-EQUIVALENT-survived", "PCR-004", REFUND_SVC, "(departure - self.store.clock.today).days)",
     "(self.store.trips[booking.trip_id].departure_time - self.store.clock.now()).days)", "pcr_"),
    ("all-or-at-least-min", "PCR-005", MODELS, "if 0 < len(active) - len(passenger_ids) < MIN_GROUP_SIZE:",
     "if len(active) - len(passenger_ids) < MIN_GROUP_SIZE:", "pcr_005"),
    ("min-group-size", "PCR-005", MODELS, "MIN_GROUP_SIZE = 5 ", "MIN_GROUP_SIZE = 4 ", "pcr_005"),
    ("global-lock", "PCR-005", REFUND_SVC, LOCKED, UNLOCKED, "pcr_005"),
    ("inventory-keeps-others", "PCR-006", SEAT_SVC,
     "kept = [item for item in assignments if item.passenger_id not in passenger_ids]", "kept = []", "pcr_006"),
    ("trip-counter", "PCR-006", SEAT_SVC, "available_seats += len(assignments) - len(kept)",
     "available_seats += 0", "pcr_006"),
    ("release-called", "PCR-006", REFUND_SVC, RELEASE, "None", "pcr_006"),
    ("booking-drops-seats", "PCR-006", MODELS,
     "self.assigned_seats = [seat for seat in self.assigned_seats if seat.passenger_id not in passenger_ids]",
     "self.assigned_seats = self.assigned_seats", "pcr_006"),
    ("append-not-overwrite", "PCR-007", REFUND_SVC,
     f'self.store.refunds.append(record){NL}            self.audit.record(booking_id, "PASSENGERS_CANCELLED"',
     f'self.store.refunds[:] = [record]{NL}            self.audit.record(booking_id, "PASSENGERS_CANCELLED"', "pcr_007"),
    ("refund-is-fare-minus-fee", "PCR-008", MODELS, "PassengerCancellation(list(passenger_ids), fee, sum(fares) - fee)",
     "PassengerCancellation(list(passenger_ids), fee, sum(fares) * (100 - percent) // 100)", "pcr_004 or pcr_008"),
    ("whole-refund-cancels-everyone", "PCR-008", MODELS, "self.cancelled_passenger_ids = self.active_passenger_ids",
     "self.cancelled_passenger_ids = []", "pcr_008 or pcr_012"),
    ("refunded-when-none-left", "PCR-009", MODELS, "if not self.active_passenger_ids:", "if False:", "pcr_009"),
    ("paid-while-some-left", "PCR-009", MODELS, "if not self.active_passenger_ids:", "if True:", "pcr_009"),
    ("response-shows-cancelled", "PCR-010", CONTRACTS, "cancelled_passenger_ids: list[str] = []",
     'cancelled_passenger_ids: list[str] = __import__("pydantic").Field(default=[], exclude=True)', "pcr_010"),
    ("refunds-of-this-booking", "PCR-010", REFUND_SVC, "if record.booking_id == booking_id]", "if True]", "pcr_010"),
    ("decide-before-release", "PCR-011", REFUND_SVC, f"{DECIDE}{NL}            {RELEASE}",
     f"self.seats.release_passengers(booking_id, booking.trip_id, passenger_ids){NL}            {DECIDE}", "pcr_011"),
    ("no-whole-refund-after-partial", "PCR-012", MODELS,
     "if self.status != BookingStatus.PAID or self.cancelled_passenger_ids:", "if self.status != BookingStatus.PAID:",
     "pcr_012"),
    ("audit-detail", "PCR-013", REFUND_SVC,
     'f"passenger_ids={\',\'.join(record.passenger_ids)} refund={record.amount} fee={record.fee}"', '""', "pcr_013"),
    ("notification", "PCR-013", REFUND_SVC, NOTIFY, "None", "pcr_013"),
    ("no-gateway-call", "PCR-014", REFUND_SVC, NOTIFY,
     f'{NOTIFY}; __import__("smart_ticket.api.dependencies", fromlist=["gateway"]).gateway.charge(booking_id, -record.amount)',
     "pcr_014"),
]

OUT.mkdir(parents=True, exist_ok=True)
rows = []
for name, ac, file, find, replace, k in CASES:
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

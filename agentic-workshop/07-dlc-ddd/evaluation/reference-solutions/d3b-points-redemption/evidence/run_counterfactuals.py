"""Run the plugin's counterfactual for every new D3b rule and save the JSON output."""
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
MEMBERS = r"src\smart_ticket\domain\members.py"
MODELS = r"src\smart_ticket\domain\models.py"
MEMBER_SVC = r"src\smart_ticket\application\member_service.py"
BOOKING_SVC = r"src\smart_ticket\application\booking_service.py"
PAYMENT_SVC = r"src\smart_ticket\application\payment_service.py"
REFUND_SVC = r"src\smart_ticket\application\refund_service.py"
CHANGE_SVC = r"src\smart_ticket\application\change_booking_service.py"
T = r"tests\integration\test_points_redemption.py"
NL = "\r\n"   # the application files use CRLF; members.py uses LF

def test(k):
    return f'"{PY}" -X utf8 -m pytest -q -p no:cacheprovider {T} -k "{k}"'

COMMIT = (f"self.members.reserve_points(booking){NL}"
          f"            self.store.bookings[booking.booking_id] = booking{NL}"
          f"            self.seats.reserve(booking.booking_id, trip_id, assignments){NL}")
COMMIT_THEN_RESERVE = (f"self.store.bookings[booking.booking_id] = booking{NL}"
                       f"            self.seats.reserve(booking.booking_id, trip_id, assignments){NL}"
                       f"            self.members.reserve_points(booking){NL}")

CASES = [
    ("zero-means-not-used", "PTS-001", MEMBER_SVC,
     f"        if not booking.redeemed_points:{NL}            return{NL}        if booking.member_id is None:",
     "        if booking.member_id is None:", "pts_001"),
    ("member-required", "PTS-002", MEMBER_SVC, "if booking.member_id is None:", "if False:", "pts_002"),
    ("min-check-blocks-negative", "PTS-003", MEMBERS, "points < MIN_REDEMPTION_POINTS or ", "", "pts_003"),
    ("min-points-number", "PTS-003", MEMBERS, "MIN_REDEMPTION_POINTS = 100", "MIN_REDEMPTION_POINTS = 200", "pts_003 or pts_007"),
    # equivalent: any positive multiple of 100 is already >= 100, so the minimum only has to reject <= 0
    ("min-points-1-EQUIVALENT-survived", "PTS-003", MEMBERS, "MIN_REDEMPTION_POINTS = 100", "MIN_REDEMPTION_POINTS = 1", "pts_"),
    ("unit-100", "PTS-003", MEMBERS, "REDEMPTION_UNIT_POINTS = 100", "REDEMPTION_UNIT_POINTS = 50", "pts_003"),
    ("balance-check", "PTS-004", MEMBERS, "if points > self.points_balance:", "if False:", "pts_004"),
    ("cap-percent", "PTS-005", MEMBERS, "MAX_REDEMPTION_PERCENT = 30 ", "MAX_REDEMPTION_PERCENT = 31 ", "pts_005"),
    ("cap-floor-vs-round", "PTS-005", MEMBERS, "return total_fare * MAX_REDEMPTION_PERCENT // 100",
     "return round(total_fare * MAX_REDEMPTION_PERCENT / 100)", "pts_005"),
    ("cap-inclusive", "PTS-005", MEMBERS, "points_value(points) > redemption_cap(total_fare)",
     "points_value(points) >= redemption_cap(total_fare)", "pts_005"),
    ("cap-on-discounted-total", "PTS-006", MEMBER_SVC, "reserve_points(booking.redeemed_points, booking.total_fare)",
     "reserve_points(booking.redeemed_points, len(booking.passengers) * self.store.trips[booking.trip_id].base_fare)",
     "pts_005 or pts_006"),
    ("point-value", "PTS-007", MEMBERS, "POINT_VALUE_TWD = 1 ", "POINT_VALUE_TWD = 2 ", "pts_007"),
    ("payable-is-total-minus-points", "PTS-007", MODELS, "return self.total_fare - points_value(self.redeemed_points)",
     "return self.total_fare", "pts_007"),
    ("reserve-before-commit", "PTS-008", BOOKING_SVC, COMMIT, COMMIT_THEN_RESERVE, "pts_008"),
    ("charge-payable", "PTS-009", PAYMENT_SVC, "self.gateway.charge(booking_id, booking.payable_amount)",
     "self.gateway.charge(booking_id, booking.total_fare)", "pts_009"),
    ("order-amount-payable", "PTS-009", PAYMENT_SVC, "Order(str(uuid4()), booking_id, booking.payable_amount, result)",
     "Order(str(uuid4()), booking_id, booking.total_fare, result)", "pts_009"),
    ("group-failure-restores", "PTS-010", PAYMENT_SVC, "self.members.restore_points(booking)", "None", "pts_010"),
    ("individual-failure-keeps", "PTS-011", PAYMENT_SVC, 'raise DomainError("PAYMENT_FAILED", "Payment failed", 409)',
     'self.members.restore_points(booking); raise DomainError("PAYMENT_FAILED", "Payment failed", 409)', "pts_011"),
    ("refund-cash-is-order-amount", "PTS-012", REFUND_SVC, "RefundRecord(str(uuid4()), booking_id, paid.amount)",
     "RefundRecord(str(uuid4()), booking_id, booking.payable_amount)", "pts_012"),
    ("refund-restores-points", "PTS-012", REFUND_SVC, "MemberService(self.store).restore_points(booking)", "None", "pts_012"),
    ("fare-difference-uses-totals", "PTS-013", CHANGE_SVC, "difference = total - booking.total_fare",
     "difference = total - booking.payable_amount", "pts_013"),
    ("global-lock", "PTS-014", BOOKING_SVC, "with self.store.lock:", "if True:", "pts_014"),
    ("audit-reserved-points", "PTS-015", MEMBER_SVC, '"POINTS_RESERVED", f"points={booking.redeemed_points}"',
     '"POINTS_RESERVED", ""', "pts_015"),
    ("audit-restored-points", "PTS-015", MEMBER_SVC, '"POINTS_RESTORED", f"points={booking.redeemed_points}"',
     '"POINTS_RESTORED", ""', "pts_015"),
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

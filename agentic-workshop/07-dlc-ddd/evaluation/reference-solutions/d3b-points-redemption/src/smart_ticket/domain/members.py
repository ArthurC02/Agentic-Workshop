from dataclasses import dataclass
from enum import StrEnum
from smart_ticket.domain.errors import DomainError

# Points redemption terms (requirement card 02). Membership owns them: points are not a
# discount (PTS-006), so Pricing never sees them; Pricing only hands over the discounted total.
POINT_VALUE_TWD = 1           # 1 point = NT$1
MIN_REDEMPTION_POINTS = 100
REDEMPTION_UNIT_POINTS = 100
MAX_REDEMPTION_PERCENT = 30   # of the discounted Booking Total Fare, floored

class MemberType(StrEnum):
    STANDARD = "STANDARD"
    CORPORATE = "CORPORATE"

def points_value(points: int) -> int:
    return points * POINT_VALUE_TWD

def redemption_cap(total_fare: int) -> int:
    """PTS-005: the most one booking may redeem, in NT$."""
    return total_fare * MAX_REDEMPTION_PERCENT // 100

@dataclass
class Member:
    member_id: str
    member_type: MemberType
    points_balance: int = 0

    def reserve_points(self, points: int, total_fare: int) -> None:
        """PTS-003 to PTS-005, PTS-014: the only place the balance goes down, so it never goes negative."""
        if points < MIN_REDEMPTION_POINTS or points % REDEMPTION_UNIT_POINTS:
            raise DomainError("POINTS_INVALID_AMOUNT",
                              f"Redeem at least {MIN_REDEMPTION_POINTS} points, in multiples of {REDEMPTION_UNIT_POINTS}", 409)
        if points > self.points_balance:
            raise DomainError("POINTS_INSUFFICIENT", "Not enough points", 409)
        if points_value(points) > redemption_cap(total_fare):
            raise DomainError("POINTS_EXCEED_LIMIT",
                              f"Points may cover at most {MAX_REDEMPTION_PERCENT}% of the total fare", 409)
        self.points_balance -= points

    def restore_points(self, points: int) -> None:
        self.points_balance += points

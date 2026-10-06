from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from smart_ticket.domain.models import PassengerType
from smart_ticket.domain.members import Member, MemberType
from smart_ticket.domain.fare_policy import FarePolicy, STUDENT_FARE_RATE

class DiscountType(StrEnum):
    CORPORATE = "CORPORATE"
    ADVANCE = "ADVANCE"
    STUDENT = "STUDENT"
    ADULT = "ADULT"

@dataclass
class DiscountResult:
    amount: int
    discount_type: DiscountType
    rate: int

class DiscountPolicy:
    """FARE-007 to FARE-010: best eligible single rate for each passenger."""
    def __init__(self, fare_policy: FarePolicy) -> None:
        self.fare_policy = fare_policy

    def calculate(self, base_fare: int, passenger_type: PassengerType,
                  member: Member | None, today: date, departure_date: date) -> DiscountResult:
        candidates = [(100, DiscountType.ADULT)]
        if passenger_type == PassengerType.STUDENT:
            candidates.append((STUDENT_FARE_RATE, DiscountType.STUDENT))
        if (departure_date - today).days >= 14:
            candidates.append((85, DiscountType.ADVANCE))
        if member is not None and member.member_type == MemberType.CORPORATE:
            candidates.append((95, DiscountType.CORPORATE))
        rate, discount_type = min(candidates, key=lambda candidate: candidate[0])
        return DiscountResult(base_fare * rate // 100, discount_type, rate)

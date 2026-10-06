from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from smart_ticket.domain.models import PassengerType
from smart_ticket.domain.members import Member, MemberType
from smart_ticket.domain.fare_policy import FarePolicy

class DiscountType(StrEnum):
    CORPORATE = "CORPORATE"
    ADVANCE = "ADVANCE"
    STUDENT = "STUDENT"
    ADULT = "ADULT"

@dataclass
class DiscountResult:
    amount: int
    discount_type: DiscountType

class DiscountPolicy:
    """Legacy first-match policy for existing individual booking flows."""
    def __init__(self, fare_policy: FarePolicy) -> None:
        self.fare_policy = fare_policy

    def calculate(self, base_fare: int, passenger_type: PassengerType,
                  member: Member | None, today: date, departure_date: date) -> DiscountResult:
        if member is not None and member.member_type == MemberType.CORPORATE:
            return DiscountResult(base_fare * 95 // 100, DiscountType.CORPORATE)
        if (departure_date - today).days >= 14:
            return DiscountResult(base_fare * 85 // 100, DiscountType.ADVANCE)
        if passenger_type == PassengerType.STUDENT:
            return DiscountResult(self.fare_policy.calculate(base_fare, passenger_type), DiscountType.STUDENT)
        return DiscountResult(self.fare_policy.calculate(base_fare, passenger_type), DiscountType.ADULT)

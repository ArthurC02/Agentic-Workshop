from datetime import date
import pytest

from smart_ticket.domain.discounts import DiscountPolicy
from smart_ticket.domain.fare_policy import FarePolicy
from smart_ticket.domain.models import PassengerType


@pytest.mark.parametrize("passenger_type,member_id,advance,expected_type,rate,amount", [
    (PassengerType.ADULT, None, False, "ADULT", 100, 700),
    (PassengerType.STUDENT, None, False, "STUDENT", 75, 525),
    (PassengerType.ADULT, None, True, "ADVANCE", 85, 595),
    (PassengerType.ADULT, "M002", False, "CORPORATE", 95, 665),
    (PassengerType.STUDENT, None, True, "STUDENT", 75, 525),
    (PassengerType.ADULT, "M002", True, "ADVANCE", 85, 595),
    (PassengerType.STUDENT, "M002", True, "STUDENT", 75, 525),
], ids=["adult", "student", "advance", "corporate", "student-advance", "corporate-advance", "all-three"])
def test_selects_best_single_candidate(passenger_type, member_id, advance, expected_type, rate, amount, memory_store):
    member = memory_store.members[member_id] if member_id else None
    today = date(2030, 1, 1) if advance else date(2030, 1, 14)
    result = DiscountPolicy(FarePolicy()).calculate(700, passenger_type, member, today, date(2030, 1, 15))
    assert result.discount_type == expected_type
    assert result.rate == rate
    assert result.amount == amount == 700 * rate // 100
    assert type(result.amount) is int

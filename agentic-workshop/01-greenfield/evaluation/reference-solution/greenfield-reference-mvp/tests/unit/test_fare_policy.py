from smart_ticket.domain.fare_policy import FarePolicy
from smart_ticket.domain.models import PassengerType


def test_adult_fare_is_full_base_fare():
    assert FarePolicy().calculate(700, PassengerType.ADULT) == 700


def test_student_fare_is_seventy_five_percent():
    assert FarePolicy().calculate(700, PassengerType.STUDENT) == 525


def test_mixed_passenger_fares_sum_as_integers():
    policy = FarePolicy()
    fares = [policy.calculate(700, kind) for kind in (PassengerType.ADULT, PassengerType.STUDENT)]
    assert all(type(fare) is int for fare in fares)
    assert sum(fares) == 1225

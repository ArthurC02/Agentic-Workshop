import pytest
from smart_ticket.domain.fare_policy import FarePolicy
from smart_ticket.domain.models import PassengerType

@pytest.mark.skip(reason="G0 FARE-001: implement adult fare")
def test_adult_fare():
    assert FarePolicy().calculate(700, PassengerType.ADULT) == 700

@pytest.mark.skip(reason="G0 FARE-002: implement student fare")
def test_student_fare():
    assert FarePolicy().calculate(700, PassengerType.STUDENT) == 525

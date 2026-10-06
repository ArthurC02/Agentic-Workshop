from smart_ticket.domain.models import PassengerType

STUDENT_FARE_RATE = 85

class FarePolicy:
    def calculate(self, base_fare: int, passenger_type: PassengerType) -> int:
        """FARE-001, FARE-002, FARE-004: integer fare per passenger."""
        if passenger_type == PassengerType.STUDENT:
            return base_fare * STUDENT_FARE_RATE // 100
        return base_fare

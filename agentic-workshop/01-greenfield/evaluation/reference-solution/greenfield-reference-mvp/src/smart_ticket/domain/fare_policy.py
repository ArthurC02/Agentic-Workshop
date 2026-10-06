from smart_ticket.domain.models import PassengerType

class FarePolicy:
    def calculate(self, base_fare: int, passenger_type: PassengerType) -> int:
        """FARE-001, FARE-002, FARE-004: integer fare per passenger."""
        if passenger_type == PassengerType.STUDENT:
            return base_fare * 75 // 100
        return base_fare

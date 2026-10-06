from smart_ticket.domain.models import PassengerType

class FarePolicy:
    def calculate(self, base_fare: int, passenger_type: PassengerType) -> int:
        # TODO(GREENFIELD, FARE-001, FARE-002, FARE-004): Calculate one passenger fare.
        raise NotImplementedError("Fare policy is not implemented in G0")

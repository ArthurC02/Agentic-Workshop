from dataclasses import dataclass
from smart_ticket.domain.errors import DomainError

# Partial-cancellation terms (requirement card 03). The group Booking applies them to its own
# passengers' fares; Pricing set those fares at sale time and Refund only records the outcome.
# (fewest days before departure, fee percent), checked from the earliest band; D <= 0 is refused.
CANCELLATION_FEE_BANDS = ((14, 10), (7, 20), (1, 30))


def cancellation_fee_percent(days_before_departure: int) -> int:
    """PCR-003, PCR-004: the fee percent on the day the cancellation is requested."""
    for min_days, percent in CANCELLATION_FEE_BANDS:
        if days_before_departure >= min_days:
            return percent
    raise DomainError("REFUND_WINDOW_CLOSED", "Passengers cannot be cancelled on or after the departure date", 409)


def cancellation_fee(fare: int, percent: int) -> int:
    """PCR-004: per passenger, on that passenger's own discounted fare, floored."""
    return fare * percent // 100


@dataclass(frozen=True)
class PassengerCancellation:
    passenger_ids: list[str]
    fee: int
    refund: int

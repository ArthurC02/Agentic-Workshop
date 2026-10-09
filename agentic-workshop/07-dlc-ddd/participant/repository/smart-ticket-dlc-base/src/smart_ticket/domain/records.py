from dataclasses import dataclass
from datetime import datetime

@dataclass
class SeatAssignment:
    booking_id: str
    passenger_id: str
    trip_id: str
    seat_id: str
    carriage_id: str = ""
    row_number: int = 0
    seat_number: int = 0
    position: int = 0

@dataclass
class RefundRecord:
    refund_id: str
    booking_id: str
    amount: int

@dataclass
class NotificationRecord:
    notification_id: str
    booking_id: str
    event: str
    created_at: datetime

@dataclass
class AuditEntry:
    audit_id: str
    booking_id: str
    event: str
    created_at: datetime
    detail: str = ""

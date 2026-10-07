from threading import RLock
from typing import Protocol
from smart_ticket.domain.models import Booking, Order, Trip

class TicketRepositories(Protocol):
    """Small structural boundary for Trip, Booking and Order repositories."""
    trips: dict[str, Trip]
    bookings: dict[str, Booking]
    orders: dict[str, Order]
    lock: RLock

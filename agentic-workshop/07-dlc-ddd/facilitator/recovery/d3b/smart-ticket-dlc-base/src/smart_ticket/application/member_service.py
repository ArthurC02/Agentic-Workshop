from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.members import Member
from smart_ticket.domain.models import Booking
from smart_ticket.infrastructure.store import InMemoryStore
from smart_ticket.application.audit_service import AuditService

class MemberService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def get(self, member_id: str) -> Member:
        member = self.store.members.get(member_id)
        if member is None:
            raise DomainError("MEMBER_NOT_FOUND", "Member not found", 404)
        return member

    def reserve_points(self, booking: Booking) -> None:
        """PTS-002, PTS-008, PTS-015. Call under the store lock as the last refusal before commit."""
        if not booking.redeemed_points:
            return
        if booking.member_id is None:
            raise DomainError("POINTS_MEMBER_REQUIRED", "Redeeming points requires a member", 409)
        self.get(booking.member_id).reserve_points(booking.redeemed_points, booking.total_fare)
        AuditService(self.store).record(booking.booking_id, "POINTS_RESERVED", f"points={booking.redeemed_points}")

    def restore_points(self, booking: Booking) -> None:
        """PTS-010, PTS-012, PTS-015: give back everything this booking reserved."""
        if not booking.redeemed_points:
            return
        self.get(booking.member_id).restore_points(booking.redeemed_points)
        AuditService(self.store).record(booking.booking_id, "POINTS_RESTORED", f"points={booking.redeemed_points}")

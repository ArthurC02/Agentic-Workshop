from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.members import Member
from smart_ticket.infrastructure.store import InMemoryStore

class MemberService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def get(self, member_id: str) -> Member:
        member = self.store.members.get(member_id)
        if member is None:
            raise DomainError("MEMBER_NOT_FOUND", "Member not found", 404)
        return member

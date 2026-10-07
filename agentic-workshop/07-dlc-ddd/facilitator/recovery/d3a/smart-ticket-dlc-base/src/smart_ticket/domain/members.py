from dataclasses import dataclass
from enum import StrEnum

class MemberType(StrEnum):
    STANDARD = "STANDARD"
    CORPORATE = "CORPORATE"

@dataclass
class Member:
    member_id: str
    member_type: MemberType
    points_balance: int = 0

from smart_ticket.application.booking_service import BookingService
from smart_ticket.application.order_service import OrderService
from smart_ticket.application.payment_service import PaymentService
from smart_ticket.application.trip_service import TripService
from smart_ticket.domain.fare_policy import FarePolicy
from smart_ticket.infrastructure.payment_gateway import MockPaymentGateway
from smart_ticket.infrastructure.store import InMemoryStore

store = InMemoryStore()
gateway = MockPaymentGateway()
trip_service = TripService(store)
booking_service = BookingService(store, FarePolicy())
payment_service = PaymentService(store, gateway)
order_service = OrderService(store)

def reset_state() -> None:
    store.reset()
    gateway.reset()

from smart_ticket.application.member_service import MemberService
from smart_ticket.application.change_booking_service import ChangeBookingService
from smart_ticket.application.refund_service import RefundService
from smart_ticket.application.notification_service import NotificationService
from smart_ticket.application.audit_service import AuditService

member_service = MemberService(store)
change_service = ChangeBookingService(store)
refund_service = RefundService(store)
notification_service = NotificationService(store)
audit_service = AuditService(store)

from smart_ticket.application.group_booking_service import GroupBookingService
group_booking_service = GroupBookingService(store)

from fastapi.testclient import TestClient
from smart_ticket.main import app
from smart_ticket.api.dependencies import reset_state, store, gateway
from smart_ticket.domain.models import PaymentStatus

reset_state()
assert [(t.trip_id, t.base_fare, t.available_seats) for t in store.trips.values()] == [
    ('T001', 700, 20), ('T002', 1500, 8), ('T003', 800, 0), ('T004', 1500, 12)]
assert store.trips['T001'].origin == '台北'
assert all(t.arrival_time > t.departure_time for t in store.trips.values())
store.trips['T001'].available_seats = 0
gateway.next_result = PaymentStatus.FAILED
reset_state()
assert store.trips['T001'].available_seats == 20
assert gateway.charge('B001', 700) == PaymentStatus.SUCCESS
with TestClient(app) as client:
    assert client.get('/health').json() == {'status': 'ok'}
    assert client.get('/openapi.json').status_code == 200
    assert '/bookings' in app.openapi()['paths']
    assert client.get('/trips').status_code == 501
    assert client.get('/orders/missing').json()['error']['code'] == 'NOT_IMPLEMENTED'
print('PASS: G0 health/OpenAPI/seed/reset/mock-payment/controlled-501')

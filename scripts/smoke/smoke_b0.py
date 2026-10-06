import sys
from datetime import date
from fastapi.testclient import TestClient
from smart_ticket.main import app
from smart_ticket.api.dependencies import reset_state, store

print(sys.version.split()[0], app.title, app.version)
reset_state()
with TestClient(app) as client:
    assert client.get('/health').json() == {'status': 'ok'}
    assert len(app.openapi()['paths']) == 11
    assert len(client.get('/trips').json()) == 7
    assert client.get('/members/M002').json()['member_type'] == 'CORPORATE'
    body = {'trip_id': 'T001', 'member_id': 'M002', 'passengers': [
        {'passenger_id': 'P1', 'name': 'Smoke Adult', 'passenger_type': 'ADULT'}]}
    response = client.post('/bookings', json=body)
    assert response.status_code == 201
    booking = response.json()
    assert booking['total_fare'] == 665 and len(booking['seat_ids']) == 1
    booking_id = booking['booking_id']
    prefix = '/bookings/' + booking_id
    payment = client.post(prefix + '/pay')
    assert payment.status_code == 200
    order = payment.json()
    assert order['amount'] == 665 and client.get('/orders/' + order['order_id']).json() == order
    changed = client.post(prefix + '/change', json={'target_trip_id': 'T005'})
    assert changed.status_code == 200
    assert changed.json()['fare_difference'] == 47 and changed.json()['total_fare'] == 712
    assert store.trips['T001'].available_seats == 20 and store.trips['T005'].available_seats == 5
    refunded = client.post(prefix + '/refund')
    assert refunded.status_code == 200
    assert client.get(prefix).json()['status'] == 'REFUNDED'
    assert store.trips['T005'].available_seats == 6
    assert [r['event'] for r in client.get(prefix + '/notifications').json()] == [
        'PAYMENT_COMPLETED', 'BOOKING_CHANGED', 'BOOKING_REFUNDED']
    assert [r['event'] for r in client.get(prefix + '/audit-log').json()] == [
        'BOOKING_CREATED', 'PAYMENT_COMPLETED', 'BOOKING_CHANGED', 'BOOKING_REFUNDED']
    assert client.get('/orders/' + order['order_id']).json()['amount'] == 665
    reset_state()
    store.clock.today = date(2030, 1, 1)
    body.pop('member_id')
    advance = client.post('/bookings', json=body)
    assert advance.status_code == 201 and advance.json()['total_fare'] == 595
reset_state()
print('IMPORT HEALTH OPENAPI MEMBER BOOK PAY CHANGE REFUND NOTIFY AUDIT ADVANCE RESET: PASS')

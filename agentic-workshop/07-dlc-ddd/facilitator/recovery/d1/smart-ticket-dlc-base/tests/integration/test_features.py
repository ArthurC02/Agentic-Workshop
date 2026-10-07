from smart_ticket.api.dependencies import gateway
from smart_ticket.domain.models import BookingStatus, PaymentStatus

def payload(count=1, student=False):
    return {'trip_id': 'T001', 'passengers': [
        {'passenger_id': f'P{i}', 'name': f'Passenger {i}',
         'passenger_type': 'STUDENT' if student or i == 1 else 'ADULT'}
        for i in range(count)]}

def error(response, code, status=409):
    assert response.status_code == status
    assert response.json()['error']['code'] == code
    assert isinstance(response.json()['error']['message'], str)

def test_sellable_trips(client):
    response = client.get('/trips')
    assert response.status_code == 200
    assert {t['trip_id'] for t in response.json()} == {'T001', 'T002', 'T004', 'T005', 'T006', 'T007', 'T008'}
    assert all(t['available_seats'] > 0 for t in response.json())

def test_exact_trip_filters(client):
    assert {t['trip_id'] for t in client.get('/trips', params={'origin': '台北'}).json()} == {'T001', 'T002', 'T005', 'T006'}
    assert {t['trip_id'] for t in client.get('/trips', params={'destination': '台中'}).json()} == {'T001', 'T005', 'T008'}
    assert [t['trip_id'] for t in client.get('/trips', params={'origin': '台北', 'destination': '台中'}).json()] == ['T001', 'T005']
    assert client.get('/trips', params={'origin': '台'}).json() == []

def test_empty_trip_query(client):
    response = client.get('/trips', params={'destination': 'missing'})
    assert response.status_code == 200 and response.json() == []

def test_adult_booking(client):
    response = client.post('/bookings', json=payload())
    assert response.status_code == 201 and response.json()['total_fare'] == 700
    assert response.json()['passengers'] == payload()['passengers']

def test_student_booking(client):
    response = client.post('/bookings', json=payload(student=True))
    assert response.status_code == 201 and response.json()['total_fare'] == 525

def test_mixed_booking_reserves_seats(client, memory_store):
    response = client.post('/bookings', json=payload(2))
    assert response.status_code == 201
    booking = response.json()
    assert booking['total_fare'] == 1225 and type(booking['total_fare']) is int
    assert booking['status'] == 'PENDING_PAYMENT'
    assert memory_store.trips['T001'].available_seats == 18
    assert client.get('/trips', params={'destination': '台中'}).json()[0]['available_seats'] == 18

def test_zero_passengers_rejected(client, memory_store):
    error(client.post('/bookings', json=payload(0)), 'INVALID_PASSENGER_COUNT')
    assert memory_store.trips['T001'].available_seats == 20 and not memory_store.bookings

def test_more_than_four_rejected(client, memory_store):
    error(client.post('/bookings', json=payload(5)), 'INVALID_PASSENGER_COUNT')
    assert memory_store.trips['T001'].available_seats == 20 and not memory_store.bookings
    assert client.post('/bookings', json=payload(4)).status_code == 201

def test_insufficient_seats_rejected(client, memory_store):
    memory_store.trips['T001'].available_seats = 1
    error(client.post('/bookings', json=payload(2)), 'INSUFFICIENT_SEATS')
    assert memory_store.trips['T001'].available_seats == 1 and not memory_store.bookings
    body = payload()
    body['trip_id'] = 'T003'
    error(client.post('/bookings', json=body), 'INSUFFICIENT_SEATS')
    assert memory_store.trips['T003'].available_seats == 0

def test_missing_resources(client, memory_store):
    body = payload()
    body['trip_id'] = 'missing'
    error(client.post('/bookings', json=body), 'TRIP_NOT_FOUND', 404)
    error(client.post('/bookings/missing/pay'), 'BOOKING_NOT_FOUND', 404)
    error(client.get('/orders/missing'), 'ORDER_NOT_FOUND', 404)
    assert memory_store.trips['T001'].available_seats == 20 and not memory_store.bookings

def test_happy_path_and_paid_order_query(client, memory_store):
    assert client.get('/health').json() == {'status': 'ok'}
    assert client.get('/trips').status_code == 200
    booking = client.post('/bookings', json=payload()).json()
    response = client.post('/bookings/' + booking['booking_id'] + '/pay')
    assert response.status_code == 200
    order = response.json()
    assert order['booking_id'] == booking['booking_id']
    assert order['amount'] == booking['total_fare'] == 700
    assert order['payment_status'] == 'SUCCESS'
    assert memory_store.bookings[booking['booking_id']].status == BookingStatus.PAID
    assert len(memory_store.orders) == 1
    queried = client.get('/orders/' + order['order_id'])
    assert queried.status_code == 200 and queried.json() == order

def test_payment_then_duplicate_rejected(client, memory_store):
    booking_id = client.post('/bookings', json=payload()).json()['booking_id']
    assert client.post('/bookings/' + booking_id + '/pay').status_code == 200
    error(client.post('/bookings/' + booking_id + '/pay'), 'BOOKING_NOT_PAYABLE')
    assert len(memory_store.orders) == 1

def test_failed_payment_preserves_pending(client, memory_store):
    booking_id = client.post('/bookings', json=payload()).json()['booking_id']
    gateway.next_result = PaymentStatus.FAILED
    error(client.post('/bookings/' + booking_id + '/pay'), 'PAYMENT_FAILED')
    assert not memory_store.orders
    assert memory_store.bookings[booking_id].status == BookingStatus.PENDING_PAYMENT
    assert memory_store.trips['T001'].available_seats == 19
    gateway.next_result = PaymentStatus.SUCCESS
    assert client.post('/bookings/' + booking_id + '/pay').status_code == 200

def test_request_validation(client, memory_store):
    body = payload()
    body['passengers'][0]['passenger_type'] = 'UNKNOWN'
    assert client.post('/bookings', json=body).status_code == 422
    assert not memory_store.bookings and memory_store.trips['T001'].available_seats == 20

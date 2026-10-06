from datetime import date
from pathlib import Path
import runpy
from fastapi.testclient import TestClient
from smart_ticket.api.dependencies import reset_state, store
from smart_ticket.main import app

assert app.version == 'B1'
reset_state()
with TestClient(app) as client:
    student = {'passenger_id': 'S1', 'name': 'Student', 'passenger_type': 'STUDENT'}
    adult = {'passenger_id': 'A1', 'name': 'Adult', 'passenger_type': 'ADULT'}
    body = {'trip_id': 'T001', 'passengers': [student]}
    response = client.post('/bookings', json=body)
    assert response.status_code == 201 and response.json()['total_fare'] == 525
    mixed = client.post('/bookings', json={'trip_id': 'T001', 'passengers': [adult, student]})
    assert mixed.status_code == 201 and mixed.json()['total_fare'] == 1225
    booking_id = mixed.json()['booking_id']
    paid = client.post('/bookings/' + booking_id + '/pay')
    assert paid.status_code == 200 and paid.json()['amount'] == 1225
    assert client.get('/orders/' + paid.json()['order_id']).json() == paid.json()
    corporate_student = client.post('/bookings', json={**body, 'member_id': 'M002'})
    assert corporate_student.status_code == 201 and corporate_student.json()['total_fare'] == 665
    store.clock.today = date(2030, 1, 1)
    advance_student = client.post('/bookings', json=body)
    assert advance_student.status_code == 201 and advance_student.json()['total_fare'] == 595
reset_state()
print('B1 STUDENT 525 MIXED 1225 ORDER AND UNCHANGED FIRST-MATCH: PASS')
runpy.run_path(str(Path(__file__).with_name('smoke_b0.py')), run_name='__main__')

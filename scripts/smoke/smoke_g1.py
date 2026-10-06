import sys
from pathlib import Path
from fastapi.testclient import TestClient
from smart_ticket.main import app
from smart_ticket.api.dependencies import reset_state, store

print(sys.version.split()[0], app.title, app.version)
reset_state()
with TestClient(app) as client:
    assert client.get('/health').json() == {'status': 'ok'}
    assert all(p in app.openapi()['paths'] for p in ['/health', '/trips', '/bookings', '/bookings/{booking_id}/pay', '/orders/{order_id}'])
    assert len(client.get('/trips').json()) == 3
    response = client.post('/bookings', json={'trip_id': 'T001', 'passengers': [{'passenger_id': 'P1', 'name': 'Demo', 'passenger_type': 'STUDENT'}]})
    assert response.status_code == 201
    booking = response.json()
    assert booking['total_fare'] == 525
    paid = client.post('/bookings/' + booking['booking_id'] + '/pay')
    assert paid.status_code == 200
    order = paid.json()
    assert client.get('/orders/' + order['order_id']).json() == order
reset_state()
assert store.trips['T001'].available_seats == 20 and not store.bookings and not store.orders
print('IMPORT HEALTH OPENAPI E2E RESET: PASS')
root = Path.cwd()
participant = root.parent.parent.parent / 'participant'
assert not any(p.name == '.git' for p in participant.rglob('.git'))
for path in participant.rglob('*.md'):
    assert 'reference-solution' not in path.read_text(encoding='utf-8')
print('PARTICIPANT LINKS/HISTORY: PASS')

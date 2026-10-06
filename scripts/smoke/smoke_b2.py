from datetime import date
from fastapi.testclient import TestClient
from smart_ticket.main import app
from smart_ticket.api.dependencies import store, reset_state
client=TestClient(app)
reset_state()
assert client.get('/health').status_code==200
assert len(app.openapi()['paths'])==11
store.clock.today=date(2030,1,1)
payload={'trip_id':'T001','member_id':'M002','passengers':[{'passenger_id':'A','name':'Adult','passenger_type':'ADULT'},{'passenger_id':'S','name':'Student','passenger_type':'STUDENT'}]}
response=client.post('/bookings',json=payload)
assert response.status_code==201,response.text
booking=response.json()
assert booking['total_fare']==1120,booking
assert [d['rate'] for d in booking['applied_discounts']]==[85,75]
assert [d['discount_type'] for d in booking['applied_discounts']]==['ADVANCE','STUDENT']
assert booking['passengers']==payload['passengers']
booking_id=booking['booking_id']
paid=client.post(f'/bookings/{booking_id}/pay')
assert paid.status_code==200,paid.text
changed=client.post(f'/bookings/{booking_id}/change',json={'target_trip_id':'T005'})
assert changed.status_code==200,changed.text
assert changed.json()['total_fare']==1199 and changed.json()['fare_difference']==79
assert sum(d['amount'] for d in changed.json()['applied_discounts'])==1199
assert client.post(f'/bookings/{booking_id}/refund').status_code==200
assert len(client.get(f'/bookings/{booking_id}/notifications').json())==3
assert len(client.get(f'/bookings/{booking_id}/audit-log').json())==4
reset_state()
print('PASS: Health/OpenAPI11, corporate+advance mixed rates85/75 total1120, change1199 delta79, pay/refund/notifications/audit/reset')

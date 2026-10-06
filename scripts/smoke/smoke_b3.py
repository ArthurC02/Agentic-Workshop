from datetime import date
from fastapi.testclient import TestClient
from smart_ticket.main import app
from smart_ticket.api.dependencies import reset_state, store, gateway
from smart_ticket.domain.models import PaymentStatus
reset_state()
assert app.version=='B3'
with TestClient(app) as client:
    assert client.get('/health').json()=={'status':'ok'}
    assert len(app.openapi()['paths'])==13
    store.clock.today=date(2030,1,1)
    passengers=[{'passenger_id':f'P{i}','name':f'Passenger {i}','passenger_type':'STUDENT' if i==0 else 'ADULT'} for i in range(5)]
    body={'trip_id':'T001','member_id':'M002','passengers':passengers}
    response=client.post('/group-bookings',json=body)
    assert response.status_code==201,response.text
    group=response.json()
    assert group['booking_type']=='GROUP' and group['status']=='PENDING_PAYMENT'
    assert group['total_fare']==2905 and [d['rate'] for d in group['applied_discounts']]==[75,85,85,85,85]
    seats=group['assigned_seats']
    assert len(seats)==5 and len({s['carriage_id'] for s in seats})==1
    assert [s['position'] for s in seats]==list(range(seats[0]['position'],seats[0]['position']+5))
    bid=group['booking_id']
    paid=client.post(f'/group-bookings/{bid}/pay')
    assert paid.status_code==200 and paid.json()['amount']==2905,paid.text
    assert client.get('/orders/'+paid.json()['order_id']).json()==paid.json()
    assert client.post(f'/group-bookings/{bid}/pay').status_code==409
    assert len(store.orders)==1
    assert client.post(f'/bookings/{bid}/refund').status_code==200
    assert store.trips['T001'].available_seats==20
    reset_state()
    response=client.post('/group-bookings',json=body)
    bid=response.json()['booking_id']
    gateway.next_result=PaymentStatus.FAILED
    failed=client.post(f'/group-bookings/{bid}/pay')
    assert failed.status_code==409,failed.text
    cancelled=client.get(f'/bookings/{bid}').json()
    assert cancelled['status']=='CANCELLED' and cancelled['seat_ids']==[] and cancelled['assigned_seats']==[]
    assert store.trips['T001'].available_seats==20 and not store.orders and not store.seat_assignments
    assert len(client.get(f'/bookings/{bid}/audit-log').json())==2
    assert len(client.get(f'/bookings/{bid}/notifications').json())==1
reset_state()
print('PASS: B3 Health/OpenAPI13; mixed group2905, same-carriage consecutive5, pay uniqueOrder/refund, fail409 CANCELLED/fullrelease/noOrder/audit2/notify1/reset')

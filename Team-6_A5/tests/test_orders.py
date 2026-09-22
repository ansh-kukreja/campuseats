import pytest
from app import create_app

PAYLOAD={"studentId":"STU-1001","items":[{"itemId":"ITEM-101","quantity":2,"unitPrice":120.0}],"paymentMethod":"CARD"}

def charge(*args): return {"id":"txn_demo"}

@pytest.fixture
def client():
    return create_app(payment_charge=charge).test_client()

def h(key="k1", accept="application/json", client_id="test"):
    return {"Authorization":"Bearer demo-token","Idempotency-Key":key,"Accept":accept,"X-Client-Id":client_id}

def test_create_returns_201_location_and_headers(client):
    r=client.post('/orders',json=PAYLOAD,headers=h())
    assert r.status_code==201
    assert r.headers['Location']=='/orders/1'
    assert r.headers['ETag']
    assert r.headers['Cache-Control']=='private, max-age=60'

def test_idempotent_repeat_returns_original(client):
    a=client.post('/orders',json=PAYLOAD,headers=h('same'))
    b=client.post('/orders',json=PAYLOAD,headers=h('same'))
    assert b.status_code==201 and b.json==a.json and b.headers['Location']==a.headers['Location']

def test_bad_body_problem(client):
    r=client.post('/orders',json={"studentId":"STU-1"},headers=h('bad'))
    assert r.status_code==400
    assert set(r.json)=={'type','title','status','detail'}

def test_unknown_order_404(client):
    r=client.get('/orders/999',headers=h('get404'))
    assert r.status_code==404 and r.json['status']==404

def test_options_allow(client):
    r=client.options('/orders')
    assert r.status_code==204 and r.headers['Allow']=='GET, POST, OPTIONS'

def test_unauthorized(client):
    r=client.get('/orders/1',headers={'Accept':'application/json','X-Client-Id':'unauth'})
    assert r.status_code==401

def test_accept_406(client):
    r=client.get('/orders',headers={'Authorization':'Bearer demo-token','Accept':'application/xml','X-Client-Id':'xml'})
    assert r.status_code==406

def test_conditional_get_304(client):
    r=client.post('/orders',json=PAYLOAD,headers=h('etag'))
    etag=r.headers['ETag']
    g=client.get('/orders/1',headers={**h('etag-get'),'If-None-Match':etag})
    assert g.status_code==304 and g.data==b'' and g.headers['ETag']==etag

def test_if_match_mismatch_412(client):
    client.post('/orders',json=PAYLOAD,headers=h('match'))
    r=client.put('/orders/1',json={'status':'CONFIRMED'},headers={**h('put'),'If-Match':'"wrong"'})
    assert r.status_code==412

def test_cancellation_conflict(client):
    client.post('/orders',json=PAYLOAD,headers=h('cancel'))
    r=client.post('/orders/1/cancellation',headers=h('cancel2'))
    assert r.status_code==200
    r=client.post('/orders/1/cancellation',headers=h('cancel3'))
    assert r.status_code==409

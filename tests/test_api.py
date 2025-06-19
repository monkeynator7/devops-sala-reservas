from app.api import app

def test_reserva_exitosa():
    cliente = app.test_client()
    resp = cliente.post('/reservar', json={
        "sala": "A",
        "hora": "12:00"
    })
    assert resp.status_code == 201
    assert resp.get_json() == {'message': 'Reserva exitosa'}

def test_sala_no_disponible():
    cliente = app.test_client()
    cliente.post('/reservar', json={
        "sala": "A",
        "hora": "10:00"
    })
    
    resp = cliente.post('/reservar', json={
        "sala": "A",
        "hora": "10:00"
    })
    assert resp.status_code == 409
    assert resp.get_json() == {'message': 'Sala no disponible'}
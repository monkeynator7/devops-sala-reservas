from app.reservas import verificar_disponibilidad

def test_sala_disponible():
    reservas = [
        {"sala": "A", "hora": "10:00"},
        {"sala": "B", "hora": "11:00"}
    ]
    nueva_reserva = {"sala": "A", "hora": "12:00"}
    assert verificar_disponibilidad(reservas, nueva_reserva) == True

def test_sala_no_disponible():
    reservas = [
        {"sala": "A", "hora": "10:00"},
        {"sala": "B", "hora": "11:00"}
    ]
    nueva_reserva = {"sala": "A", "hora": "10:00"}
    assert verificar_disponibilidad(reservas, nueva_reserva) == False

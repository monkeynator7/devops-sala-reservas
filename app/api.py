from flask import Flask, request, jsonify
from app.reservas import verificar_disponibilidad

app = Flask(__name__)
reservas = []

@app.route('/reservar', methods=['POST'])
def reservar():
    
    data = request.get_json()
    disponible = verificar_disponibilidad(reservas, data)

    if disponible:
        reservas.append(data)
        return jsonify({'message': 'Reserva exitosa'}), 201
    return jsonify({'message': 'Sala no disponible'}), 409

if __name__ == '__main__':
    app.run(debug=True)
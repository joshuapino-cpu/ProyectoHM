from flask import Flask, request, jsonify
from database import get_connection

app = Flask(__name__)

@app.route('/api/lectura', methods=['POST'])
def recibir_lectura():
    data = request.get_json()

    temperatura = data.get("temperatura")
    humedad = data.get("humedad")

    if temperatura is None or humedad is None:
        return jsonify({"error": "Datos incompletos"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO lecturas (temperatura, humedad) VALUES (%s, %s)"
    cursor.execute(sql, (temperatura, humedad))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Lectura almacenada"}), 200


@app.route('/')
def home():
    return "API funcionando OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

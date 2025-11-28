from flask import Flask, request, jsonify, render_template
from database import get_connection

app = Flask(__name__)

# --- RUTA YA CREADA ---
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


# --- NUEVO: API GET para consultar datos ---
@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT temperatura, humedad, fecha FROM lecturas ORDER BY fecha DESC")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(datos)


# --- NUEVO: Página principal ---
@app.route('/')
def index():
    return render_template("index.html")


# --- NUEVO: Historial en tabla ---
@app.route('/historial')
def historial():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT temperatura, humedad, fecha FROM lecturas ORDER BY fecha DESC")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("historial.html", datos=datos)


# --- NUEVO: Dashboard principal ---
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

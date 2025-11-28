from flask import Flask, request, jsonify, render_template
from database import get_connection
import math

app = Flask(__name__)

# ----------------------
#   ENDPOINT POST
# ----------------------
@app.route('/api/lectura', methods=['POST'])
def recibir_lectura():
    data = request.get_json()

    temperatura = data.get("temperatura")
    humedad = data.get("humedad")

    # Validación de datos vacíos
    if temperatura is None or humedad is None:
        return jsonify({"error": "Datos incompletos"}), 400

    # Validación de datos NUMÉRICOS
    try:
        temperatura = float(temperatura)
        humedad = float(humedad)
    except:
        return jsonify({"error": "Valores no numéricos"}), 400

    # Validación de NaN (muy importante)
    if math.isnan(temperatura) or math.isnan(humedad):
        return jsonify({"error": "Valores inválidos (NaN)"}), 400

    # Guardar en BD
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO lecturas (temperatura, humedad) VALUES (%s, %s)"
    cursor.execute(sql, (temperatura, humedad))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Lectura almacenada"}), 200


# ----------------------
#   ENDPOINT GET DATOS
# ----------------------
@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT temperatura, humedad, fecha FROM lecturas ORDER BY fecha DESC")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(datos)


# ----------------------
#   PÁGINA PRINCIPAL
# ----------------------
@app.route('/')
def index():
    return render_template("index.html")


# ----------------------
#   HISTORIAL
# ----------------------
@app.route('/historial')
def historial():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT temperatura, humedad, fecha FROM lecturas ORDER BY fecha DESC")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("historial.html", datos=datos)


# ----------------------
#   DASHBOARD
# ----------------------
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, request, jsonify, render_template
from database import get_connection
import math

app = Flask(__name__)

# =====================================================================
#   ENDPOINT POST: recibe lecturas del sensor
# =====================================================================
@app.route('/api/lectura', methods=['POST'])
def recibir_lectura():
    data = request.get_json()

    temperatura = data.get("temperatura")
    humedad = data.get("humedad")

    # Validación de datos vacíos
    if temperatura is None or humedad is None:
        return jsonify({"error": "Datos incompletos"}), 400

    # Validación de datos numéricos
    try:
        temperatura = float(temperatura)
        humedad = float(humedad)
    except:
        return jsonify({"error": "Valores no numéricos"}), 400

    # Validación contra NaN
    if math.isnan(temperatura) or math.isnan(humedad):
        return jsonify({"error": "Valores inválidos (NaN)"}), 400

    # Inserción a BD
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO lecturas (temperatura, humedad) VALUES (%s, %s)"
    cursor.execute(sql, (temperatura, humedad))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Lectura almacenada"}), 200


# =====================================================================
#   ENDPOINT GET: devuelve TODAS las lecturas (JSON)
# =====================================================================
@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT temperatura, humedad, fecha FROM lecturas ORDER BY fecha DESC")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(datos)


# =====================================================================
#   INDEX
# =====================================================================
@app.route('/')
def index():
    return render_template("index.html")


# =====================================================================
#   HISTORIAL COMPLETO (HTML)
# =====================================================================
@app.route('/historial')
def historial():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT temperatura, humedad, fecha FROM lecturas ORDER BY fecha DESC")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("historial.html", datos=datos)


# =====================================================================
#   DASHBOARD: última lectura
# =====================================================================
@app.route('/dashboard')
def dashboard():
    conn = get_connection()
    cursor = conn.cursor()

    # Obtener SOLO la lectura más reciente
    cursor.execute("""
        SELECT temperatura, humedad, fecha 
        FROM lecturas 
        ORDER BY fecha DESC 
        LIMIT 1
    """)
    data = cursor.fetchone()

    cursor.close()
    conn.close()

    # Si hay datos
    if data:
        temperatura, humedad, fecha = data
    else:
        temperatura = "—"
        humedad = "—"
        fecha = "Sin datos"

    return render_template(
        "dashboard.html",
        temperatura=temperatura,
        humedad=humedad,
        fecha=fecha
    )


# =====================================================================
#   EJECUCIÓN DEL SERVIDOR
# =====================================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

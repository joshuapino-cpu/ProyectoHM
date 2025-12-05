# =====================================================================
#   IMPORTS Y CONFIGURACIÓN INICIAL
# =====================================================================
from flask import Flask, request, jsonify, render_template, redirect, url_for
from database import get_connection
import math

app = Flask(__name__)


# =====================================================================
#   ENDPOINT POST — recibe datos del sensor y mantiene máximo 20 registros
# =====================================================================
@app.route('/api/lectura', methods=['POST'])
def recibir_lectura():
    data = request.get_json()

    temperatura = data.get("temperatura")
    humedad = data.get("humedad")

    # Validación de campos
    if temperatura is None or humedad is None:
        return jsonify({"error": "Datos incompletos"}), 400

    # Validación numérica
    try:
        temperatura = float(temperatura)
        humedad = float(humedad)
    except:
        return jsonify({"error": "Valores no numéricos"}), 400

    # Validación NaN
    if math.isnan(temperatura) or math.isnan(humedad):
        return jsonify({"error": "Valores inválidos (NaN)"}), 400

    # Guardar en base de datos
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO lecturas (temperatura, humedad) VALUES (%s, %s)",
        (temperatura, humedad)
    )
    conn.commit()

    # Mantener solo los 20 registros más recientes
    cursor.execute("""
        DELETE FROM lecturas
        WHERE id NOT IN (
            SELECT id FROM (
                SELECT id FROM lecturas ORDER BY fecha DESC LIMIT 20
            ) AS t
        );
    """)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Lectura almacenada"}), 200


# =====================================================================
#   ENDPOINT GET — devuelve todos los registros actuales (máx. 20)
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
#   INDEX — Página principal
# =====================================================================
@app.route('/')
def index():
    return render_template("index.html")


# =====================================================================
#   HISTORIAL — tabla con máximo 20 registros + botón borrar BD
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
#   RUTA PARA BORRAR TODA LA BD
# =====================================================================
@app.route('/borrar_todo', methods=['POST'])
def borrar_todo():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM lecturas")
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('historial'))


# =====================================================================
#   DASHBOARD — Última lectura + auto actualización
# =====================================================================
@app.route('/dashboard')
def dashboard():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT temperatura, humedad, fecha
        FROM lecturas
        ORDER BY fecha DESC
        LIMIT 1
    """)

    data = cursor.fetchone()

    cursor.close()
    conn.close()

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

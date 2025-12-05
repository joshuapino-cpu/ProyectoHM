import grovepi
import time
import requests
import math

sensor_port = 7      
sensor_type = 0
url = "http://localhost:5000/api/lectura"

while True:
    try:
        temp, hum = grovepi.dht(sensor_port, sensor_type)

        print("Lectura cruda:", temp, hum)

        # Ignorar None
        if temp is None or hum is None:
            print("Lectura None, saltando...")
            time.sleep(5)
            continue

        # Ignorar NaN
        if math.isnan(temp) or math.isnan(hum):
            print("Lectura NaN, saltando...")
            time.sleep(5)
            continue

        payload = {
            "temperatura": float(temp),
            "humedad": float(hum)
        }

        print("Enviando:", payload)

        try:
            r = requests.post(url, json=payload)
            print("Respuesta API:", r.status_code, r.text)
        except Exception as e:
            print("Error enviando a API:", e)

        time.sleep(3)

    except Exception as e:
        print("Error general:", e)
        time.sleep(5)

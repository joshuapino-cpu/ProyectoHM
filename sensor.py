import grovepi
import time
import requests

sensor_port = 4      
sensor_type = 22        

url = "http://localhost:5000/api/lectura"

while True:
    try:
        temp, hum = grovepi.dht(sensor_port, sensor_type)

        if temp is not None and hum is not None:
            payload = {
                "temperatura": temp,
                "humedad": hum
            }

            try:
                requests.post(url, json=payload)
            except:
                pass

        time.sleep(20)

    except Exception:
        continue

import grovepi
import time
import requests

sensor_port = 7      
sensor_type = 1        

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

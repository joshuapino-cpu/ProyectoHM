import grovepi
import time

sensor_port = 4          # Puerto digital D4 del GrovePi
sensor_type = 22         # 22 = DHT22, 11 = DHT11  (cámbialo si usas DHT11)

# Variables donde se guardarán los datos
temperatura = None
humedad = None

while True:
    try:
        temp, hum = grovepi.dht(sensor_port, sensor_type)

        if temp is not None and hum is not None:
            temperatura = temp
            humedad = hum

        time.sleep(20)

    except Exception:
        pass

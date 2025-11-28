import grovepi
import time

sensor_port = 4      
sensor_type = 22        
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
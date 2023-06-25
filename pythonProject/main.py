import json
import time
import bmp280 as bmp280
import mpu6050
import mqtt
import wifi
from machine import RTC, Pin, I2C

# This template assumes the following file setup
# - main.py
# - mpu6050.py
# - bmp280.py
# - wifi.py
# - mqtt.py
# - cert
#    | - cert.der
#    | - private.der
#    | - wifi_passwords.txt

MQTT_TOPIC = "environment-data"

# construct an I2C bus
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
bmp280 = bmp280.BMP280(i2c)
mpu = mpu6050.accel(i2c)
pir = Pin(0, Pin.IN, Pin.PULL_UP) # enable internal pull-up resistor

def convert_to_iso(datetime):
    y, m, d, _, h, mi, s, _ = datetime
    h += 2  # Füge einen 2-stündigen Versatz hinzu
    if h >= 24:
        h -= 24  # Behandele den Fall, wenn die Stunde größer als 23 ist
        d += 1  # Erhöhe den Tag um 1

    return "{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(y, m, d, h, mi, s)


def measure_environment_data():
    #sensor = DHT11(Pin(5))
    #sensor.measure()
    #return sensor.temperature(), sensor.humidity()
    temp = bmp280.getTemp()
    pres = bmp280.getPress()
    alt = bmp280.getAlti()
    occ = pir.value()
    values = mpu.get_values()  
    gyx = values["GyX"]
    gyy = values["GyY"]
    gyz = values["GyZ"]
    acx = values["AcX"]
    acy = values["AcY"]
    acz = values["AcZ"]

    return temp, pres, alt, occ, gyx, gyy, gyz, acx, acy, acz

def publish_environment_data(mqtt_client):
    data = measure_environment_data()
    iso_timestamp = convert_to_iso(RTC().datetime())

    message = {"temperature": data[0], "pressure": data[1], "altitude": data[2], "occupancy": data[3], "gyx": data[4], "gyy": data[5], "gyz": data[6], "acx": data[7], "acy": data[8], "acz": data[9],"timestamp": iso_timestamp}
    mqtt_client.publish(MQTT_TOPIC, json.dumps(message))


def connect_and_publish():
    print("connect wifi and synchronize RTC")
    wifi.connect()
    wifi.synchronize_rtc()

    print("connect mqtt")
    mqtt_client = mqtt.connect_mqtt()

    print("start publishing data")
    while True:
        try:
            publish_environment_data(mqtt_client)
        except Exception as e:
            print(str(e))
        time.sleep(1)


if __name__ == "__main__":
    connect_and_publish()
from umqtt.robust import MQTTClient

# The certificate and key file need to be converted from PEM to DER format first
#
# $ openssl x509 -in aaaaaaaaa-certificate.pem.crt.txt -out cert.der -outform DER
# $ openssl rsa -in aaaaaaaaaa-private.pem.key -out private.der -outform DER

CERT_FILE = "/cert/certificate.der"
KEY_FILE = "/cert/private.der"
MQTT_CLIENT_ID = "demo-vorlesung"
MQTT_PORT = 8883

MQTT_HOST = "????"


def connect_mqtt():
    try:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
            print("Got Key")

        with open(CERT_FILE, "rb") as f:
            cert = f.read()
            print("Got Cert")

        ssl_params = {"cert": cert, "key": key, "server_side": False}
        mqtt_client = MQTTClient(
            client_id=MQTT_CLIENT_ID,
            server=MQTT_HOST,
            port=MQTT_PORT,
            keepalive=5000,
            ssl=True,
            ssl_params=ssl_params,
        )

        mqtt_client.connect()
        print("MQTT Connected")

        return mqtt_client

    except Exception as e:
        print("Cannot connect MQTT: " + str(e))
        raise

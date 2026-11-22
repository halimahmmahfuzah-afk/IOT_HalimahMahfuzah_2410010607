from datetime import datetime
import json
import random
import time
import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPIC_SENSOR = "iot/sensor"
TOPIC_KONTROL = "iot/kontrol"

lamp_state = "off"


def on_connect(client, userdata, flags, rc):
    print(f"Terhubung ke broker (rc={rc})")
    client.subscribe(TOPIC_KONTROL)


def on_message(client, userdata, msg):
    global lamp_state
    try:
        cmd = json.loads(msg.payload.decode())
        if cmd.get("device") == "lamp":
            lamp_state = cmd.get("action", lamp_state)
            print(f"<- Kontrol diterima: lampu {lamp_state.upper()}")
    except json.JSONDecodeError:
        print(f"<- Pesan tidak valid: {msg.payload}")


# Menambahkan callback_api_version untuk Paho-MQTT v2.0+
client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION1, client_id="ESP32-Simulator"
)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_start()

print("ESP32 Simulator berjalan... Ctrl+C untuk stop")

try:
    while True:
        data = {
            "suhu": round(random.uniform(25, 32), 1),
            "kelembaban": round(random.uniform(55, 80), 1),
            "timestamp": datetime.now().isoformat(),
            "lamp": lamp_state,
        }
        client.publish(TOPIC_SENSOR, json.dumps(data))
        print(f"-> Publish: {data}")
        time.sleep(3)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
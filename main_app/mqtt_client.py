import paho.mqtt.client as mqtt
import json
from main_app.models import WasteBot, SmartBin, Waste
from django.core.management import execute_from_command_line

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe("WasteBots/data")

def on_message(client, userdata, message):
    print(f"Message received: {message.payload}")
    data = json.loads(message.payload)
    wastebot_instance = WasteBot.objects.get(id=data["wastebot_id"])
    smartbin_instance = SmartBin.objects.get(id=1)

    Waste.objects.create(
        waste_type=data["detected_waste"][0]["class"],
        wastebot=wastebot_instance,
        smartbin=smartbin_instance
    )

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt-broker-url", 1883, 60)
client.loop_forever()

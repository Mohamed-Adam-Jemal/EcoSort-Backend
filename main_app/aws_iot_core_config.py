import ssl
import paho.mqtt.client as mqtt
from django.conf import settings
import threading
import json
from main_app.models import WasteBot, Waste, SmartBin

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to AWS IoT Core!")
        client.subscribe(settings.MQTT_CONFIG["topic"])  # Subscribe to the topic
        print(f"Subscribed to topic: {settings.MQTT_CONFIG['topic']}")
    else:
        print(f"Connection failed with code {rc}")

# Callback when a message is received
def on_message(client, userdata, message):
    print(f"Message received on topic {message.topic}: {message.payload}")

    try:
        # Parse the JSON payload
        data = json.loads(message.payload)

        # Retrieve the WasteBot instance using the wastebot_id
        wastebot_instance = WasteBot.objects.get(id=data["wastebot_id"])

        # Retrieve the SmartBin instance using the smartbin_id
        smartbin_instance = SmartBin.objects.get(id=1)

        # Save to database
        Waste.objects.create(
            waste_type=data["detected_waste"][0]["class"],
            wastebot=wastebot_instance,  # Use the actual instance of WasteBot
            smartbin=smartbin_instance  # Use the actual instance of SmartBin
        )
        print("Data saved to the database.")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Configure and run the MQTT client
def run_mqtt_client():
    client = mqtt.Client()
    client.tls_set(
        ca_certs=settings.MQTT_CONFIG["root_ca_file"],
        certfile=settings.MQTT_CONFIG["cert_file"],
        keyfile=settings.MQTT_CONFIG["private_key_file"],
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLSv1_2
    )
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(settings.MQTT_CONFIG["iot_endpoint"], settings.MQTT_CONFIG["port"])

    # Start MQTT client loop in the background
    client.loop_forever()

# This method will be used to start the MQTT client in a background thread
def start_mqtt_in_thread():
    mqtt_thread = threading.Thread(target=run_mqtt_client)
    mqtt_thread.daemon = True  # Ensure the thread will exit when the main program exits
    mqtt_thread.start()

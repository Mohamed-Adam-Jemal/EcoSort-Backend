import ssl
import paho.mqtt.client as mqtt
from django.conf import settings
import threading
import json
from main_app.models import WasteBot, WasteBin, Waste


# To track if the client is already subscribed
is_subscribed = False

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    global is_subscribed

    if rc == 0:
        print("Connected to AWS IoT Core!")

        # Check if already subscribed to avoid double subscription
        if not is_subscribed:
            client.subscribe(settings.MQTT_CONFIG["data_topic"], qos=0)
            is_subscribed = True
            print(f"Subscribed to topic: {settings.MQTT_CONFIG['data_topic']}")
    else:
        print(f"Connection failed with code {rc}")

# Callback when a message is received
def on_message(client, userdata, message):
    print(f"Message received on topic {message.topic}: {message.payload}")

    try:
        # Parse the JSON payload
        data = json.loads(message.payload)

        # Retrieve instances from the database (synchronous ORM)
        wastebot_instance = WasteBot.objects.get(id=data["wastebot_id"])
        smartbin_instance = WasteBin.objects.get(id=1)

        # Save data to the database using async function
        save_waste_data(wastebot_instance, smartbin_instance, data)

        print("Data saved to the database.")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"Error processing message: {e}")

def save_waste_data(wastebot_instance, smartbin_instance, data):
    Waste.objects.create(
        waste_type=data["detected_waste"][0]["class"],
        wastebot=wastebot_instance,
        smartbin=smartbin_instance
    )


def publish_wastebot_status(status):
    """
    Publish ON/OFF command to WasteBot1618/status.
    Args:
        status (str): "ON" or "OFF"
    """
    if status not in ["ON", "OFF"]:
        raise ValueError("Status must be 'ON' or 'OFF'")
    
    if not client:
        raise RuntimeError("MQTT client not initialized. Call init_mqtt() first.")
    
     # Create JSON payload
    payload = json.dumps({"message": status})

    client.publish(
        settings.MQTT_CONFIG["status_topic"],
        payload,
        qos=1,
        retain=False
    )
    print(f"Published status: {status}")

# Configure and run the MQTT client
def run_mqtt_client():
    global client
    client = mqtt.Client(userdata={"subscribed": False})  # Initialize userdata
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

    # Start the MQTT client loop in the background
    client.loop_forever()

mqtt_thread = None

def start_mqtt_in_thread():
    global mqtt_thread
    if mqtt_thread is None or not mqtt_thread.is_alive():
        mqtt_thread = threading.Thread(target=run_mqtt_client)
        mqtt_thread.daemon = True
        mqtt_thread.start()
        print("MQTT client started in background thread.")
    else:
        print("MQTT client is already running.")

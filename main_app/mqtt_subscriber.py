# from django.core.management.base import BaseCommand
# from main_app.aws_iot_core_config import setup_mqtt_client

# class Command(BaseCommand):
#     help = "Subscribes to AWS IoT Core WasteBots data"

#     def handle(self, *args, **kwargs):
#         client = setup_mqtt_client()
#         print("Starting MQTT subscriber...")
#         client.loop_forever()  # Keep the MQTT client running

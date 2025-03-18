from django.apps import AppConfig


class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'

    def ready(self):
        import main_app.signals
        # Start MQTT client in a background thread when Django is ready
        from main_app.aws_iot_core_config import start_mqtt_in_thread
        start_mqtt_in_thread()
        

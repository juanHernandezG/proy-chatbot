# chatbot_app/__init__.py

from django.apps import AppConfig
import firebase_admin
from firebase_admin import credentials

class ChatbotAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatbot_app'

    def ready(self):
        # Inicialización de Firebase cuando la aplicación se carga
        try:
            firebase_admin.get_app()
        except ValueError:
            # Path al archivo JSON de configuración de Firebase
            cred = credentials.Certificate("firebase_config.json")
            firebase_admin.initialize_app(cred)

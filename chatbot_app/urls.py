# chatbot_app/urls.py
from django.urls import path
from .views import chatbot_view
from . import views

urlpatterns = [
    path('', chatbot_view, name='chatbot_view'),
    path('mostrar_instructivo/', views.mostrar_instructivo, name='mostrar_instructivo'),
    path('mostrar_comentarios/', views.mostrar_comentarios, name='mostrar_comentarios'),
    path('guardar_pregunta_no_reconocida/', views.guardar_pregunta_no_reconocida, name='guardar_pregunta_no_reconocida'),
]

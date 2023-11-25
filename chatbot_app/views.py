from django.shortcuts import render

# Create your views here.
# chatbot/views.py
from django.http import JsonResponse
from .chatbot import generate_response  # Importa la función del chatbot


def chatbot_view(request):
    # Mensaje de bienvenida
    welcome_message = "¡Hola! Soy Gastón, tú asistente virtual. ¿En qué puedo ayudarte?"
    
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        chatbot_response = generate_response(user_input)
        return JsonResponse({'response': chatbot_response})

    return render(request, 'chatbot/chatbot.html',{'welcome_message': welcome_message})

def mostrar_instructivo(request):
    return render(request, 'chatbot/instructivo.html')
from django.shortcuts import render

# Create your views here.
# chatbot/views.py
from django.http import JsonResponse
from .chatbot import generate_response  # Importa la función del chatbot
# from .firebase import initialize_firebase

# initialize_firebase()

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

def mostrar_comentarios(request):
    return render(request, 'chatbot/comentarios.html')

# def guardar_comentario(request):
#     if request.method == 'POST':
#         comentario = request.POST.get('comentario')
        
#         #Guardar el comentario en la bdd de firebase
#         db = firestore.client()
#         comentarios_ref = db.collection('Comentarios')
        
#         data = {
#             'comentario': comentario,
#             'fecha': firestore.SERVER_TIMESTAMP
#         }
        
#         comentarios_ref.add(data)
#         # Redireccionar a la página de comentarios o a donde desees
#         return render(request, 'comentarios.html')
#     # Lógica adicional si es una solicitud GET
#     return render(request, 'otra_pagina.html')
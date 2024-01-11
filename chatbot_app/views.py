from django.shortcuts import render

# Create your views here.
# chatbot/views.py
from django.http import JsonResponse
from .chatbot import generate_response  # Importa la función del chatbot
# from .firebase import initialize_firebase
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import random
import json
#initialize_firebase()
import os

def chatbot_view(request):
    # Mensaje de bienvenida
    welcome_message = "¡Hola! Soy Gastón, tú asistente virtual. ¿En qué puedo ayudarte?"
    
    with open('datasetPt.json','r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        all_tags = list(set(intent['tag'] for intent in data['Intents']))  # Obtener todas las etiquetas únicas
        
        suggested_questions = []
        for tag in all_tags:
            if tag not in ["saludosHola","insultos","duda","disculpas","Agradecimiento","Despedida","ComoEstas","ComoEstasMal","Cuentame de ti","como te llamas","cual es tu color favorito","queeEsUnRamo","queEsUnaAsignatura",]:
                patterns_for_tag = [intent['patterns'] for intent in data['Intents'] if intent['tag'] == tag]
                random_pattern = random.choice(patterns_for_tag[0]) if patterns_for_tag else None
                if random_pattern:
                    suggested_questions.append(random_pattern)
            

        suggested_questions = random.sample(suggested_questions, min(3, len(suggested_questions))) 
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        chatbot_response = generate_response(user_input)
        return JsonResponse({'response': chatbot_response, 'suggested_questions': suggested_questions})

    return render(request, 'chatbot/chatbot.html',{
        'welcome_message': welcome_message,
        'suggested_questions':suggested_questions
        })

def mostrar_instructivo(request):
    return render(request, 'chatbot/instructivo.html')

def mostrar_comentarios(request):
    return render(request, 'chatbot/comentarios.html')

def guardar_pregunta_no_reconocida(request):
    if request.method == 'POST':
        try:  
            question = request.POST.get('pregunta', '')
            current_time = datetime.now().isoformat()
            
            #Ruta al archivo miFirebase.json ajustada
            current_dir = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(current_dir, 'miFirebase.json')
            
            cred = credentials.Certificate(file_path)   
            # Verifica si la app de Firebase está inicializada
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)

            
            # Acceder a la colección en Firestore y guardar la pregunta no reconocida
            pregunta_ref = firestore.client().collection('PreguntasNoReconocidas')
            data = {
                'pregunta': question,
                'fecha': current_time, 
            }
            
            pregunta_ref.add(data)
        
            return JsonResponse({'message': 'Pregunta no reconocida guardada en Firebase'})
        except Exception as e:
            print(f'Error interno al guardar la pregunta no reconocida: {str(e)}')
            return JsonResponse({'message': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'message': 'Error: Método no permitido'}, status=405)
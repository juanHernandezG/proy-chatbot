from transformers import AutoModelForCausalLM, AutoTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from nltk.corpus import stopwords
import nltk
import random

# Verificar si las stopwords ya están descargadas
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    # Descargar las stopwords si no están presentes
    nltk.download('stopwords')

#Crear una lista de stopwords en español
stop_words = set(stopwords.words('spanish'))

# Cargar el archivo JSON
with open('datasetPT.json', 'r', encoding='utf-8') as file:
    dataset = json.load(file)

# Inicializar el modelo GPT-2 en español
model_name = "datificate/gpt2-small-spanish"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Preprocesamiento de texto
def preprocess_text(text):
    text = text.lower()
    # Tokenizar el texto
    words = text.split()
    # Filtrar las stopwords
    filtered_words = [word for word in words if word not in stop_words]
    # Reconstituir el texto
    text = ' '.join(filtered_words)
    
    return text

# Construir el corpus de documentos (intenciones)
corpus = [' '.join(intent['patterns']) for intent in dataset['Intents']]

# Construir la matriz TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)

# Función para generar respuestas
def generate_response(prompt):
    prompt = preprocess_text(prompt)
    
    # Calcular TF-IDF para la pregunta del usuario
    user_tfidf = vectorizer.transform([prompt])

    # Calcular similitud del coseno entre la pregunta del usuario y las intenciones
    cosine_similarities = cosine_similarity(user_tfidf, tfidf_matrix)

    # Seleccionar la intención más similar
    best_intent_index = cosine_similarities.argmax()
    best_intent = dataset['Intents'][best_intent_index]

    # Establecer un umbral de similitud
    similarity_threshold = 0.2

    # Verificar si la similitud es menor que el umbral
    if cosine_similarities[0, best_intent_index] < similarity_threshold:
        response = "Lo siento, no entiendo tu pregunta. ¿Puedes reformularla de manera más clara?"
    else:
        response = random.choice(best_intent['responses'])
        
    return response

# # Función para manejar la entrada del usuario
# def send_message(event=None):
#     # Obtener la entrada del usuario desde el widget de entrada
#     user_input = user_input_entry.get()
#     user_input_entry.delete(0, tk.END)

#     # Generar una respuesta del chatbot utilizando Transformers
#     chatbot_response = generate_response(user_input)

#     # Agregar la entrada del usuario y la respuesta del chatbot al cuadro de chat
#     chatbox.config(state=tk.NORMAL)
#     chatbox.insert(tk.END, "Tu: " + user_input + "\n\n")
#     chatbox.insert(tk.END, "Chatbot: " + chatbot_response + "\n\n")
#     chatbox.config(state=tk.DISABLED)
#     chatbox.see(tk.END)

# # Set up GUI
# root = tk.Tk()
# root.title("Chatbot")
# root.configure(bg="#ff6c3a")

# # Add chatbox
# chatbox = tk.Text(root, height=20, width=60, state=tk.DISABLED)
# chatbox.pack(padx=10, pady=10)

# # Add user input entry widget
# user_input_entry = tk.Entry(root, width=50)
# user_input_entry.pack(padx=10, pady=10)
# user_input_entry.bind("<Return>", send_message)

# # Add send button
# send_button = tk.Button(root, text="Enviar", command=send_message)
# send_button.pack(padx=10, pady=10)

# # Start GUI main loop
# root.mainloop()

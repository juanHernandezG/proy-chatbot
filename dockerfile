FROM python:3.11.4

ENV backHOME=/home/juanhernandez1901/containers/django/proy_chatbot

#definimos la ruta donde se alojara el codigo
WORKDIR /home/juanhernandez1901/containers/django/proy_chatbot


#Actualizamos pip
RUN pip install --upgrade pip

#COPIAMOS LOS ARCHIVOS A NUESTRO DIRECTORIO
COPY . /home/juanhernandez1901/containers/django/proy_chatbot
#COPIAMOS LAS VARIABLES DE ENTORNO


#Corremos el comando para instalar todas las dependencias del requirements.txt
RUN pip install -r requirements.txt

#hacemos las migraciones




CMD python manage.py runserver 0.0.0.0:8000
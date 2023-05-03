#PancaIA Version 0.0.2 Private

import speech_recognition as sr
import keyboard
import pyttsx3
import requests
import json
import datetime

r = sr.Recognizer()

engine = pyttsx3.init()

def speak(text):
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=971682660bfc016747fb46f32226de4a&lang=es&units=metric"
    response = requests.get(url)
    weather_data = json.loads(response.text)

    if weather_data.get('cod') == 200:
        temp = weather_data['main'].get('temp')
        wind = weather_data['wind'].get('speed')
        rain_data = weather_data.get('rain', {}).get('1h', 0)
        rain = "No parece que se vayan a presentar condiciones meteorológicas que indiquen la ocurrencia de precipitaciones en el transcurso del día de hoy." if rain_data == 0 else "Las condiciones meteorológicas sugieren la probabilidad de precipitaciones en el transcurso del día de hoy."
        speak(f"En {city} hay {temp} grados, el viento está a {wind} kilómetros por hora. Comprobando si va a llover hoy... {rain}")
    else:
        speak(f"No se ha encontrado información para {city}")

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=0.5)
    while True:
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language="es-ES")
            print(text)
        except sr.UnknownValueError:
            print("No se ha podido entender el audio")
            continue
        
        text = text.lower()

        if 'quién es tu desarrollador' in text:
            speak("Mi desarrollador es PancaDev")
        elif 'buenos días' in text:
            speak("Buenos dias, espero que hayas dormido bien. Que tengas un buen dia.")
        elif 'registra mi nombre' in text:
            speak("Por ahora no estoy desarrollada, para agregar a nuevos usuarios a mi base de datos.")
        elif 'cierra el programa' in text:
            speak("Cerrando el programa")
            break
        elif 'dime el tiempo en' in text:
            city = text.replace('dime el tiempo en', '').strip()
            get_weather(city)
        elif 'qué hora es' in text:
            spain = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2)))
            hora = spain.strftime("Son las %H:%M en España")
            speak(hora)

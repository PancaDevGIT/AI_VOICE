#PancaIA Version 0.0.1 Private

import speech_recognition as sr
import keyboard
import pyttsx3
import requests
import json
import datetime

r = sr.Recognizer()

engine = pyttsx3.init()

def speak(text):
    engine.setProperty('rate', 100)
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
        rain = "No va a llover hoy" if rain_data == 0 else "Si va a llover hoy"
        speak(f"En {city} hay {temp} grados, el viento está a {wind} kilómetros por hora. Comprobando si va a llover hoy... {rain}")
    else:
        speak(f"No se ha encontrado información para {city}")

with sr.Microphone() as source:
    text = ''
    while True:
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language="es-ES")
            print(text)
        except sr.UnknownValueError:
            print("No se ha podido entender el audio")
            continue
        
        if text == '':
            keyboard.press_and_release('enter')
        
        if 'quién es tu desarrollador' in text.lower():
            speak("Mi desarrollador es PancaDev")

        if 'buenos días' in text.lower():
            speak("Buenos dias, espero que hayas dormido bien. Que tengas un buen dia.")
        
        if 'registra mi nombre' in text.lower():
            speak("Por ahora no estoy desarrollada, para agregar a nuevos usuarios a mi base de datos.")
        
        if 'cierra el programa' in text.lower():
            speak("Cerrando el programa")
            break
        
        if 'dime el tiempo en' in text.lower():
            city = text.lower().replace('dime el tiempo en', '').strip()
            get_weather(city)
        
        if 'qué hora es' in text.lower():

            spain = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2)))
            hora = spain.strftime("Son las %H:%M en España")
            speak(hora)

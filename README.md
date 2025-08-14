# Sentio-AI-Assistant
A voice-driven AI assistant with real-time interaction

## 🚀 Features
- Voice input & output
- Natural Language Understanding
- Customizable personality & responses

## 🛠️ Tech Stack
- Python, gTTS, Gemini AI API


import http
import os

import gemini_ai
import gemini_api
import google.generativeai as genai

from dotenv import load_dotenv
import webbrowser
import datetime
import time
import speech_recognition as rs
import pyttsx3
import requests
from Demos.win32ts_logoff_disconnected import username

USER_NAME = "Vaid"

load_dotenv()
def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()



def takeCommand():
    r = rs.Recognizer()
    with rs.Microphone() as source:
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "some error occured .sorry from sentio"

def greet_user():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    if 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    minute_str = f"{minute:02d}" if minute > 9 else f"oh {minute}"
    time_str = f"{hour}:{minute:02d}"
    spoken_time = f"{hour} {minute_str}"
    say(f"{greeting}, {USER_NAME}! Sentio is ready to assist you. The current time is {spoken_time}.")
    print(f"{greeting}, {USER_NAME}! {greeting} , {USER_NAME}! Sentio is ready to assist you. 0The current time is {spoken_time}.")
    print(f"current time is {time_str}")

    time.sleep(2)


+


gemini_api_key = os.getenv("GEMINI_API_KEY")
weather_api_key = os.getenv("WEATHER_API_KEY")

url = "https://api.gemini.com/v1/pubticker/btcusd"

response = requests.get(url, headers={"Authorization": f"Bearer {gemini_api_key}"})


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        print(f"Weather in {city}: {description}, {temperature}°C")
    else:
        print(f"Error: Unable to fetch weather data for {city}. Status code: {response.status_code}")


def listen_for_city():
    recognizer = rs.Recognizer()

    with rs.Microphone() as source:
        print("Please say the city name...")
        audio = recognizer.listen(source)

        try:
            city = recognizer.recognize_google(audio)
            print(f"You said: {city}")
            return city
        except rs.UnknownValueError:
            print("Sorry, I didn't catch that. Please try again.")
        except rs.RequestError as e:
            print(f"Could not request results; {e}")
greet_user()
city_name = listen_for_city()

if city_name:
    get_weather(city_name)

gemini_api_key=os.getenv("GEMINI_API_KEY")
def chat_with_user(prompt):
    headers = {
        "Authorization": f"Bearer {gemini_api_key}",
        "Content-Type": "application/json"
    }
    url = "https://api.gemini.com/v1/ai/chat"
    data = {"prompt": prompt, "max_tokens": 100}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        response_text = response_data.get("choices")[0].get("text")
        say(response_text)
        print(f"Sentio: {response_text}")
    else:
        say("Sorry, I couldn't fetch a response. Please try again later.")



if __name__ == '__main__':
    print('PyCharm')


    while True:
        print('Listening...')
        query = takeCommand().lower()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],["gemini","https://gemini.google.com/"]
            , ["google", "https://www.google.com"], ["instagram", "https://www.instagram.com"], ["linkedin", "https://www.linkedin.com"],["spotify", "https://www.spotify.com"], ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} Sir...")
                webbrowser.open(site[1])
        if"open music supreme" in query.lower():
            musicPath = "C:/Users/vaids/Downloads/734315.mp3"
            os.startfile(musicPath)
        if"play video of running horses" in query.lower():
            videoPath = "C:/Users/vaids\Downloads\Beautiful Herd of Horses Running Free!.mp4"
            print(videoPath)
            os.startfile(videoPath)

        if "exit" in query or "quit" in query or "stop" in query:
            say(f"Goodbye, {USER_NAME}! See you soon.")
            break

#vaid swami
from difflib import get_close_matches
import http
import os

from dotenv import load_dotenv
import webbrowser
import datetime
import time
import speech_recognition as rs
import pyttsx3
import requests
from Demos.win32ts_logoff_disconnected import username
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pywhatkit as kit
conversation_history = []

current_personality = "default"   # ok


USER_NAME = "Vaid"

load_dotenv()



import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.0-flash")



# faster and best for assistants


def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    time.sleep(1.2)




def takeCommand():
    r = rs.Recognizer()
    r.pause_threshold = 1.5       # how long it waits after you stop speaking
    r.energy_threshold = 250      # sensitivity to background noise
    r.dynamic_energy_threshold = True
    with rs.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.8)
        audio = r.listen(source, timeout=15, phrase_time_limit=25)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            if len(query.strip()) < 2:
                return ""
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


gemini_api_key = os.getenv("GEMINI_API_KEY")

# --------------------- PERSONALITY PRESETS --------------------- #

personality_presets = {
    "default": "You are Sentio — warm, friendly, short, natural, helpful.",
    "professional": "You are Sentio — professional, calm, formal, clear, like a corporate assistant.",
    "funny": "You are Sentio — humorous, light, playful, but still helpful. Add tiny humor.",
    "strict": "You are Sentio — serious, direct, no jokes, no unnecessary talk. Very to the point.",
    "motivational": "You are Sentio — inspiring, positive, supportive, talks like a motivational coach.",
    "siri": "You are Sentio — polite, short answers, clean tone, slightly robotic but friendly like Siri."
}

# -------- LONG TERM MEMORY SAVE -------- #
def save_memory(text):
    with open("sentio_memory.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")

def load_memory():
    if not os.path.exists("sentio_memory.txt"):
        return ""
    with open("sentio_memory.txt", "r", encoding="utf-8") as f:
        return f.read()

# Load memory on start
long_term_memory = load_memory()



def chat_with_sentio(prompt):
    try:
        # Save user message in memory
        conversation_history.append(f"User: {prompt}")
        if len(conversation_history) > 30:
            conversation_history.pop(0)

        memory_text = long_term_memory + "\n" + "\n".join(conversation_history)

        strict_prompt = (
    f"You are Sentio — a smart AI assistant. Your current personality is: {personality_presets[current_personality]}\n"
    "Respond in that style.\n"
    "Keep responses short (1–2 sentences), helpful, natural, and human-like.\n"
    "Use the real current date and time provided below.\n"
    "If the user asks about the year, time, day, or month — ALWAYS use the real system time.\n"
    "If the user gives ANY topic (like 'WhatsApp', 'F1 race drivers', 'Rohini', 'iPhone') → treat it as a valid question and answer properly.\n"
    "ONLY say 'Please complete your question.' if the message ends abruptly like: "
    "'tell me about', 'what is', 'who is', 'information about', or similar incomplete fragments.\n"
    "If user says something personal like 'I am human', 'I am tired', 'I am bored', "
    "respond naturally with empathy.\n"
    "Do NOT be rude. Do NOT give robotic answers.\n\n"
    f"Current date and time: {datetime.datetime.now()}\n\n"
    f"Conversation History:\n{memory_text}\n\n"
    f"User: {prompt}\nSentio:"
)

        # Generate response
        response = model.generate_content(strict_prompt)
        reply = response.text.strip()

        # Save reply to memory
        conversation_history.append(f"Sentio: {reply}")

        say(reply)
        print(f"Sentio: {reply}")
        return reply

    except Exception as e:
        print("Error:", e)
        say("Sorry, I had trouble processing that.")
        return "Sorry, I had trouble processing that."

greet_user()



conversation_mode = False

# WhatsApp Contacts
whatsapp_contacts = {
    "nitin": "+917877858190",
    "dev": "+919269995556",
    "shekhawat": "+919376501607",
    "kaushik": "+919414587180",
    "papa": "+918949240188",
    "mama": "+916376024334",
    "arpit": "+916378042701",
    "parth": "+919929564886",
}


# ---------------- EMAIL AUTOMATION ---------------- #

# Contacts list
contacts = {
    "nitin": "swaminitin20@gmail.com",
    "jayveer": "jaivss14@gmail.com",
    "parth": "parthsarthi2103@gmail.com",
    "arpit": "arpitsharma9406@gmail.com",
    "nishant" :"nishantsirvi2003@gmail.com",
    "sahil": "msgsahil5@gmail.com",
}

# Get your email + password from .env
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(receiver_name, message):
    receiver_name = receiver_name.lower()

    if receiver_name not in contacts:
        return "I don't have this person in my contact list."

    receiver_email = contacts[receiver_name]

    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email
        msg["Subject"] = "Voice Email from Sentio"

        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()

        return f"Email sent to {receiver_name}."
    
    except Exception as e:
        return "Sorry, I could not send the email."
    
def play_song_on_spotify(song_query):
    try:
        # Convert song name to URL search format
        search_query = song_query.replace(" ", "%20")

        url = f"https://open.spotify.com/search/{search_query}"
        say(f"Playing {song_query} on Spotify.")
        webbrowser.open(url)
        return "Opening Spotify search..."
    except:
        return "Sorry, I couldn't open Spotify."


def send_whatsapp_message(name, message):
    name = name.lower()

    # find best match from your contact keys
    possible_name = get_close_matches(name, whatsapp_contacts.keys(), n=1, cutoff=0.5)

    if not possible_name:
        return "I don't have this person in my WhatsApp contacts."

    real_name = possible_name[0]  
    number = whatsapp_contacts[real_name]

    try:
        kit.sendwhatmsg_instantly(number, message, wait_time=15, tab_close=True)
        return f"WhatsApp message sent to {real_name}."
    except:
        return "Sorry, I could not send the WhatsApp message."
    
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        data = requests.get(url).json()

        if data.get("cod") != 200:
            return None

        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        desc = data["weather"][0]["description"].title()

        return f"The weather in {city.title()} is {desc} with a temperature of {temp}°C, feels like {feels}°C."
    except:
        return None



GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

def get_news(category="general"):
    categories_map = {
        "general": "",
        "india": "india",
        "sports": "sports",
        "technology": "technology" 
    }

    query = categories_map.get(category, "")

    url = f"https://gnews.io/api/v4/search?q={query}&lang=en&country=in&max=5&apikey={GNEWS_API_KEY}"

    response = requests.get(url).json()

    articles = response.get("articles", [])

    if not articles:
        return ["No latest news found right now."]

    headlines = [a["title"] for a in articles]
    return headlines

import threading

def start_timer(seconds):
    def timer_thread():
        time.sleep(seconds)
        say("Your timer is complete, Vaid!")
    threading.Thread(target=timer_thread).start()

def set_alarm(time_string):
    try:
        say(f"Alarm set for {time_string}")
        os.system(f'schtasks /create /sc once /tn "SentioAlarm" /tr "cmd /c echo Alarm! && pause" /st {time_string}')
        return True
    except:
        return False




if __name__ == '__main__':
    print("PyCharm")
    print("Testing Weather API…")
    print(requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q=Delhi&appid={WEATHER_API_KEY}&units=metric"
    ).json())

    alarms = {}
    timers = {}

    while True:
        print('Listening...')
        query = takeCommand().lower()
        matched = False

        # -------- PERSONALITY MODE SWITCH -------- #
        if "sentio professional mode" in query:
            current_personality = "professional"
            say("Professional mode activated, Vaid.")
            continue

        elif "sentio funny mode" in query:
            current_personality = "funny"
            say("Funny mode activated. Let's have some fun!")
            continue

        elif "sentio strict mode" in query:
            current_personality = "strict"
            say("Strict mode activated. I will keep answers serious.")
            continue

        elif "sentio motivational mode" in query:
            current_personality = "motivational"
            say("Motivational mode activated. Let’s do this!")
            continue

        elif "sentio siri mode" in query or "sentio siri style" in query:
            current_personality = "siri"
            say("Siri-style mode activated.")
            continue

        # -------- NEWS FEATURE -------- #
        if "news" in query or "headlines" in query:
            say("Which news category? You can say: general, India, sports, technology, or global.")
            category = takeCommand().lower()

            if "india" in category:
                category = "india"
            elif "sport" in category:
                category = "sports"
            elif "tech" in category or "technology" in category:
                category = "technology"
            elif "global" in category:
                category = "global"
            else:
                category = "general"

            headlines = get_news(category)

            say("Here are the top news headlines.")
            for line in headlines:
                say(line)

            matched = True
            continue

        # -------- WEATHER -------- #
        if "weather" in query or "temperature" in query:
            say("Which city should I check, Vaid?")
            city = takeCommand().lower()

            weather_info = get_weather(city)

            if weather_info:
                say(weather_info)
            else:
                say("Sorry, I couldn't fetch the weather for that city.")

            matched = True
            continue

        # -------- TIMER -------- #
        if "set a timer" in query or "set timer" in query:
            say("For how many minutes?")
            duration = takeCommand().lower()

            try:
                minutes = int(duration.split()[0])
                seconds = minutes * 60
                say(f"Timer set for {minutes} minutes.")

                def run_timer(sec):
                    time.sleep(sec)
                    say("Time's up, Vaid!")

                import threading
                threading.Thread(target=run_timer, args=(seconds,), daemon=True).start()
            except:
                say("Sorry, I couldn't understand the timer duration.")

            matched = True
            continue

        # -------- ALARM -------- #
        if "set alarm" in query or "alarm for" in query:
            say("At what time should I set the alarm?")
            alarm_time = takeCommand().lower()

            try:
                alarm_time_24 = datetime.datetime.strptime(alarm_time, "%I %M %p").strftime("%H:%M")
            except:
                try:
                    alarm_time_24 = datetime.datetime.strptime(alarm_time, "%I %p").strftime("%H:%M")
                except:
                    say("Sorry, I couldn't understand the alarm time.")
                    matched = True
                    continue

            say(f"Alarm set for {alarm_time}.")

            def alarm_checker(target_time):
                while True:
                    now = datetime.datetime.now().strftime("%H:%M")
                    if now == target_time:
                        say("Vaid, your alarm is ringing!")
                        break
                    time.sleep(20)

            import threading
            threading.Thread(target=alarm_checker, args=(alarm_time_24,), daemon=True).start()

            matched = True
            continue

        # -------- WHATSAPP -------- #
        if "send whatsapp" in query or "whatsapp message" in query:
            say("Who do you want to send the message to?")
            name = takeCommand().lower()

            say("What should the message say?")
            message = takeCommand()

            result = send_whatsapp_message(name, message)
            say(result)
            matched = True
            continue

        # -------- EMAIL -------- #
        if "send email" in query or "send a mail" in query:
            say("Who do you want to send the email to?")
            name = takeCommand().lower()

            say("What should I say?")
            message = takeCommand()

            result = send_email(name, message)
            say(result)
            matched = True
            continue

        # -------- GREETING -------- #
        greeting_words = ["hi", "hello", "hey"]

        if query.strip() in greeting_words or query.strip() in [f"{g} sentio" for g in greeting_words]:
            say(f"Hello {USER_NAME}, I'm right here. How can I help you?")
            matched = True
            continue

        # -------- WAKE WORD -------- #
        wake_words = ["sentio", "hey sentio", "ok sentio"]

        if query.strip() in wake_words:
            say("Yes Vaid, I'm listening.")
            conversation_mode = True
            continue

        if conversation_mode:
            conversation_mode = False

        # -------- SPOTIFY -------- #
        if ("play" in query and "song" in query) or query.startswith("play "):
            say("Which song should I play, Vaid?")
            song = takeCommand().lower()

            if song != "":
                say(f"Playing {song} on Spotify.")
                url = f"https://open.spotify.com/search/{song.replace(' ', '%20')}"
                webbrowser.open(url)
                matched = True
                continue
            else:
                say("I couldn't hear the song name. Please try again.")
                continue

        # -------- MEMORY COMMAND (STEP 5) -------- #
        if "remember this" in query or "save this" in query:
            say("Okay Vaid, tell me what to remember.")
            info = takeCommand()

            save_memory(f"{datetime.datetime.now()} - {info}")
            long_term_memory = load_memory()

            say("Got it. I will remember that.")
            matched = True
            continue

        # -------- OPEN ANY WEBSITE -------- #
        if query.startswith("open "):
            site_name = query.replace("open ", "").strip().replace(" ", "")
            url = f"https://www.{site_name}.com"
            say(f"Opening {site_name}...")
            webbrowser.open(url)
            matched = True
            continue

        # -------- PRESET WEBSITES -------- #
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["gemini", "https://gemini.google.com/"],
            ["google", "https://www.google.com"],
            ["instagram", "https://www.instagram.com"],
            ["linkedin", "https://www.linkedin.com"],
            ["spotify", "https://www.spotify.com"]
        ]

        for site in sites:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]} Sir...")
                webbrowser.open(site[1])
                matched = True
                break

        # -------- EXIT -------- #
        if "exit" in query or "quit" in query or "stop" in query:
            say(f"Goodbye, {USER_NAME}! See you soon.")
            break

        # -------- DEFAULT CHAT -------- #
        if not matched:
            chat_with_sentio(query)




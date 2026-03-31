import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent.parent
BACKEND_DIR = BASE_DIR / "backend"
CONFIG_DIR = BASE_DIR / "config"

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sentio.db")

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# JWT Settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days

# User Settings
USER_NAME = "Vaid"
DEFAULT_PERSONALITY = "default"

# Load personalities from JSON
personality_file = CONFIG_DIR / "personalities.json"
if personality_file.exists():
    with open(personality_file, "r") as f:
        PERSONALITY_PRESETS = json.load(f)
else:
    # Default personalities if file doesn't exist
    PERSONALITY_PRESETS = {
        "default": "You are Sentio — warm, friendly, short, natural, helpful.",
        "professional": "You are Sentio — professional, calm, formal, clear, like a corporate assistant.",
        "funny": "You are Sentio — humorous, light, playful, but still helpful. Add tiny humor.",
        "strict": "You are Sentio — serious, direct, no jokes, no unnecessary talk. Very to the point.",
        "motivational": "You are Sentio — inspiring, positive, supportive, talks like a motivational coach.",
        "siri": "You are Sentio — polite, short answers, clean tone, slightly robotic but friendly like Siri."
    }

# Contacts
WHATSAPP_CONTACTS = {
    "nitin": "+917877858190",
    "dev": "+919269995556",
    "shekhawat": "+919376501607",
    "kaushik": "+919414587180",
    "papa": "+918949240188",
    "mama": "+916376024334",
    "arpit": "+916378042701",
    "parth": "+919929564886",
}

EMAIL_CONTACTS = {
    "nitin": "swaminitin20@gmail.com",
    "jayveer": "jaivss14@gmail.com",
    "parth": "parthsarthi2103@gmail.com",
    "arpit": "arpitsharma9406@gmail.com",
    "nishant": "nishantsirvi2003@gmail.com",
    "sahil": "msgsahil5@gmail.com",
}

# Speech Settings
SPEECH_RATE = 150
RECOGNITION_LANGUAGE = "en-in"

# AI Settings
MAX_CONVERSATION_HISTORY = 10  # Keep last 10 messages for context

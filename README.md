# 🤖 Sentio AI Assistant

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**Sentio** is an advanced voice-powered AI assistant built with Python that combines Google's Gemini AI with powerful automation capabilities. Control your computer, send messages, get weather updates, and much more—all through natural voice commands.

---

## ✨ Features

### 🎭 **Multiple Personality Modes**
- **Default** - Warm, friendly, and helpful
- **Professional** - Corporate and formal assistant
- **Funny** - Humorous and light-hearted
- **Strict** - Serious and direct
- **Motivational** - Inspiring and positive
- **Siri** - Polite and concise responses

### 🧠 **AI-Powered Intelligence**
- Natural conversation using Google Gemini 2.0 Flash
- Context-aware responses with conversation history
- Long-term memory system for personalized interactions
- Real-time date and time awareness

### 📱 **Communication**
- **WhatsApp Integration** - Send instant messages via voice
- **Email Automation** - Compose and send emails hands-free
- Contact management for both platforms

### 🌦️ **Information Services**
- **Weather Updates** - Real-time weather for any city
- **News Headlines** - Latest news across multiple categories (General, India, Sports, Technology)
- Date and time queries

### 🎵 **Media Control**
- Spotify integration for music playback
- System volume control (up/down/mute/unmute)
- Play songs by voice command

### 💻 **System Control**
- Screen brightness adjustment
- System shutdown, restart, sleep, and lock
- Screenshot capture
- Camera access
- Website launcher

### ⏰ **Time Management**
- Voice-activated timers
- Custom alarm setting
- Time and date queries

### 📝 **Memory System**
- Save important information with "remember this"
- Persistent storage across sessions
- Context retention in conversations

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Windows OS (for system control features)
- Microphone for voice input
- Active internet connection

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/vaid27/Sentio-AI-Assistant.git
cd Sentio-AI-Assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create a `.env` file** in the root directory with the following:
```env
GEMINI_API_KEY=your_gemini_api_key_here
SENDER_EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
WEATHER_API_KEY=your_openweather_api_key_here
GNEWS_API_KEY=your_gnews_api_key_here
```

4. **Get API Keys**
   - **Gemini API**: [Google AI Studio](https://makersuite.google.com/app/apikey)
   - **Weather API**: [OpenWeatherMap](https://openweathermap.org/api)
   - **News API**: [GNews](https://gnews.io/)
   - **Email**: Generate an [App Password](https://support.google.com/accounts/answer/185833) for Gmail

5. **Run Sentio**
```bash
python main.py
```

---

## 📦 Dependencies

```
google-generativeai
pyttsx3
SpeechRecognition
pyautogui
pywhatkit
python-dotenv
requests
screen-brightness-control
smtplib
```

---

## 🎯 Usage

### Basic Commands

**Personality Switching:**
- "Sentio professional mode"
- "Sentio funny mode"
- "Sentio strict mode"
- "Sentio motivational mode"
- "Sentio Siri mode"

**Communication:**
- "Send WhatsApp to [name]"
- "Send email to [name]"

**Information:**
- "What's the weather in [city]?"
- "Tell me the news" (then specify: general/India/sports/technology)

**Media:**
- "Play [song name] on Spotify"
- "Increase/decrease volume"
- "Mute/unmute"

**System Control:**
- "Increase/decrease brightness"
- "Take screenshot"
- "Open camera"
- "Shutdown/restart/sleep/lock"

**Time Management:**
- "Set a timer for [X] minutes"
- "Set alarm for [time]"

**Memory:**
- "Remember this: [information]"

**Web:**
- "Open [website name]" (e.g., "Open YouTube")

**General Chat:**
- Just say "Sentio" or "Hey Sentio" and then ask anything!

---

## 🛠️ Configuration

### Adding Contacts

**WhatsApp Contacts** (`main.py` line ~183):
```python
whatsapp_contacts = {
    "name": "+91XXXXXXXXXX",
}
```

**Email Contacts** (`main.py` line ~192):
```python
contacts = {
    "name": "email@example.com",
}
```

### Adjusting Voice Settings
Modify the `say()` function for speech rate, volume, or voice selection.

### Microphone Sensitivity
Adjust these values in `takeCommand()` function:
```python
r.pause_threshold = 1.5        # Pause duration
r.energy_threshold = 250       # Background noise sensitivity
```

---

## 🌐 React Frontend (Optional)

A React.js interface (`sentio.js`) is included for browser-based interaction. To use:

1. Set up a Flask/FastAPI backend to connect with `main.py`
2. Create an endpoint at `http://localhost:5000/ask`
3. Install React dependencies and run the frontend

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🐛 Known Issues

- WhatsApp message sending requires WhatsApp Web to be logged in
- System control features are Windows-specific
- Voice recognition accuracy depends on microphone quality and ambient noise

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Vaid Swami**
- GitHub: [@vaid27](https://github.com/vaid27)

---

## 🙏 Acknowledgments

- Google Gemini AI for natural language processing
- OpenWeatherMap for weather data
- GNews API for news headlines
- All open-source library contributors

---

## 📞 Support

If you encounter any issues or have questions:
- Open an [Issue](https://github.com/vaid27/Sentio-AI-Assistant/issues)
- Star ⭐ the repository if you find it helpful!

---

## 🔮 Future Enhancements

- [ ] Task management and to-do lists
- [ ] Calendar integration
- [ ] Multi-language support
- [ ] Offline mode for basic commands
- [ ] Mobile app integration
- [ ] Custom voice training
- [ ] Document reading and summarization

---

<div align="center">

**Made with ❤️ by Vaid Swami**

*"Your AI companion for a smarter, hands-free digital life"*

</div>

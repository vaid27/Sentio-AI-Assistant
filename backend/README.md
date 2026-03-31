# 🤖 Sentio AI Chat Robot - Backend API

This is the FastAPI backend for the Sentio AI Chat Robot web application.

## 📋 Features

- **Chat API**: `/api/chat/send` - Send messages and get AI responses
- **Chat History**: `/api/chat/history` - Retrieve conversation history
- **Personality Mode**: `/api/chat/personality` - Switch between personality modes
- **Database**: SQLite (dev) / PostgreSQL (production)
- **AI Integration**: Google Gemini 2.0 Flash
- **CORS**: Enabled for React frontend

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
cd ..
python -m backend.init_db
```

This will:
- Create database tables
- Create a test user (email: `test@sentio.ai`, password: `test123`)
- Add sample messages

### 3. Run the Backend Server

```bash
python -m backend.main
```

The server will start at `http://localhost:8000`

### 4. Access API Documentation

- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📚 API Endpoints

### Chat Endpoints

#### Send Message
```
POST /api/chat/send?user_id=1
Content-Type: application/json

{
    "message": "Hello! What's your name?"
}
```

**Response:**
```json
{
    "response": "I'm Sentio, your AI assistant!",
    "timestamp": "2024-03-31T10:30:00",
    "conversation_history_count": 15
}
```

#### Get Chat History
```
GET /api/chat/history?user_id=1&limit=50
```

**Response:**
```json
{
    "messages": [
        {
            "id": 1,
            "role": "user",
            "content": "Hello!",
            "timestamp": "2024-03-31T10:30:00"
        },
        {
            "id": 2,
            "role": "assistant",
            "content": "Hi there!",
            "timestamp": "2024-03-31T10:30:05"
        }
    ],
    "total_count": 2
}
```

#### Clear Chat History
```
DELETE /api/chat/history?user_id=1
```

#### Set Personality
```
POST /api/chat/personality?user_id=1&personality=professional
```

**Available Personalities:**
- `default` - Warm, friendly, helpful
- `professional` - Corporate, formal
- `funny` - Humorous, playful
- `strict` - Serious, direct
- `motivational` - Inspiring, positive
- `siri` - Polite, concise

#### Get Current Personality
```
GET /api/chat/personality?user_id=1
```

## 🗄️ Database Schema

### Users Table
```
id (Integer, Primary Key)
email (String, Unique)
username (String, Unique)
hashed_password (String)
personality (String, Default: "default")
created_at (DateTime)
updated_at (DateTime)
```

### Messages Table
```
id (Integer, Primary Key)
user_id (Integer, Foreign Key)
role (String: "user" or "assistant")
content (Text)
timestamp (DateTime, Indexed)
```

### Memory Table
```
id (Integer, Primary Key)
user_id (Integer, Foreign Key)
content (Text)
category (String, Default: "general")
timestamp (DateTime, Indexed)
```

## 📝 Environment Variables

Create `.env` in the project root:

```
# API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# Database (SQLite for dev, PostgreSQL for production)
DATABASE_URL=sqlite:///./sentio_chat.db
# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/sentio_db

# JWT Security
SECRET_KEY=your-secret-key-change-in-production

# Optional
WEATHER_API_KEY=your_weather_api_key_here
GNEWS_API_KEY=your_gnews_api_key_here
SENDER_EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
```

## 🔧 Development Tips

### Run in Development Mode (with auto-reload)
```bash
python -m backend.main
```

### Access Interactive Docs
The API documentation is auto-generated. Visit `/docs` to test endpoints directly.

### Database Reset
To start fresh:
```bash
# Delete the SQLite database file
rm sentio_chat.db

# Reinitialize
python -m backend.init_db
```

### Debug Logs
Check console output for detailed logs. All API calls and errors are logged.

## 📦 Project Structure

```
backend/
├── __init__.py
├── main.py                 # FastAPI app entry point
├── config.py              # Configuration settings
├── database.py            # SQLAlchemy setup
├── models.py              # Database models
├── init_db.py             # Database initialization
├── requirements.txt       # Python dependencies
├── routes/
│   ├── __init__.py
│   └── chat.py           # Chat endpoints
├── services/
│   ├── __init__.py
│   └── ... (future services)
└── utils/
    ├── __init__.py
    └── ... (helper utilities)
```

## 🚨 Troubleshooting

### CORS Error
Make sure you're running the frontend on `http://localhost:3000` or `http://localhost:5173`. Update `app.add_middleware` in `main.py` if needed.

### Database Lock Error
Close any other processes accessing the database and try again.

### Gemini API Error
Verify your `GEMINI_API_KEY` is valid in `.env`

### Connection Refused
Make sure the server is running: `python -m backend.main`

## 🔐 Security Notes

⚠️ **For Production:**
1. Change `SECRET_KEY` in `.env`
2. Use PostgreSQL instead of SQLite
3. Enable HTTPS/SSL
4. Implement proper JWT authentication
5. Add rate limiting
6. Use environment variables for all secrets
7. Validate and sanitize all inputs

## 📈 Next Steps

1. ✅ Backend API is ready
2. ⏳ Build React frontend (frontend/)
3. ⏳ Connect frontend to backend
4. ⏳ Deploy to cloud (Vercel + Render/Railway)

## 📞 Support

For issues or questions, check:
- API Docs: http://localhost:8000/docs
- Error logs in console
- Database query issues: Check SQLAlchemy logs

---

Happy coding! 🚀

# 🎯 YOUR SENTIO AI SYSTEM - QUICK START GUIDE

## 🔴 STATUS CHECK

```
✅ Backend API Running        → Port 8000
✅ Database Active           → sentio_chat.db
✅ Test User Created         → ID: 1, testuser@sentio.ai
✅ Documentation Ready       → Auto-generated Swagger UI
✅ Original CLI Working      → main.py (unchanged)
```

---

## 🌐 3 WAYS TO ACCESS YOUR SYSTEM NOW

### **WAY 1: Interactive Browser Testing** 🎨
```
NO CODING NEEDED - Just click and test!

URL: http://localhost:8000/docs

What you'll see:
├─ All 5 API endpoints listed
├─ Try-it-out buttons for each endpoint
├─ Automatic request/response formatting
├─ Real-time responses from your backend
└─ Perfect for learning how the system works
```

### **WAY 2: Python Commands** 🐍
```bash
# Test everything in one go:
python tests/test_all.py

# Or test individual features:
python tests/test_health.py          # Is backend running?
python tests/test_history.py         # View chat history
python tests/test_personality.py     # Test personality switching
```

### **WAY 3: Python Code** 💻
```python
import requests

# Send a message
response = requests.post(
    "http://localhost:8000/api/chat/send?user_id=1",
    json={"message": "Hello Sentio!"}
)
result = response.json()
print(result['response'])  # AI response

# Check history
hist = requests.get("http://localhost:8000/api/chat/history?user_id=1").json()
print(f"You have {hist['total_count']} messages saved")

# Switch personality
requests.post("http://localhost:8000/api/chat/personality?user_id=1&personality=funny")
```

---

## 🚀 WHAT YOU CAN DO NOW (That You Couldn't Before)

### ❌ BEFORE (Original CLI Only)
```
One user at a time
Voice input only
No web access
No chat history
No personality switching
Data lost on restart
Can't access from browser
```

### ✅ NOW (CLI + API Backend)
```
Multiple users simultaneously
Voice + API access
Access from web browser anytime
Full persistent chat history
6 personality modes to switch
Data saved forever in database
View/manage everything from http://localhost:8000
Control from Python code
Ready for mobile apps
Ready for integrations (Slack, Discord, etc.)
```

---

## 📊 URLS YOU SHOULD KNOW

| Purpose | URL | How to Use |
|---------|-----|-----------|
| **Test API** | http://localhost:8000/docs | Open in browser |
| **Health Check** | http://localhost:8000/health | curl or browser |
| **API Root** | http://localhost:8000/ | Info about API |
| **JavaScript Console** | DevTools in browser | See requests/responses |
| **Database File** | sentio_chat.db | SQLite database (in your project folder) |

---

## 🎬 STEP-BY-STEP: See It Working

### **Step 1: Open Browser**
```
Go to: http://localhost:8000/docs
```

### **Step 2: Click on POST /api/chat/send**
```
Expands to show:
├─ Parameter: user_id = 1
├─ Request body (empty initially)
└─ Try it out button
```

### **Step 3: Click "Try it out"**
```
Now you can:
├─ Fill in message: "Hello"
├─ See the request that will be sent
└─ Click "Execute"
```

### **Step 4: See Response**
```
Response will show:
├─ Status: 200 (success) or error code
├─ Response body (JSON):
│  ├─ response: "AI's message back"
│  ├─ timestamp: "2024-01-20T15:30:45.123"
│  └─ history_count: 1
└─ cURL equivalent (for command line)
```

### **Step 5: Try Other Endpoints**
```
GET /api/chat/history
└─ See all your saved messages

GET /api/chat/personality
└─ See available personality modes

POST /api/chat/personality
└─ Switch to a different personality

DELETE /api/chat/history
└─ Clear all messages
```

---

## 🔧 BACKEND CHECK

### **Is Server Running?**
```bash
# Check 1: In terminal, you should see:
#  "Uvicorn running on http://0.0.0.0:8000"

# Check 2: Run this (in a different terminal):
curl http://localhost:8000/health

# Check 3: Should return:
{"status":"ok","service":"Sentio AI Chat Robot","version":"1.0.0"}
```

### **Is Database Working?**
```bash
# The file should exist:
ls -l sentio_chat.db

# Or in Python:
import sqlite3
conn = sqlite3.connect('sentio_chat.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM users')
print(f"Users in database: {cursor.fetchone()[0]}")
```

---

## 📱 WHAT'S IN THE DATABASE

### **Users Table**
```
ID: 1
Email: test@sentio.ai
Username: testuser
Personality: funny (changeable)
Created: 2024-01-20
```

### **Messages Table**
```
Stores all conversations:
- Each message from you
- Each response from AI
- Exact timestamp
- Role (you vs AI)
```

### **Memory Table**
```
Reserved for future:
- Things the AI should remember
- User preferences
- Context information
```

---

## 🎯 THE 5 ENDPOINTS EXPLAINED

### **1. Send Message (POST)**
```
Endpoint: /api/chat/send?user_id=1
What it does:
├─ Takes your message
├─ Gets conversation history (last 10 messages)
├─ Gets your memories
├─ Asks Gemini API for response
├─ Saves both messages to database
└─ Returns AI response

Request:
{
  "message": "What's the weather?"
}

Response:
{
  "response": "I'd need to check...",
  "timestamp": "2024-01-20T15:30:45.123Z",
  "history_count": 5
}
```

### **2. Get History (GET)**
```
Endpoint: /api/chat/history?user_id=1&limit=50
What it does:
├─ Retrieves all your messages
├─ Retrieves all AI responses
├─ Returns in order
└─ With timestamps and metadata

Response:
{
  "messages": [
    {"role": "user", "content": "Hi", ...},
    {"role": "assistant", "content": "Hello!", ...}
  ],
  "total_count": 10
}
```

### **3. Clear History (DELETE)**
```
Endpoint: /api/chat/history?user_id=1
What it does:
├─ Deletes ALL your messages
├─ Returns count of deleted items
└─ Fresh start

Response:
{
  "message": "History cleared",
  "deleted_count": 10
}
```

### **4. Set Personality (POST)**
```
Endpoint: /api/chat/personality?user_id=1&personality=funny
What it does:
├─ Changes your personality preference
├─ AI uses this in all future responses
└─ Saved in database

Available: default, professional, funny, strict, motivational, siri

Response:
{
  "personality": "funny",
  "message": "Personality updated!"
}
```

### **5. Get Personality (GET)**
```
Endpoint: /api/chat/personality?user_id=1
What it does:
├─ Shows your current personality
├─ Shows all available options
└─ Helpful for UI dropdown

Response:
{
  "personality": "funny",
  "available_personalities": [
    "default",
    "professional",
    "funny",
    "strict",
    "motivational",
    "siri"
  ]
}
```

---

## 💡 PRO TIPS

### **Tip 1: Use Browser Dev Tools**
```
Open: http://localhost:8000/docs
Press: F12 (to open Developer Tools)
Tab: Network
Now when you execute API calls, you'll see:
├─ HTTP method used
├─ URL called
├─ Request body
├─ Response body
└─ Response time (ms)
```

### **Tip 2: Test with Different Users**
```
Change ?user_id=1 to ?user_id=2

Each user gets:
├─ Separate messages
├─ Own personality preference
├─ Private conversation history
└─ Isolated data
```

### **Tip 3: Watch the Database Grow**
```
Every message creates a new row in MESSAGES table

Before:  sqlite> SELECT COUNT(*) FROM messages;
         4

After one chat: sqlite> SELECT COUNT(*) FROM messages;
                6
```

### **Tip 4: Personality Changes Immediately**
```
1. Set personality to "professional"
2. Send next message
3. AI responds in professional tone
→ No restart needed!
```

---

## ⚡ QUICK COMMANDS

```bash
# Test all endpoints at once:
python tests/test_all.py

# Test just one endpoint:
python -c "import requests; print(requests.get('http://localhost:8000/health').json())"

# Check database:
sqlite3 sentio_chat.db "SELECT COUNT(*) FROM messages;"

# Check if port is in use:
netstat -ano | findstr :8000

# View database content:
sqlite3 sentio_chat.db ".tables"
sqlite3 sentio_chat.db "SELECT * FROM users;"
```

---

## 🎓 LEARNING PATH

1. **First**: Visit http://localhost:8000/docs
   - Get familiar with Swagger UI
   - Read endpoint descriptions

2. **Second**: Click "Try it out" on /api/chat/personality
   - See what endpoints are available
   - Test getting current personality

3. **Third**: Test /api/chat/history
   - See what data format is returned
   - Understand the structure

4. **Fourth**: Try POST /api/chat/send
   - Send a test message
   - See AI response (if API key is valid)

5. **Fifth**: Run python tests/test_all.py
   - See all features automated
   - Understand the workflow

6. **Sixth**: Write your own Python code
   - Make requests to the API
   - Process responses
   - Build on top

---

## 🔐 REMEMBER

- ✅ Backend is running on **port 8000**
- ✅ Database file is **sentio_chat.db**
- ✅ Test user is **ID: 1**
- ✅ Original CLI (**main.py**) still works unchanged
- ✅ Data is **persistent** (survives restart)
- ✅ Original whatsapp and email features still available
- ✅ All data is **backed up in database** (not just text files)

---

## 🚀 YOU NOW HAVE

✅ A working REST API
✅ A persistent database
✅ Multi-user support
✅ Personality system
✅ Browser access ready
✅ Mobile-ready architecture
✅ Integration-ready endpoints
✅ Beautiful API documentation
✅ Complete test suite
✅ Production foundation

**Next step: Build the React frontend to create a beautiful web UI!** 🎨

---

## 📞 SUPPORT

For issues:
- Check TRANSFORMATION_SUMMARY.md for detailed architecture
- Check backend/README.md for API documentation
- Check tests/README.md for testing guide
- Run tests/test_all.py to diagnose issues

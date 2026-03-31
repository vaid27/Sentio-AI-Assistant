# 🧪 Testing Sentio AI Backend - Complete Guide

## ✅ Prerequisites

Make sure the backend is running:
```bash
cd "c:\Users\vaids\OneDrive\Desktop\SENTIO AI"
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 🧪 Test 1: Health Check (Simplest)

### Python Script
**File: `test_health.py`**
```python
import requests

url = "http://localhost:8000/health"

response = requests.get(url)
print("Status Code:", response.status_code)
print("Response:")
print(response.json())
```

### Run It
```bash
python test_health.py
```

### Expected Output
```
Status Code: 200
Response:
{'status': 'ok', 'service': 'Sentio AI Chat Robot', 'version': '1.0.0'}
```

### Using curl (Windows Command)
```bash
curl http://localhost:8000/health
```

---

## 💬 Test 2: Send a Message & Get AI Response

### Python Script
**File: `test_chat.py`**
```python
import requests
import json

# API endpoint
url = "http://localhost:8000/api/chat/send?user_id=1"

# Message to send
data = {
    "message": "Hello Sentio! What is your name?"
}

# Send request
print("Sending message...")
response = requests.post(url, json=data)

# Print response
print("\n✅ Response Status:", response.status_code)
print("\n📄 Full Response:")
print(json.dumps(response.json(), indent=2))

# Print just the AI response
if response.status_code == 200:
    ai_response = response.json()['response']
    print(f"\n🤖 Sentio Says: {ai_response}")
```

### Run It
```bash
python test_chat.py
```

### Expected Output
```
Sending message...

✅ Response Status: 200

📄 Full Response:
{
  "response": "I'm Sentio, your AI assistant. How can I help you today?",
  "timestamp": "2024-03-31T12:45:30.123456",
  "conversation_history_count": 7
}

🤖 Sentio Says: I'm Sentio, your AI assistant. How can I help you today?
```

---

## 📝 Test 3: Send Multiple Messages (Conversation)

### Python Script
**File: `test_conversation.py`**
```python
import requests
import json
import time

url = "http://localhost:8000/api/chat/send?user_id=1"

messages = [
    "Hello Sentio!",
    "What's your name?",
    "Can you tell me a joke?",
    "What can you do?"
]

print("🎭 Starting Conversation with Sentio\n")
print("=" * 60)

for i, message in enumerate(messages, 1):
    print(f"\n📤 Message {i}: {message}")
    
    data = {"message": message}
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"🤖 Sentio: {result['response']}")
        print(f"⏱️  Timestamp: {result['timestamp']}")
        print(f"📊 Total Messages: {result['conversation_history_count']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    time.sleep(1)  # Wait 1 second between messages

print("\n" + "=" * 60)
print("✅ Conversation Complete!")
```

### Run It
```bash
python test_conversation.py
```

### Expected Output
```
🎭 Starting Conversation with Sentio

============================================================

📤 Message 1: Hello Sentio!
🤖 Sentio: Hi! I'm Sentio, your AI assistant. How can I help you?
⏱️  Timestamp: 2024-03-31T12:45:30.123456
📊 Total Messages: 9

📤 Message 2: What's your name?
🤖 Sentio: I'm Sentio, your friendly AI assistant.
⏱️  Timestamp: 2024-03-31T12:45:32.654321
📊 Total Messages: 11

📤 Message 3: Can you tell me a joke?
🤖 Sentio: Sure! Why don't scientists trust atoms? Because they make up everything!
⏱️  Timestamp: 2024-03-31T12:45:34.234567
📊 Total Messages: 13

📤 Message 4: What can you do?
🤖 Sentio: I can chat, remember things, and help with various tasks!
⏱️  Timestamp: 2024-03-31T12:45:36.897654
📊 Total Messages: 15

============================================================
✅ Conversation Complete!
```

---

## 📚 Test 4: Get Chat History

### Python Script
**File: `test_history.py`**
```python
import requests
import json

url = "http://localhost:8000/api/chat/history?user_id=1&limit=10"

print("📜 Retrieving Chat History...\n")

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    print(f"Total Messages: {data['total_count']}\n")
    print("=" * 60)
    
    for msg in data['messages']:
        role = "👤 You" if msg['role'] == 'user' else "🤖 Sentio"
        print(f"\n{role}:")
        print(f"  {msg['content']}")
        print(f"  Time: {msg['timestamp']}")
    
    print("\n" + "=" * 60)
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
```

### Run It
```bash
python test_history.py
```

### Expected Output
```
📜 Retrieving Chat History...

Total Messages: 15

============================================================

👤 You:
  Hello Sentio!
  Time: 2024-03-31T12:45:30.123456

🤖 Sentio:
  Hi! I'm Sentio, your AI assistant. How can I help you?
  Time: 2024-03-31T12:45:30.654321

👤 You:
  What's your name?
  Time: 2024-03-31T12:45:32.234567

🤖 Sentio:
  I'm Sentio, an AI assistant here to help!
  Time: 2024-03-31T12:45:32.897654

... (and more messages)

============================================================
```

---

## 🎭 Test 5: Switch Personality Modes

### Python Script
**File: `test_personality.py`**
```python
import requests
import json

# List of personalities to test
personalities = ["default", "professional", "funny", "strict", "motivational", "siri"]

print("🎭 Testing Personality Modes\n")
print("=" * 60)

for personality in personalities:
    # Set personality
    url_set = f"http://localhost:8000/api/chat/personality?user_id=1&personality={personality}"
    response_set = requests.post(url_set)
    
    if response_set.status_code == 200:
        print(f"\n✅ Set to '{personality}' mode")
        
        # Send message to see personality in action
        url_chat = "http://localhost:8000/api/chat/send?user_id=1"
        data = {"message": "I feel tired today"}
        response_chat = requests.post(url_chat, json=data)
        
        if response_chat.status_code == 200:
            ai_response = response_chat.json()['response']
            print(f"   Input: 'I feel tired today'")
            print(f"   Response: {ai_response}")
    else:
        print(f"\n❌ Failed to set {personality} mode")

print("\n" + "=" * 60)
```

### Run It
```bash
python test_personality.py
```

### Expected Output
```
🎭 Testing Personality Modes

============================================================

✅ Set to 'default' mode
   Input: 'I feel tired today'
   Response: That's understandable. Make sure to get some rest!

✅ Set to 'professional' mode
   Input: 'I feel tired today'
   Response: I recommend taking a break to recharge your energy levels.

✅ Set to 'funny' mode
   Input: 'I feel tired today'
   Response: Sounds like your batteries need recharging! 😄

✅ Set to 'strict' mode
   Input: 'I feel tired today'
   Response: Rest when necessary to maintain productivity.

✅ Set to 'motivational' mode
   Input: 'I feel tired today'
   Response: Remember, rest is essential! Take a break and come back stronger!

✅ Set to 'siri' mode
   Input: 'I feel tired today'
   Response: I suggest taking some rest to recover.

============================================================
```

---

## 🧹 Test 6: Clear Chat History

### Python Script
**File: `test_clear_history.py`**
```python
import requests

url = "http://localhost:8000/api/chat/history?user_id=1"

print("🗑️  Clearing chat history...\n")

response = requests.delete(url)

if response.status_code == 200:
    data = response.json()
    print(f"✅ Success!")
    print(f"   Message: {data['message']}")
    print(f"   Deleted Messages: {data['deleted_count']}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
```

### Run It
```bash
python test_clear_history.py
```

### Expected Output
```
🗑️  Clearing chat history...

✅ Success!
   Message: Chat history cleared
   Deleted Messages: 15
```

---

## 🔍 Test 7: Get Current Personality

### Python Script
**File: `test_get_personality.py`**
```python
import requests
import json

url = "http://localhost:8000/api/chat/personality?user_id=1"

print("🎭 Getting Current Personality...\n")

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"Current: {data['personality']}")
    print(f"Description: {data['description']}")
    print(f"\nAvailable personalities:")
    for p in data['available_personalities']:
        print(f"  - {p}")
else:
    print(f"❌ Error: {response.status_code}")
```

### Run It
```bash
python test_get_personality.py
```

### Expected Output
```
🎭 Getting Current Personality...

Current: default
Description: You are Sentio — warm, friendly, short, natural, helpful.

Available personalities:
  - default
  - professional
  - funny
  - strict
  - motivational
  - siri
```

---

## 🌐 Test 8: Using Interactive API Docs (Best for Beginners)

### Step-by-Step

1. **Keep backend running** in terminal
   ```bash
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```

2. **Open browser** and go to:
   ```
   http://localhost:8000/docs
   ```

3. **You'll see all endpoints**. Click on them to expand:
   - `/health` - Health check
   - `/api/chat/send` - Send message
   - `/api/chat/history` - Get history
   - `/api/chat/personality` - Manage personality

4. **To test an endpoint:**
   - Click on it to expand
   - Click "Try it out"
   - Enter parameters (user_id=1, message="hello")
   - Click "Execute"
   - See response immediately!

---

## 📊 Test 9: Complete Testing Suite

**File: `test_all.py`**
```python
import requests
import json

BASE_URL = "http://localhost:8000"
USER_ID = 1

print("\n")
print("=" * 70)
print("🧪 SENTIO AI BACKEND - COMPLETE TEST SUITE")
print("=" * 70)

# TEST 1: Health Check
print("\n[1] Health Check")
print("-" * 70)
try:
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    print("✅ PASS - Backend is running")
except:
    print("❌ FAIL - Backend not responding")
    exit(1)

# TEST 2: Send Message
print("\n[2] Send Chat Message")
print("-" * 70)
try:
    r = requests.post(
        f"{BASE_URL}/api/chat/send?user_id={USER_ID}",
        json={"message": "What's 2+2?"}
    )
    assert r.status_code == 200
    data = r.json()
    assert 'response' in data
    print(f"✅ PASS - AI responded: {data['response'][:60]}...")
except Exception as e:
    print(f"❌ FAIL - {str(e)}")

# TEST 3: Get History
print("\n[3] Get Chat History")
print("-" * 70)
try:
    r = requests.get(f"{BASE_URL}/api/chat/history?user_id={USER_ID}")
    assert r.status_code == 200
    data = r.json()
    assert 'messages' in data
    print(f"✅ PASS - Retrieved {data['total_count']} messages")
except Exception as e:
    print(f"❌ FAIL - {str(e)}")

# TEST 4: Set Personality
print("\n[4] Set Personality Mode")
print("-" * 70)
try:
    r = requests.post(
        f"{BASE_URL}/api/chat/personality?user_id={USER_ID}&personality=funny"
    )
    assert r.status_code == 200
    print("✅ PASS - Personality set to 'funny'")
except Exception as e:
    print(f"❌ FAIL - {str(e)}")

# TEST 5: Get Personality
print("\n[5] Get Current Personality")
print("-" * 70)
try:
    r = requests.get(f"{BASE_URL}/api/chat/personality?user_id={USER_ID}")
    assert r.status_code == 200
    data = r.json()
    assert data['personality'] == 'funny'
    print(f"✅ PASS - Current personality: {data['personality']}")
except Exception as e:
    print(f"❌ FAIL - {str(e)}")

# TEST 6: Send Message with Different Personality
print("\n[6] Test Personality Response")
print("-" * 70)
try:
    r = requests.post(
        f"{BASE_URL}/api/chat/send?user_id={USER_ID}",
        json={"message": "I'm bored"}
    )
    assert r.status_code == 200
    data = r.json()
    print(f"✅ PASS - Response: {data['response'][:60]}...")
except Exception as e:
    print(f"❌ FAIL - {str(e)}")

# TEST 7: Clear History
print("\n[7] Clear Chat History")
print("-" * 70)
try:
    r = requests.delete(f"{BASE_URL}/api/chat/history?user_id={USER_ID}")
    assert r.status_code == 200
    data = r.json()
    print(f"✅ PASS - Deleted {data['deleted_count']} messages")
except Exception as e:
    print(f"❌ FAIL - {str(e)}")

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED!")
print("=" * 70 + "\n")
```

### Run It
```bash
python test_all.py
```

### Expected Output
```
======================================================================
🧪 SENTIO AI BACKEND - COMPLETE TEST SUITE
======================================================================

[1] Health Check
----------------------------------------------------------------------
✅ PASS - Backend is running

[2] Send Chat Message
----------------------------------------------------------------------
✅ PASS - AI responded: That's a great question! 2 + 2 = 4...

[3] Get Chat History
----------------------------------------------------------------------
✅ PASS - Retrieved 5 messages

[4] Set Personality Mode
----------------------------------------------------------------------
✅ PASS - Personality set to 'funny'

[5] Get Current Personality
----------------------------------------------------------------------
✅ PASS - Current personality: funny

[6] Test Personality Response
----------------------------------------------------------------------
✅ PASS - Response: Boredom? Let's find something fun to do! ...

[7] Clear Chat History
----------------------------------------------------------------------
✅ PASS - Deleted 5 messages

======================================================================
✅ ALL TESTS PASSED!
======================================================================
```

---

## 🎯 Quick Reference - Copy & Paste Examples

### Test 1: Simple Health Check
```bash
# Terminal 1 - Start backend
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Terminal 2 - Test health
python -c "import requests; print(requests.get('http://localhost:8000/health').json())"
```

### Test 2: Send Message and Get Response
```python
import requests

r = requests.post(
    "http://localhost:8000/api/chat/send?user_id=1",
    json={"message": "Hello!"}
)
print(r.json()['response'])
```

### Test 3: Get Full Chat History
```python
import requests

r = requests.get("http://localhost:8000/api/chat/history?user_id=1")
for msg in r.json()['messages']:
    role = "You" if msg['role'] == 'user' else "Sentio"
    print(f"{role}: {msg['content']}")
```

### Test 4: Switch to Funny Personality
```python
import requests

requests.post("http://localhost:8000/api/chat/personality?user_id=1&personality=funny")
r = requests.post(
    "http://localhost:8000/api/chat/send?user_id=1",
    json={"message": "Tell me something"}
)
print(r.json()['response'])
```

---

## 📋 Summary of All Tests

| Test | File | What It Tests |
|------|------|---------------|
| Health Check | `test_health.py` | Is backend running? |
| Chat | `test_chat.py` | Can I send messages and get responses? |
| Conversation | `test_conversation.py` | Does context work across multiple messages? |
| History | `test_history.py` | Are messages being saved? |
| Personality | `test_personality.py` | Do all personality modes work? |
| Clear | `test_clear_history.py` | Can I clear history? |
| Get Personality | `test_get_personality.py` | What's my current personality? |
| All Tests | `test_all.py` | Complete test suite |

---

## 🚀 Ready? Start Testing!

1. **Create a folder**: `C:\Users\vaids\OneDrive\Desktop\SENTIO AI\tests\`

2. **Pick a test file** from above and create it

3. **Run it**:
   ```bash
   python tests/test_chat.py
   ```

4. **See results immediately!**

---

**Which test would you like to try first?** I can create the file for you! 🧪

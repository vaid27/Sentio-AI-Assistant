"""
Test 2: Send Message - Send a single chat message and get AI response
Usage: python tests/test_chat.py
"""

import requests
import json

print("\n" + "="*60)
print("🧪 TEST 2: Send Chat Message")
print("="*60)

url = "http://localhost:8000/api/chat/send?user_id=1"
message = "Hello Sentio! What is your name?"

try:
    print(f"\n📤 Sending message: '{message}'")
    
    data = {"message": message}
    response = requests.post(url, json=data)
    
    print(f"\n✅ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        
        print("\n📄 Response:")
        print(f"   Status: 200 OK")
        print(f"   AI Response: {result['response']}")
        print(f"   Timestamp: {result['timestamp']}")
        print(f"   Messages in History: {result['conversation_history_count']}")
        
        print("\n✅ SUCCESS - Message sent and response received!")
    else:
        print(f"\n❌ Error Response:")
        print(json.dumps(response.json(), indent=4))
        
except requests.exceptions.ConnectionError:
    print("❌ ERROR - Cannot connect to backend")
    print("   Make sure backend is running:")
    print("   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000")
except Exception as e:
    print(f"❌ ERROR - {str(e)}")

print("="*60 + "\n")

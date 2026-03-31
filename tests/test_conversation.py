"""
Test 3: Multi-Message Conversation - Send multiple messages
Usage: python tests/test_conversation.py
"""

import requests
import json
import time

print("\n" + "="*60)
print("🧪 TEST 3: Multi-Message Conversation")
print("="*60)

url = "http://localhost:8000/api/chat/send?user_id=1"

messages = [
    "Hello Sentio!",
    "What's your name?",
    "Can you tell me a joke?",
    "What can you do?"
]

print(f"\n📋 Sending {len(messages)} messages...\n")

try:
    for i, message in enumerate(messages, 1):
        print(f"\n[Message {i}]")
        print(f"📤 You: {message}")
        
        data = {"message": message}
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"🤖 Sentio: {result['response']}")
            print(f"📊 Total messages: {result['conversation_history_count']}")
        else:
            print(f"❌ Error: {response.status_code}")
            break
        
        time.sleep(1)  # Wait between messages
    
    print("\n" + "-"*60)
    print("✅ SUCCESS - Conversation complete!")
    
except requests.exceptions.ConnectionError:
    print("❌ ERROR - Cannot connect to backend")
except Exception as e:
    print(f"❌ ERROR - {str(e)}")

print("="*60 + "\n")

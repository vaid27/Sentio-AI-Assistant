"""
Test 4: Get Chat History - Retrieve all saved messages
Usage: python tests/test_history.py
"""

import requests
import json

print("\n" + "="*60)
print("🧪 TEST 4: Get Chat History")
print("="*60)

url = "http://localhost:8000/api/chat/history?user_id=1&limit=20"

try:
    print("\n📜 Retrieving chat history...\n")
    
    response = requests.get(url)
    
    print(f"✅ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        total = data['total_count']
        messages = data['messages']
        
        print(f"📊 Total messages in database: {total}")
        print(f"📋 Displaying: {len(messages)} messages\n")
        
        if messages:
            print("-"*60)
            for msg in messages:
                role = "👤 You" if msg['role'] == 'user' else "🤖 Sentio"
                print(f"\n{role}:")
                print(f"   {msg['content']}")
                print(f"   Time: {msg['timestamp']}")
            print("-"*60)
            
            print(f"\n✅ SUCCESS - Retrieved {len(messages)} messages!")
        else:
            print("📭 No messages found. Try sending a message first!")
    else:
        print(f"\n❌ Error Response:")
        print(json.dumps(response.json(), indent=4))

except requests.exceptions.ConnectionError:
    print("❌ ERROR - Cannot connect to backend")
except Exception as e:
    print(f"❌ ERROR - {str(e)}")

print("="*60 + "\n")

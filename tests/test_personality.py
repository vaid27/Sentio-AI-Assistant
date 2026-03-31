"""
Test 5: Personality Modes - Test all 6 personality modes
Usage: python tests/test_personality.py
"""

import requests
import json

print("\n" + "="*60)
print("🧪 TEST 5: Personality Modes")
print("="*60)

personalities = ["default", "professional", "funny", "strict", "motivational", "siri"]
test_message = "I feel tired today. What should I do?"

try:
    print(f"\nTesting all {len(personalities)} personality modes...\n")
    
    for personality in personalities:
        print("\n" + "-"*60)
        
        # Set personality
        url_set = f"http://localhost:8000/api/chat/personality?user_id=1&personality={personality}"
        response_set = requests.post(url_set)
        
        if response_set.status_code == 200:
            print(f"🎭 Personality: {personality.upper()}")
            
            # Send message to see personality in action
            url_chat = "http://localhost:8000/api/chat/send?user_id=1"
            data = {"message": test_message}
            response_chat = requests.post(url_chat, json=data)
            
            if response_chat.status_code == 200:
                ai_response = response_chat.json()['response']
                print(f"📤 Input: '{test_message}'")
                print(f"🤖 Response: {ai_response}")
            else:
                print(f"❌ Error getting response")
        else:
            print(f"❌ Failed to set {personality} mode")
    
    print("\n" + "-"*60)
    print("\n✅ SUCCESS - All personality modes tested!")
    
except requests.exceptions.ConnectionError:
    print("❌ ERROR - Cannot connect to backend")
except Exception as e:
    print(f"❌ ERROR - {str(e)}")

print("="*60 + "\n")

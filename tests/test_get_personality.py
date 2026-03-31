"""
Test 7: Get Current Personality - Check what personality is active
Usage: python tests/test_get_personality.py
"""

import requests
import json

print("\n" + "="*60)
print("🧪 TEST 7: Get Current Personality")
print("="*60)

url = "http://localhost:8000/api/chat/personality?user_id=1"

try:
    print("\n🎭 Retrieving current personality settings...\n")
    
    response = requests.get(url)
    
    print(f"✅ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"\n📄 Current Settings:")
        print(f"   Personality: {data['personality']}")
        print(f"   Description: {data['description']}")
        
        print(f"\n📋 Available Personalities:")
        for p in data['available_personalities']:
            marker = "✓" if p == data['personality'] else " "
            print(f"   [{marker}] {p}")
        
        print("\n✅ SUCCESS - Personality retrieved!")
    else:
        print(f"\n❌ Error Response:")
        print(json.dumps(response.json(), indent=4))

except requests.exceptions.ConnectionError:
    print("❌ ERROR - Cannot connect to backend")
except Exception as e:
    print(f"❌ ERROR - {str(e)}")

print("="*60 + "\n")

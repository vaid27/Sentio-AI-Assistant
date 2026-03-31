"""
Test 6: Clear History - Delete all chat messages
Usage: python tests/test_clear_history.py
"""

import requests
import json

print("\n" + "="*60)
print("🧪 TEST 6: Clear Chat History")
print("="*60)

url = "http://localhost:8000/api/chat/history?user_id=1"

try:
    print("\n⚠️  This will delete all messages for user_id=1\n")
    
    # First, show how many messages exist
    response_check = requests.get(url + "&limit=1")
    if response_check.status_code == 200:
        total_before = response_check.json()['total_count']
        print(f"📊 Messages before delete: {total_before}\n")
    
    # Confirm action
    confirm = input("Are you sure? Type 'yes' to confirm: ").strip().lower()
    
    if confirm == 'yes':
        print("\n🗑️  Clearing chat history...\n")
        
        response = requests.delete(url)
        
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Message: {data['message']}")
            print(f"   Deleted: {data['deleted_count']} messages")
            
            print("\n✅ SUCCESS - History cleared!")
        else:
            print(f"\n❌ Error Response:")
            print(json.dumps(response.json(), indent=4))
    else:
        print("\n❌ Cancelled - No messages deleted")

except requests.exceptions.ConnectionError:
    print("❌ ERROR - Cannot connect to backend")
except Exception as e:
    print(f"❌ ERROR - {str(e)}")

print("="*60 + "\n")

"""
Test 1: Health Check - Verify backend is running
Usage: python tests/test_health.py
"""

import requests

print("\n" + "="*60)
print("🧪 TEST 1: Health Check")
print("="*60)

try:
    print("\n📡 Connecting to http://localhost:8000/health...")
    
    response = requests.get("http://localhost:8000/health")
    
    print(f"✅ Status Code: {response.status_code}")
    print("\n📄 Response:")
    
    data = response.json()
    for key, value in data.items():
        print(f"   {key}: {value}")
    
    if response.status_code == 200:
        print("\n✅ SUCCESS - Backend is running!")
    else:
        print(f"\n❌ FAILED - Unexpected status code")
        
except requests.exceptions.ConnectionError:
    print("❌ ERROR - Cannot connect to backend")
    print("   Make sure backend is running:")
    print("   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000")
except Exception as e:
    print(f"❌ ERROR - {str(e)}")

print("="*60 + "\n")

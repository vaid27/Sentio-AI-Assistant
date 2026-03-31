"""
Test 8: Complete Test Suite - Run all tests
Usage: python tests/test_all.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"
USER_ID = 1

print("\n")
print("=" * 70)
print("🧪 SENTIO AI BACKEND - COMPLETE TEST SUITE")
print("=" * 70)

tests_passed = 0
tests_failed = 0

# TEST 1: Health Check
print("\n[1/7] Health Check")
print("-" * 70)
try:
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    print("✅ PASS - Backend is running")
    tests_passed += 1
except Exception as e:
    print(f"❌ FAIL - {str(e)}")
    print("   Make sure backend is running:")
    print("   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000")
    tests_failed += 1
    exit(1)

# TEST 2: Send Message
print("\n[2/7] Send Chat Message")
print("-" * 70)
try:
    r = requests.post(
        f"{BASE_URL}/api/chat/send?user_id={USER_ID}",
        json={"message": "What's 2+2?"}
    )
    assert r.status_code == 200
    data = r.json()
    assert 'response' in data
    response_text = data['response'][:60]
    print(f"✅ PASS - AI responded: {response_text}...")
    tests_passed += 1
except Exception as e:
    print(f"❌ FAIL - {str(e)}")
    tests_failed += 1

# TEST 3: Get History
print("\n[3/7] Get Chat History")
print("-" * 70)
try:
    r = requests.get(f"{BASE_URL}/api/chat/history?user_id={USER_ID}")
    assert r.status_code == 200
    data = r.json()
    assert 'messages' in data
    message_count = data['total_count']
    print(f"✅ PASS - Retrieved {message_count} messages")
    tests_passed += 1
except Exception as e:
    print(f"❌ FAIL - {str(e)}")
    tests_failed += 1

# TEST 4: Set Personality
print("\n[4/7] Set Personality Mode")
print("-" * 70)
try:
    r = requests.post(
        f"{BASE_URL}/api/chat/personality?user_id={USER_ID}&personality=funny"
    )
    assert r.status_code == 200
    print("✅ PASS - Personality set to 'funny'")
    tests_passed += 1
except Exception as e:
    print(f"❌ FAIL - {str(e)}")
    tests_failed += 1

# TEST 5: Get Personality
print("\n[5/7] Get Current Personality")
print("-" * 70)
try:
    r = requests.get(f"{BASE_URL}/api/chat/personality?user_id={USER_ID}")
    assert r.status_code == 200
    data = r.json()
    assert data['personality'] == 'funny'
    print(f"✅ PASS - Current personality: {data['personality']}")
    tests_passed += 1
except Exception as e:
    print(f"❌ FAIL - {str(e)}")
    tests_failed += 1

# TEST 6: Send Message with Different Personality
print("\n[6/7] Test Personality Response")
print("-" * 70)
try:
    r = requests.post(
        f"{BASE_URL}/api/chat/send?user_id={USER_ID}",
        json={"message": "I'm bored"}
    )
    assert r.status_code == 200
    data = r.json()
    response_text = data['response'][:60]
    print(f"✅ PASS - Response: {response_text}...")
    tests_passed += 1
except Exception as e:
    print(f"❌ FAIL - {str(e)}")
    tests_failed += 1

# TEST 7: Clear History
print("\n[7/7] Clear Chat History")
print("-" * 70)
try:
    r = requests.delete(f"{BASE_URL}/api/chat/history?user_id={USER_ID}")
    assert r.status_code == 200
    data = r.json()
    deleted_count = data['deleted_count']
    print(f"✅ PASS - Deleted {deleted_count} messages")
    tests_passed += 1
except Exception as e:
    print(f"❌ FAIL - {str(e)}")
    tests_failed += 1

# SUMMARY
print("\n" + "=" * 70)
print("📊 TEST SUMMARY")
print("=" * 70)
print(f"   Total Tests: {tests_passed + tests_failed}")
print(f"   Passed: {tests_passed} ✅")
print(f"   Failed: {tests_failed} ❌")

if tests_failed == 0:
    print("\n🎉 ALL TESTS PASSED!")
else:
    print(f"\n⚠️  {tests_failed} tests failed")

print("=" * 70 + "\n")

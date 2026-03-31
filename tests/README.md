# Sentio AI Backend - Test Suite

This directory contains test files to verify the backend API is working correctly.

## Quick Start

### 1. Make sure backend is running
```bash
cd ..
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 2. Run any test
```bash
python test_health.py
python test_chat.py
python test_conversation.py
python test_history.py
python test_personality.py
python test_get_personality.py
python test_clear_history.py
python test_all.py      # Runs all tests
```

## Test Files

| File | Purpose | What it tests |
|------|---------|---------------|
| `test_health.py` | Health check | Is backend running? |
| `test_chat.py` | Send message | Can I send a message and get response? |
| `test_conversation.py` | Multi-message | Does context work across multiple messages? |
| `test_history.py` | Get history | Are messages saved and retrievable? |
| `test_personality.py` | All personalities | Do all personality modes work? |
| `test_get_personality.py` | Current personality | What's the current personality? |
| `test_clear_history.py` | Clear messages | Can I delete chat history? |
| `test_all.py` | Complete suite | Run all tests at once |

## Expected Results

All tests should show ✅ PASS when backend is running properly.

If you see ❌ FAIL, make sure:
1. Backend is running on port 8000
2. Database is initialized (run `python -m backend.init_db`)
3. You have a valid GEMINI_API_KEY in .env

## Example Output

```
✅ Status Code: 200

📄 Response:
   status: ok
   service: Sentio AI Chat Robot
   version: 1.0.0

✅ SUCCESS - Backend is running!
```

---

Try running `python test_all.py` first to verify everything works!

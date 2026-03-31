"""
Database initialization script - run this once to set up the database and create a test user.
Usage: python -m backend.init_db
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import engine, SessionLocal
from backend.models import Base, User, Message, Memory
import bcrypt
from datetime import datetime

def init_database():
    """Initialize database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")

def create_test_user():
    """Create a test user for development."""
    db = SessionLocal()
    
    try:
        # Check if test user already exists
        existing_user = db.query(User).filter(User.email == "test@sentio.ai").first()
        if existing_user:
            print(f"✓ Test user already exists: {existing_user.username}")
            return existing_user
        
        # Hash password
        password = "test123"
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        # Create test user
        test_user = User(
            email="test@sentio.ai",
            username="testuser",
            hashed_password=hashed_password,
            personality="default"
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"✓ Test user created successfully!")
        print(f"  Email: test@sentio.ai")
        print(f"  Username: testuser")
        print(f"  Password: test123")
        print(f"  User ID: {test_user.id}")
        
        return test_user
    
    except Exception as e:
        print(f"✗ Error creating test user: {str(e)}")
        db.rollback()
        return None
    
    finally:
        db.close()

def add_sample_conversation():
    """Add sample messages to test user."""
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.email == "test@sentio.ai").first()
        if not user:
            print("✗ Test user not found")
            return
        
        # Check if sample messages already exist
        existing_messages = db.query(Message).filter(Message.user_id == user.id).first()
        if existing_messages:
            print("✓ Sample messages already exist")
            return
        
        # Add sample messages
        sample_messages = [
            Message(user_id=user.id, role="user", content="Hello Sentio!"),
            Message(user_id=user.id, role="assistant", content="Hello! I'm Sentio, your AI assistant. How can I help you today?"),
            Message(user_id=user.id, role="user", content="What can you do?"),
            Message(user_id=user.id, role="assistant", content="I can help you with conversations, answer questions, remember important information, and much more. Try asking me anything!"),
        ]
        
        db.add_all(sample_messages)
        db.commit()
        
        print(f"✓ Added {len(sample_messages)} sample messages")
    
    except Exception as e:
        print(f"✗ Error adding sample messages: {str(e)}")
        db.rollback()
    
    finally:
        db.close()

def main():
    """Run all initialization steps."""
    print("\n" + "="*50)
    print("SENTIO AI - DATABASE INITIALIZATION")
    print("="*50 + "\n")
    
    init_database()
    test_user = create_test_user()
    
    if test_user:
        add_sample_conversation()
    
    print("\n" + "="*50)
    print("✓ Database initialization complete!")
    print("="*50 + "\n")
    print("Next steps:")
    print("1. Run the backend: python -m backend.main")
    print("2. Visit: http://localhost:8000/docs")
    print("3. Test the endpoints with user_id=1\n")

if __name__ == "__main__":
    main()

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
import google.generativeai as genai
import logging
import datetime
from backend.config import GEMINI_API_KEY, PERSONALITY_PRESETS, MAX_CONVERSATION_HISTORY
from backend.database import get_db
from backend.models import Message, User, Memory

logger = logging.getLogger(__name__)

router = APIRouter()

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash")

# ==================== PYDANTIC MODELS ====================

class MessageRequest(BaseModel):
    """Request model for sending a message."""
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What's the weather today?"
            }
        }


class MessageResponse(BaseModel):
    """Response model for chat."""
    response: str
    timestamp: str
    conversation_history_count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "I'd be happy to help with that!",
                "timestamp": "2024-03-31T10:30:00",
                "conversation_history_count": 5
            }
        }


class ChatHistoryResponse(BaseModel):
    """Response model for chat history."""
    messages: list
    total_count: int


# ==================== HELPER FUNCTIONS ====================

def get_user_from_request(user_id: int = Query(...), db: Session = Depends(get_db)):
    """Get user by ID. In production, use JWT authentication."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_conversation_context(user_id: int, db: Session) -> str:
    """Get recent conversation history as context."""
    messages = db.query(Message).filter(
        Message.user_id == user_id
    ).order_by(Message.timestamp.desc()).limit(MAX_CONVERSATION_HISTORY).all()
    
    # Reverse to get chronological order
    messages.reverse()
    
    context = ""
    for msg in messages:
        context += f"{msg.role.capitalize()}: {msg.content}\n"
    
    return context


def get_user_memories(user_id: int, db: Session) -> str:
    """Get user's saved memories for context."""
    memories = db.query(Memory).filter(
        Memory.user_id == user_id
    ).order_by(Memory.timestamp.desc()).limit(5).all()
    
    if not memories:
        return ""
    
    memory_text = "\n=== USER MEMORIES ===\n"
    for mem in reversed(memories):
        memory_text += f"- {mem.content}\n"
    
    return memory_text


def generate_ai_response(user_message: str, personality: str, context: str, memories: str) -> str:
    """Generate AI response using Gemini API."""
    try:
        personality_desc = PERSONALITY_PRESETS.get(personality, PERSONALITY_PRESETS["default"])
        
        # Build the prompt
        prompt = f"""{personality_desc}

Keep responses short (1-2 sentences), helpful, natural, and human-like.
Use the real current date and time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{memories}

Conversation history:
{context}

User: {user_message}
Sentio:"""
        
        logger.info(f"Generating response for user message: {user_message[:100]}")
        response = model.generate_content(prompt, stream=False)
        
        if response and response.text:
            ai_response = response.text.strip()
            logger.info(f"Generated response: {ai_response[:100]}")
            return ai_response
        else:
            logger.warning("Empty response from Gemini API")
            return "I'm thinking... Could you ask that again?"
    
    except Exception as e:
        logger.error(f"Error generating AI response: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")


# ==================== API ENDPOINTS ====================

@router.post("/send", response_model=MessageResponse)
async def send_message(
    request: MessageRequest,
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """
    Send a message and get AI response.
    
    - **message**: The user's message
    - **user_id**: The ID of the user sending the message
    
    Returns:
    - **response**: The AI assistant's response
    - **timestamp**: When the response was generated
    - **conversation_history_count**: Number of messages in conversation
    """
    
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_message = request.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    logger.info(f"User {user.username} sent: {user_message[:100]}")
    
    try:
        # Get conversation context and memories
        context = get_conversation_context(user_id, db)
        memories = get_user_memories(user_id, db)
        
        # Generate AI response
        ai_response = generate_ai_response(
            user_message,
            user.personality,
            context,
            memories
        )
        
        # Save user message to database
        user_msg = Message(
            user_id=user_id,
            role="user",
            content=user_message
        )
        db.add(user_msg)
        
        # Save AI response to database
        ai_msg = Message(
            user_id=user_id,
            role="assistant",
            content=ai_response
        )
        db.add(ai_msg)
        
        # Commit both messages
        db.commit()
        db.refresh(ai_msg)
        
        # Get conversation count
        msg_count = db.query(Message).filter(Message.user_id == user_id).count()
        
        logger.info(f"Response saved. Total messages: {msg_count}")
        
        return MessageResponse(
            response=ai_response,
            timestamp=datetime.datetime.utcnow().isoformat(),
            conversation_history_count=msg_count
        )
    
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    user_id: int = Query(..., description="User ID"),
    limit: int = Query(50, ge=1, le=100, description="Number of messages to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Get chat history for a user.
    
    - **user_id**: The ID of the user
    - **limit**: Maximum number of messages to return (default: 50, max: 100)
    
    Returns:
    - **messages**: List of messages in conversation
    - **total_count**: Total number of messages
    """
    
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        # Get messages
        messages = db.query(Message).filter(
            Message.user_id == user_id
        ).order_by(Message.timestamp.desc()).limit(limit).all()
        
        # Reverse for chronological order
        messages.reverse()
        
        # Convert to dictionaries
        message_dicts = [msg.to_dict() for msg in messages]
        
        # Get total count
        total_count = db.query(Message).filter(Message.user_id == user_id).count()
        
        logger.info(f"Retrieved {len(message_dicts)} messages for user {user.username}")
        
        return ChatHistoryResponse(
            messages=message_dicts,
            total_count=total_count
        )
    
    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/history")
async def clear_chat_history(
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """
    Clear all chat history for a user.
    
    - **user_id**: The ID of the user
    """
    
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        # Delete all messages for this user
        deleted_count = db.query(Message).filter(
            Message.user_id == user_id
        ).delete()
        
        db.commit()
        
        logger.info(f"Deleted {deleted_count} messages for user {user.username}")
        
        return {
            "message": "Chat history cleared",
            "deleted_count": deleted_count
        }
    
    except Exception as e:
        logger.error(f"Error clearing chat history: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/personality")
async def set_personality(
    personality: str = Query(..., description="Personality mode"),
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """
    Set user's personality mode.
    
    - **personality**: One of (default, professional, funny, strict, motivational, siri)
    - **user_id**: The ID of the user
    """
    
    # Validate personality
    if personality not in PERSONALITY_PRESETS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid personality. Choose from: {', '.join(PERSONALITY_PRESETS.keys())}"
        )
    
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        # Update personality
        user.personality = personality
        user.updated_at = datetime.datetime.utcnow()
        db.commit()
        
        logger.info(f"User {user.username} switched to {personality} personality")
        
        return {
            "message": f"Personality set to {personality}",
            "personality": personality,
            "description": PERSONALITY_PRESETS[personality]
        }
    
    except Exception as e:
        logger.error(f"Error setting personality: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/personality")
async def get_personality(
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """
    Get user's current personality mode.
    
    - **user_id**: The ID of the user
    """
    
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "personality": user.personality,
        "description": PERSONALITY_PRESETS.get(user.personality, "Unknown"),
        "available_personalities": list(PERSONALITY_PRESETS.keys())
    }

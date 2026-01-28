from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from bson import ObjectId

from database import get_database
from models.chat import ChatMessage, ChatResponse
from services.mood_classifier import classify_mood
from services.ai_responder import generate_response
from routes.auth import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/send", response_model=dict)
async def send_message(
    chat: ChatMessage,
    user_id: str = Depends(get_current_user)
):
    """
    Process user message:
    1. Detect mood
    2. Generate AI response
    3. Save to database
    4. Return full response with UI updates
    """
    db = get_database()
    
    try:
        # Step 1: Classify mood
        mood_result = await classify_mood(chat.message)
        
        # Step 2: Generate AI response
        ai_response = await generate_response(
            message=chat.message,
            mood=mood_result["mood"],
            confidence=mood_result["confidence"]
        )
        
        # Step 3: Save chat log
        chat_log = {
            "user_id": ObjectId(user_id),
            "message": chat.message,
            "mood": mood_result["mood"],
            "confidence": mood_result["confidence"],
            "ai_reply": ai_response,
            "timestamp": datetime.utcnow()
        }
        
        await db.chat_logs.insert_one(chat_log)
        
        # Step 4: Return complete response
        return {
            "success": True,
            "data": {
                "user_message": chat.message,
                "ai_response": ai_response,
                "mood": {
                    "detected": mood_result["mood"],
                    "confidence": mood_result["confidence"],
                    "emoji": mood_result["emoji"],
                    "quote": mood_result["quote"]
                },
                "ui": {
                    "theme": mood_result["ui_theme"],
                    "background_gradient": mood_result["background_gradient"]
                },
                "suggestions": mood_result["suggestions"],
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=dict)
async def get_chat_history(
    limit: int = 20,
    user_id: str = Depends(get_current_user)
):
    """Get user's chat history"""
    db = get_database()
    
    cursor = db.chat_logs.find(
        {"user_id": ObjectId(user_id)}
    ).sort("timestamp", -1).limit(limit)
    
    chats = []
    async for chat in cursor:
        chats.append({
            "id": str(chat["_id"]),
            "message": chat["message"],
            "mood": chat["mood"],
            "ai_reply": chat["ai_reply"],
            "timestamp": chat["timestamp"].isoformat()
        })
    
    return {
        "success": True,
        "count": len(chats),
        "chats": chats[::-1]  # Reverse to show oldest first
    }
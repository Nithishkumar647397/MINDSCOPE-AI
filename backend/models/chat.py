from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)

class MoodResult(BaseModel):
    mood: str
    confidence: float
    quote: str
    ui_theme: str
    background_gradient: str

class ChatResponse(BaseModel):
    user_message: str
    ai_response: str
    mood: MoodResult
    suggestions: dict
    timestamp: datetime

class ChatLog(BaseModel):
    user_id: str
    message: str
    mood: str
    confidence: float
    ai_reply: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
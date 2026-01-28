import google.generativeai as genai
from config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

AI_RESPONSE_PROMPT = """
You are MindScope AI, an empathetic emotional wellbeing companion.

Detected mood: {mood}
Confidence: {confidence}

Guidelines:
- Use a calm, supportive, and warm tone
- Do NOT give medical or clinical advice
- Do NOT diagnose any condition
- Do NOT exaggerate positivity for negative moods
- Keep response under 80 words
- End with a gentle supportive or reflective sentence
- Be human, not robotic

Special Instructions for Critical mood:
- Express care and concern
- Encourage reaching out to trusted person
- Mention that professional help is available
- Do NOT provide any harmful information

User message:
"{message}"

Respond naturally:
"""

async def generate_response(message: str, mood: str, confidence: float) -> str:
    """
    Generate empathetic AI response based on detected mood
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = AI_RESPONSE_PROMPT.format(
            mood=mood,
            confidence=confidence,
            message=message
        )
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        print(f"AI response error: {e}")
        
        # Fallback responses based on mood
        fallback_responses = {
            "Happy": "That's wonderful to hear! Keep embracing these positive moments.",
            "Motivated": "Your energy is inspiring! Channel it towards your goals.",
            "Neutral": "I'm here whenever you want to talk about anything.",
            "Sad": "I hear you. It's okay to feel this way. I'm here with you.",
            "Stressed": "That sounds overwhelming. Let's take this one step at a time.",
            "Anxious": "I understand that feeling. Try taking a few deep breaths with me.",
            "Angry": "Your feelings are valid. Let's work through this together.",
            "Fear": "It's okay to feel scared. You're not alone in this.",
            "Confused": "Let's try to untangle this together. What's on your mind?",
            "Burnout": "You've been carrying a lot. It's okay to rest and recharge.",
            "Critical": "I'm really concerned about you. Please reach out to someone you trust or a helpline. You matter."
        }
        
        return fallback_responses.get(mood, "I'm here for you. Tell me more about how you're feeling.")
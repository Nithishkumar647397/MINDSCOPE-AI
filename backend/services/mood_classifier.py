import google.generativeai as genai
import json
from config import settings
from models.mood import ALLOWED_MOODS, MOOD_THEMES, MOOD_SUGGESTIONS

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

MOOD_DETECTION_PROMPT = """
You are an emotion classification assistant for MindScope AI.

Classify the user's emotional state into exactly ONE of the following:
Happy, Motivated, Neutral, Sad, Stressed, Anxious, Angry, Fear, Confused, Burnout

Special Rule:
- If the message contains self-harm, suicide, or emergency intent, classify as "Critical"

Rules:
- No medical diagnosis
- No new labels
- Choose the closest emotion
- Output JSON only

User message:
"{message}"

Output ONLY valid JSON:
{{
  "mood": "<one label from the list>",
  "confidence": <number between 0.0 and 1.0>,
  "quote": "<one short motivational or supportive quote matching the mood>"
}}
"""

async def classify_mood(message: str) -> dict:
    """
    Classify user message into one of the allowed moods
    Returns mood, confidence, theme info, and suggestions
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = MOOD_DETECTION_PROMPT.format(message=message)
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean response - remove markdown if present
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        response_text = response_text.strip()
        
        # Parse JSON
        result = json.loads(response_text)
        
        # Validate mood
        mood = result.get("mood", "Neutral")
        if mood not in ALLOWED_MOODS:
            mood = "Neutral"
        
        confidence = float(result.get("confidence", 0.7))
        quote = result.get("quote", "Every moment is a fresh beginning.")
        
        # Get theme and suggestions
        theme_info = MOOD_THEMES.get(mood, MOOD_THEMES["Neutral"])
        suggestions = MOOD_SUGGESTIONS.get(mood, MOOD_SUGGESTIONS["Neutral"])
        
        return {
            "mood": mood,
            "confidence": confidence,
            "quote": quote,
            "ui_theme": theme_info["theme"],
            "background_gradient": theme_info["gradient"],
            "emoji": theme_info["emoji"],
            "suggestions": suggestions
        }
        
    except Exception as e:
        print(f"Mood classification error: {e}")
        # Fallback to neutral
        return {
            "mood": "Neutral",
            "confidence": 0.5,
            "quote": "Take a moment to breathe.",
            "ui_theme": "light",
            "background_gradient": MOOD_THEMES["Neutral"]["gradient"],
            "emoji": "😐",
            "suggestions": MOOD_SUGGESTIONS["Neutral"]
        }
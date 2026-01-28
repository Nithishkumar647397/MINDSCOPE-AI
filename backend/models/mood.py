from pydantic import BaseModel
from typing import List
from datetime import datetime

# Fixed mood list - NEVER change this
ALLOWED_MOODS = [
    "Happy", "Motivated", "Neutral", "Sad", "Stressed",
    "Anxious", "Angry", "Fear", "Confused", "Burnout", "Critical"
]

# Mood to score mapping for analytics
MOOD_SCORES = {
    "Happy": 2,
    "Motivated": 1,
    "Neutral": 0,
    "Confused": -0.5,
    "Stressed": -1,
    "Anxious": -1,
    "Sad": -2,
    "Angry": -2,
    "Fear": -2,
    "Burnout": -3,
    "Critical": -3
}

# Background gradients for each mood
MOOD_THEMES = {
    "Happy": {
        "gradient": "linear-gradient(135deg, #FFF3B0, #FFD166)",
        "theme": "light",
        "emoji": "😊"
    },
    "Motivated": {
        "gradient": "linear-gradient(135deg, #C7F9CC, #80ED99)",
        "theme": "light",
        "emoji": "💪"
    },
    "Neutral": {
        "gradient": "linear-gradient(135deg, #F1F5F9, #E2E8F0)",
        "theme": "light",
        "emoji": "😐"
    },
    "Sad": {
        "gradient": "linear-gradient(135deg, #1E3A8A, #312E81)",
        "theme": "dark",
        "emoji": "😢"
    },
    "Stressed": {
        "gradient": "linear-gradient(135deg, #7C2D12, #B45309)",
        "theme": "dark",
        "emoji": "😰"
    },
    "Anxious": {
        "gradient": "linear-gradient(135deg, #4C1D95, #6D28D9)",
        "theme": "dark",
        "emoji": "😟"
    },
    "Angry": {
        "gradient": "linear-gradient(135deg, #7F1D1D, #991B1B)",
        "theme": "dark",
        "emoji": "😠"
    },
    "Fear": {
        "gradient": "linear-gradient(135deg, #0F172A, #1E293B)",
        "theme": "dark",
        "emoji": "😨"
    },
    "Confused": {
        "gradient": "linear-gradient(135deg, #334155, #475569)",
        "theme": "dark",
        "emoji": "😕"
    },
    "Burnout": {
        "gradient": "linear-gradient(135deg, #020617, #1E1B4B)",
        "theme": "dark",
        "emoji": "😩"
    },
    "Critical": {
        "gradient": "linear-gradient(135deg, #450a0a, #7f1d1d)",
        "theme": "dark",
        "emoji": "🆘"
    }
}

# Place suggestions based on mood
MOOD_SUGGESTIONS = {
    "Happy": {
        "places": ["Cafe", "Social hangout spot", "Park"],
        "music_mood": "upbeat"
    },
    "Motivated": {
        "places": ["Gym", "Library", "Co-working space"],
        "music_mood": "energetic"
    },
    "Neutral": {
        "places": ["Cafe", "Bookstore", "Walking trail"],
        "music_mood": "ambient"
    },
    "Sad": {
        "places": ["Quiet park", "Nature spot", "Peaceful garden"],
        "music_mood": "calm"
    },
    "Stressed": {
        "places": ["Temple", "Spa", "Quiet walking path"],
        "music_mood": "relaxing"
    },
    "Anxious": {
        "places": ["Calm cafe", "Garden", "Meditation center"],
        "music_mood": "soothing"
    },
    "Angry": {
        "places": ["Open ground", "Sports facility", "Nature trail"],
        "music_mood": "calming"
    },
    "Fear": {
        "places": ["Safe indoor space", "Familiar cafe", "Home"],
        "music_mood": "comforting"
    },
    "Confused": {
        "places": ["Quiet library", "Park bench", "Peaceful spot"],
        "music_mood": "focus"
    },
    "Burnout": {
        "places": ["Nature retreat", "Beach", "Mountain view"],
        "music_mood": "healing"
    },
    "Critical": {
        "places": ["Safe space", "Trusted friend's place"],
        "music_mood": "gentle"
    }
}

class MoodAnalytics(BaseModel):
    date: str
    mood: str
    score: float
    count: int

class WeeklyTrend(BaseModel):
    data: List[MoodAnalytics]
    average_score: float
    dominant_mood: str
from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from bson import ObjectId
from collections import Counter

from database import get_database
from models.mood import MOOD_SCORES
from routes.auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/weekly-trend", response_model=dict)
async def get_weekly_trend(user_id: str = Depends(get_current_user)):
    """Get mood trend for the past 7 days"""
    db = get_database()
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    # Fetch mood logs
    cursor = db.chat_logs.find({
        "user_id": ObjectId(user_id),
        "timestamp": {"$gte": start_date, "$lte": end_date}
    }).sort("timestamp", 1)
    
    # Process data by day
    daily_data = {}
    async for log in cursor:
        date_key = log["timestamp"].strftime("%Y-%m-%d")
        if date_key not in daily_data:
            daily_data[date_key] = []
        daily_data[date_key].append(log["mood"])
    
    # Build trend data
    trend = []
    all_moods = []
    total_score = 0
    count = 0
    
    for i in range(7):
        date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        day_name = (start_date + timedelta(days=i)).strftime("%a")
        
        if date in daily_data:
            moods = daily_data[date]
            all_moods.extend(moods)
            
            # Get dominant mood for the day
            dominant = Counter(moods).most_common(1)[0][0]
            score = MOOD_SCORES.get(dominant, 0)
            total_score += score
            count += 1
            
            trend.append({
                "date": date,
                "day": day_name,
                "mood": dominant,
                "score": score,
                "entries": len(moods)
            })
        else:
            trend.append({
                "date": date,
                "day": day_name,
                "mood": None,
                "score": 0,
                "entries": 0
            })
    
    # Calculate overall stats
    avg_score = total_score / count if count > 0 else 0
    dominant_mood = Counter(all_moods).most_common(1)[0][0] if all_moods else "Neutral"
    
    return {
        "success": True,
        "data": {
            "trend": trend,
            "summary": {
                "average_score": round(avg_score, 2),
                "dominant_mood": dominant_mood,
                "total_entries": len(all_moods)
            }
        }
    }

@router.get("/mood-distribution", response_model=dict)
async def get_mood_distribution(
    days: int = 30,
    user_id: str = Depends(get_current_user)
):
    """Get mood distribution for specified days"""
    db = get_database()
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    cursor = db.chat_logs.find({
        "user_id": ObjectId(user_id),
        "timestamp": {"$gte": start_date}
    })
    
    mood_counts = Counter()
    async for log in cursor:
        mood_counts[log["mood"]] += 1
    
    total = sum(mood_counts.values())
    
    distribution = []
    for mood, count in mood_counts.most_common():
        distribution.append({
            "mood": mood,
            "count": count,
            "percentage": round((count / total) * 100, 1) if total > 0 else 0
        })
    
    return {
        "success": True,
        "period_days": days,
        "total_entries": total,
        "distribution": distribution
    }
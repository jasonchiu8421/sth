import random
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from last_fm import fetch_current_mood

app = FastAPI()

# ====================== PLACEHOLDER FUNCTIONS ======================
def get_current_mood():
    """Returns a simple mood string + track info for display"""
    mood = random.choice(["calm", "intense", "uplifting", "introspective"])
    print(mood)
    return {
        "track": "Blinding Lights",
        "artist": "The Weeknd",
        "mood": mood,
        "timestamp": "just now"
    }

def fetch_ai_insight(mood: str):
    """Return one insight based on the detected mood"""
    insights_db = {
        "calm": [
            {"short": "Peaceful flow", "long": "This track creates a calm, centered atmosphere. Perfect for focus or winding down."},
            {"short": "Gentle waves", "long": "Soft textures and minimal movement — ideal for meditation or deep work."}
        ],
        "intense": [
            {"short": "High energy", "long": "Driving rhythm and tension. This one pushes adrenaline and motivation."},
            {"short": "Emotional surge", "long": "Intense build-ups and raw power — great for workouts or catharsis."}
        ],
        "uplifting": [
            {"short": "Feel-good boost", "long": "Bright melodies and positive energy. This lifts the spirit instantly."},
            {"short": "Hopeful spark", "long": "Warm chords and rising momentum — perfect for motivation."}
        ],
        "introspective": [
            {"short": "Deep reflection", "long": "Melancholic yet beautiful. Encourages self-reflection and emotional processing."},
            {"short": "Quiet contemplation", "long": "Subtle layers that invite you to look inward."}
        ]
    }

    mood = mood.lower()
    if mood not in insights_db:
        mood = "uplifting"

    return random.choice(insights_db[mood])

# ====================== API ROUTES ======================
@app.get("/mood")
def mood_endpoint():
    return get_current_mood()

@app.get("/insights")
def insights_endpoint():
    return [fetch_ai_insight("uplifting") for _ in range(50)]

# ====================== SERVE STATIC FILES ======================
@app.get("/")
def root():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")

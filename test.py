import pylast

def get_current_mood(username: str, api_key: str, api_secret: str = None) -> dict:
    """
    Get the currently playing track on Last.fm and return its mood
    limited to: uplifting, intense, introspective, or calm.
    """
    network = pylast.LastFMNetwork(api_key=api_key, api_secret=api_secret)
    
    try:
        user = network.get_user(username)
        recent_tracks = user.get_recent_tracks(limit=1, stream=True)
        
        if not recent_tracks:
            return {
                "is_playing": False,
                "track": None,
                "artist": None,
                "mood": "calm",
                "message": "Not listening to anything right now"
            }
        
        track_obj = recent_tracks[0].track
        now_playing = getattr(recent_tracks[0], 'nowplaying', False) or False
        
        title = track_obj.title.lower()
        artist_name = track_obj.artist.name.lower()
        
        if not now_playing:
            return {
                "is_playing": False,
                "track": track_obj.title,
                "artist": track_obj.artist.name,
                "mood": "introspective",   # last track often feels reflective
                "message": "Last played track (not currently listening)"
            }
        
        # Strong keyword lists for each mood
        mood_keywords = {
            "uplifting": [
                "happy", "sunshine", "good", "feel good", "joy", "love", "summer",
                "dance", "party", "upbeat", "bright", "hope", "victory", "rise",
                "blinding", "levitating", "shake", "celebrat"
            ],
            "intense": [
                "rage", "war", "death", "fight", "power", "heavy", "metal", "rock",
                "aggress", "anger", "storm", "fire", "burn", "kill", "blood",
                "black metal", "death metal", "hardcore", "breakdown"
            ],
            "introspective": [
                "sad", "lonely", "heartbreak", "tears", "rain", "blue", "alone",
                "memory", "dream", "ghost", "lost", "sorry", "pain", "dark",
                "melancholy", "reflect", "think", "soul", "deep"
            ],
            "calm": [
                "chill", "relax", "sleep", "ambient", "peace", "quiet", "soft",
                "lofi", "dreamy", "ocean", "rain", "serene", "gentle", "breathe",
                "meditat", "piano", "acoustic"
            ]
        }
        
        # Artist-based strong defaults (very reliable)
        artist_moods = {
            "the weeknd": "intense",
            "taylor swift": "uplifting",
            "billie eilish": "introspective",
            "lofi girl": "calm",
            "kendrick lamar": "intense",
            "drake": "introspective",
            "daft punk": "uplifting",
            "radiohead": "introspective",
            "metallica": "intense",
            "tame impala": "introspective",
            "post malone": "uplifting",
            "adele": "introspective",
            "coldplay": "uplifting",
            "bon iver": "introspective",
        }
        
        # Check artist first (highest priority)
        detected_mood = None
        for art, mood in artist_moods.items():
            if art in artist_name:
                detected_mood = mood
                break
        
        # Then check keywords in title + artist
        if not detected_mood:
            scores = {mood: 0 for mood in mood_keywords}
            
            for mood, words in mood_keywords.items():
                for word in words:
                    if word in title or word in artist_name:
                        scores[mood] += 2 if word in title else 1   # title has more weight
            
            # Pick the mood with highest score
            max_score = max(scores.values())
            if max_score > 0:
                candidates = [m for m, s in scores.items() if s == max_score]
                detected_mood = candidates[0]  # take the first if tie
            else:
                detected_mood = "calm"   # safe default
        
        return {
            "is_playing": True,
            "track": track_obj.title,
            "artist": track_obj.artist.name,
            "mood": detected_mood,
            "confidence": "high" if detected_mood in artist_moods.values() else "medium"
        }
        
    except Exception as e:
        return {
            "is_playing": False,
            "error": str(e),
            "mood": "calm"
        }
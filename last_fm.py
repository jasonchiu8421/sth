import requests

# ================== CONFIGURE THESE ==================
USERNAME = "loymathm"
API_KEY = "3b713e6aceedfffc2fcc42606c4ae27f"
# ====================================================

def get_track_tags(artist=None, track=None):
    if not track:
        print("❌ No track name provided.")
        return

    url = "https://ws.audioscrobbler.com/2.0/"
    print(f"\n🔍 Looking up tags for: {artist or '(unknown)'} — {track}")

    # Step 1: Direct getTopTags with autocorrect
    if artist:
        print("→ Trying direct getTopTags with autocorrect...")
        params = {
            "method": "track.getTopTags",
            "artist": artist,
            "track": track,
            "api_key": API_KEY,
            "format": "json",
            "limit": 20,
            "autocorrect": 1
        }
        data = requests.get(url, params=params, timeout=10).json()
        toptags = data.get("toptags", {}).get("tag", [])
        
        if toptags:
            print("✅ Success with direct call!")
            show_tags(toptags)
            return

    # Step 2: Fallback - Search by track title
    print("→ Direct call failed. Searching by track title only...")
    search_params = {
        "method": "track.search",
        "track": track,
        "api_key": API_KEY,
        "format": "json",
        "limit": 5
    }
    search_data = requests.get(url, params=search_params, timeout=10).json()
    matches = search_data.get("results", {}).get("trackmatches", {}).get("track", [])

    if not matches:
        print("❌ No matches found even by title search.")
        return

    # Take the first (best) match
    if isinstance(matches, list):
        best = matches[0]
    else:
        best = matches

    best_artist = best.get("artist")
    best_track = best.get("name")
    print(f"Best match: {best_artist} — {best_track}")

    # Step 3: Get tags for the best match
    print("→ Fetching tags for best match...")
    tag_params = {
        "method": "track.getTopTags",
        "artist": best_artist,
        "track": best_track,
        "api_key": API_KEY,
        "format": "json",
        "limit": 20,
        "autocorrect": 1
    }
    tag_data = requests.get(url, params=tag_params, timeout=10).json()
    toptags = tag_data.get("toptags", {}).get("tag", [])

    if not toptags:
        print("\n❌ Still no tags returned by the API (even for best match).")
        print("   This is a known Last.fm API limitation — tags show on website but not always via API.")
        return

    print("✅ Tags found via best match!")
    show_tags(toptags)


def show_tags(toptags):
    if isinstance(toptags, dict):
        toptags = [toptags]
    
    print("\n🏷️  Top Tags from Last.fm API:")
    for tag in toptags[:15]:
        name = tag.get("name", "Unknown")
        count = tag.get("count", "?")
        print(f"   • {name} ({count})")


# Main: Check your currently playing / recent track
def fetch_current_mood():
    url = "https://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "user.getRecentTracks",
        "user": USERNAME,
        "api_key": API_KEY,
        "format": "json",
        "limit": 3
    }
    
    data = requests.get(url, params=params, timeout=10).json()
    tracks = data.get("recenttracks", {}).get("track", [])
    
    if not tracks:
        print("No recent tracks.")
        return
    
    t = tracks[0]
    artist = t["artist"]["#text"]
    title = t["name"]
    is_nowplaying = t.get("@attr", {}).get("nowplaying") == "true"
    
    print(f"{'🎵 NOW PLAYING' if is_nowplaying else '⏸️ Last played'}: {artist} — {title}")
    get_track_tags(artist=artist, track=title)
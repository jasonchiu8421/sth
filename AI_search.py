import requests

API_KEY = "f7e9fb5957770fdf25edca465f381dc1591b22ac7705a5c9cfd295bb952980fd"

MOOD_TO_QUERY = {
    "uplifting": "latest AI breakthroughs 2026",
    "intense": "surprising AI research findings",
    "calm": "simple explanation of AI concepts",
    "introspective": "AI ethics and long-term implications"
}

def search_ai_content(music_mood):
    try:
        query = MOOD_TO_QUERY.get(music_mood.lower())
    except:
        query = "interesting AI facts"
    if not query:
        raise ValueError("Unknown mood")

    url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": API_KEY,
        "num": 5
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []
    for item in data.get("organic_results", []):
        results.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet")
        })

    return results
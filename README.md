# MoodSpark AI 🎵

**Music-Enhanced Serendipitous Learning**

MoodSpark AI is an innovative web application that delivers useful, bite-sized knowledge on topics like AI, framed to feel natural with the current song's emotional tone. By detecting the emotional character of the music you're listening to, it provides insights that match the mood, creating moments of serendipitous learning during everyday music listening.

## Features

- **Mood Detection**: Analyzes your currently playing music to determine emotional tone (uplifting, intense, calm, introspective)
- **AI Insights**: Delivers curated, useful information on AI topics tailored to the detected mood

## How It Works

1. **Music Analysis**: The app fetches your currently playing track from Last.fm
2. **Mood Classification**: Determines the emotional tone using track metadata and tags
3. **Content Selection**: Matches AI insights to the detected mood for optimal learning experience
4. **Delivery**: Presents insights in a way that feels congruent with your music

## Prerequisites

- Python 3.8 or higher
- Last.fm account and API key
- SerpAPI key for AI content search

## Installation

1. **Clone the repository**:
   `ash
   git clone <repository-url>
   cd MoodSpark-AI
   `

2. **Install dependencies**:
   `ash
   pip install -r requirements.txt
   `

3. **Set up API keys**:

   - **Last.fm API**: Sign up at [Last.fm API](https://www.last.fm/api) and get your API key
   - **SerpAPI**: Get your API key from [SerpAPI](https://serpapi.com/)

   Update the following files with your keys:
   
   - In last_fm.py: Replace API_KEY and USERNAME with your Last.fm credentials
   - In AI_search.py: Replace API_KEY with your SerpAPI key

## Running the Application

1. **Start the server**:
   `ash
   uvicorn server:app --reload
   `

2. **Open your browser** and navigate to http://localhost:8000

3. **Enter your Last.fm username** when prompted

4. **Enjoy mood-matched AI insights** while listening to music!

## Project Structure

`
MoodSpark-AI/
├── AI_search.py          # SerpAPI integration for AI content search
├── last_fm.py            # Last.fm API integration for music data
├── server.py             # FastAPI backend server
├── requirements.txt      # Python dependencies
├── static/
│   └── index.html        # Frontend web interface
└── README.md             # This file
`

## API Endpoints

- GET / - Serves the main web interface
- GET /mood - Returns current mood and track information
- GET /insights?mood=<mood> - Returns AI insights for the specified mood

## Configuration

The app uses the following mood categories:
- **Uplifting**: High energy, positive insights about AI breakthroughs
- **Intense**: High energy, surprising AI research findings
- **Calm**: Low energy, simple explanations of AI concepts
- **Introspective**: Low energy, AI ethics and long-term implications

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms specified in the LICENSE file.

## Acknowledgments

- Last.fm for music data API
- SerpAPI for search functionality
- FastAPI for the web framework

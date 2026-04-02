import streamlit as st
import random
import json
import time

# ====================== PAGE CONFIG + DARK THEME ======================
st.set_page_config(
    page_title="MoodSpark AI",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ====================== PLACEHOLDER FUNCTIONS ======================
def get_current_mood():
    """Returns a simple mood string + track info for display"""
    mood = random.choice(["calm", "intense", "uplifting", "introspective"])
    print(mood)
    return {
        "track": "Blinding Lights",
        "artist": "The Weeknd",
        "mood": mood,           # string
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

# ====================== MOOD API ENDPOINT ======================
query_params = st.query_params
if "_get_mood" in query_params or st.query_params.get("_get_mood") is not None:
    try:
        mood_data = get_current_mood()
        st.json(mood_data)   # Full data for JS
    except Exception as e:
        st.json({"error": str(e)})
    st.stop()

# ====================== STYLING ======================
st.markdown("""
    <style>
        .stApp { background-color: #0f0f1e; color: #e0e0ff; }
        h1 { color: #a78bfa; text-align: center; margin-bottom: 0; }
        .stButton > button { border-radius: 12px; height: 52px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# ====================== SESSION STATE ======================
if "page" not in st.session_state:
    st.session_state.page = "init"
if "lastfm_username" not in st.session_state:
    st.session_state.lastfm_username = ""
if "ai_insights" not in st.session_state:
    # Generate initial insights (you can regenerate when mood changes)
    st.session_state.ai_insights = [fetch_ai_insight("uplifting") for _ in range(50)]

if "last_mood" not in st.session_state:
    st.session_state.last_mood = None

# ====================== PAGE ROUTING ======================
if st.session_state.page == "init":
    st.title("🎵 MoodSpark AI")
    st.markdown("**Detects the emotional tone of your music and delivers meaningful AI insights.**")
    print("initiated")

    username_input = st.text_input(
        label="Last.fm username",
        placeholder="e.g. loymathm",
        value=st.session_state.lastfm_username,
        help="Your public Last.fm username (case-sensitive)"
    )

    if st.button("Connect to Last.fm", type="primary", use_container_width=True):
        if username_input.strip():
            st.session_state.lastfm_username = username_input.strip()
            st.session_state.page = "main"
            st.success(f"✅ Connected as **{username_input.strip()}**")
            st.rerun()
        else:
            st.error("Please enter a Last.fm username")

else:
    # ====================== MAIN PAGE ======================
    col_title, col_disconnect = st.columns([9, 1])
    with col_title:
        st.title("🎵 MoodSpark AI")
    with col_disconnect:
        if st.button("❌", help="Disconnect & restart", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.markdown("### ")

    insights_json = json.dumps([
        {"short": item["short"], "long": item["long"]} 
        for item in st.session_state.ai_insights
    ])

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
            
            body {{ 
                margin:0; padding:0; background:#0f0f1e; 
                font-family:'Inter',sans-serif; overflow:hidden; 
            }}
            
            .container {{
                width: 100%;
                max-width: 520px;
                height: 500px;
                margin: 0 auto;
                position: relative;
                overflow: hidden;
            }}

            .card {{
                width: 100%;
                height: 100%;
                background: #1e1e38;
                border-radius: 20px;
                border: 2px solid #6366f1;
                box-shadow: 0 10px 30px rgba(99, 102, 241, 0.25);
                padding: 32px 28px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                color: #e0e0ff;
                font-size: 1.25rem;
                line-height: 1.5;
                position: absolute;
                top: 0; left: 0;
                transition: transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
                cursor: grab;
                user-select: none;
                box-sizing: border-box;
            }}
            .short-text {{ 
                transition: opacity 0.3s ease; 
                font-weight: 600;
            }}
            .card.expanded .short-text {{ opacity: 0.3; }}
            
            .long-text {{
                margin-top: 28px;
                font-size: 1.05rem;
                line-height: 1.45;
                opacity: 0;
                max-height: 0;
                overflow: hidden;
                transition: all 0.5s ease;
            }}
            .card.expanded .long-text {{ 
                opacity: 1; 
                max-height: 280px; 
            }}
        </style>
    </head>
    <body>
        <div class="container" id="container">
            <div id="card1" class="card"></div>
            <div id="card2" class="card" style="transform: translateX(100%);"></div>
        </div>
        <div style="text-align:center; margin-top:12px; color:#666; font-size:13px;">
            ← Swipe left (next) • Swipe right (previous) →
        </div>

        <script>
            let currentIndex = 0;
            let insights = {insights_json};
            const total = insights.length;
            
            const card1 = document.getElementById('card1');
            const card2 = document.getElementById('card2');
            const container = document.getElementById('container');

            let startX = 0, isDragging = false, velocity = 0, lastX = 0, lastTime = 0;

            let currentMood = null;

            function loadCard(card, index) {{
                if (!card.querySelector('.short-text')) {{
                    card.innerHTML = `
                        <div class="short-text"></div>
                        <div class="long-text"></div>
                    `;
                }}
                card.querySelector('.short-text').textContent = insights[index].short;
                card.querySelector('.long-text').textContent = insights[index].long;
                card.classList.remove('expanded');
            }}

            function animateCard(card, x, duration = 500) {{
                card.style.transition = `transform ${{duration}}ms cubic-bezier(0.25, 0.46, 0.45, 0.94)`;
                card.style.transform = `translateX(${{x}}px)`;
            }}

            function goToNext() {{
                animateCard(card1, -window.innerWidth * 1.1, 450);
                card2.style.transition = 'none';
                card2.style.transform = `translateX(${{window.innerWidth * 1.1}}px)`;
                loadCard(card2, (currentIndex + 1) % total);
                
                setTimeout(() => animateCard(card2, 0, 450), 10);

                setTimeout(() => {{
                    currentIndex = (currentIndex + 1) % total;
                    loadCard(card1, currentIndex);
                    card1.style.transition = 'none';
                    card1.style.transform = 'translateX(0)';
                    card2.style.transition = 'none';
                    card2.style.transform = `translateX(100%)`;
                }}, 460);
            }}

            function goToPrev() {{
                animateCard(card1, window.innerWidth * 1.1, 450);
                card2.style.transition = 'none';
                card2.style.transform = `translateX(${{-window.innerWidth * 1.1}}px)`;
                loadCard(card2, (currentIndex - 1 + total) % total);
                
                setTimeout(() => animateCard(card2, 0, 450), 10);

                setTimeout(() => {{
                    currentIndex = (currentIndex - 1 + total) % total;
                    loadCard(card1, currentIndex);
                    card1.style.transition = 'none';
                    card1.style.transform = 'translateX(0)';
                    card2.style.transition = 'none';
                    card2.style.transform = `translateX(-100%)`;
                }}, 460);
            }}

            // Drag & Swipe logic (same as before, simplified)
            function startDrag(e) {{
                isDragging = true;
                startX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
                lastX = startX;
                lastTime = Date.now();
                card1.style.transition = 'none';
            }}

            function duringDrag(e) {{
                if (!isDragging) return;
                const clientX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
                const diff = clientX - startX;
                card1.style.transform = `translateX(${{diff}}px)`;
                
                const now = Date.now();
                velocity = (clientX - lastX) / (now - lastTime + 1);
                lastX = clientX;
                lastTime = now;
            }}

            function endDrag(e) {{
                if (!isDragging) return;
                isDragging = false;
                
                const clientX = e.type.includes('mouse') ? e.clientX : 
                                (e.changedTouches ? e.changedTouches[0].clientX : startX);
                const diffX = clientX - startX;
                const absDiffX = Math.abs(diffX);

                if (absDiffX < 8) {{
                    toggleExpand();
                    return;
                }}

                if (absDiffX > 100 || Math.abs(velocity) > 0.7) {{
                    if (diffX < 0) goToNext();
                    else goToPrev();
                }} else {{
                    animateCard(card1, 0, 280);
                }}
            }}

            function toggleExpand() {{
                const visibleCard = card1;
                let tx = 0;
                if (visibleCard.style.transform) {{
                    const match = visibleCard.style.transform.match(/-?[\\d.]+/);
                    tx = match ? parseFloat(match[0]) : 0;
                }}
                if (Math.abs(tx) < 30) {{
                    visibleCard.classList.toggle('expanded');
                }}
            }}

            // ====================== BACKGROUND MOOD UPDATER ======================
            async function fetchCurrentMood() {{
                try {{
                    // ← THIS IS THE ONLY LINE THAT CHANGED
                    const res = await fetch(window.location.origin + "?_get_mood=1");
                    
                    if (res.ok) {{
                        const moodData = await res.json();
                        if (moodData.mood && moodData.mood !== currentMood) {
                            currentMood = moodData.mood;
                            preloadNextMood(moodData);   // or whatever you named this function
                        }}
                    }}
                }} catch (err) {{
                    console.log("Mood fetch error:", err);
                }}
            }}

            function preloadNextMood(moodData) {{
                // Preload the mood into the NEXT card (card2) so we don't interrupt the user
                const nextIndex = (currentIndex + 1) % total;
                
                // For demo: replace the next card with live mood
                card2.querySelector('.short-text').textContent = 
                    `🎧 ${{moodData.track || "Unknown"}} — ${{moodData.artist || "Unknown"}}`;
                card2.querySelector('.long-text').textContent = 
                    `Vibe: ${{moodData.mood}} • ${{moodData.timestamp || ""}}`;
                
                // Optional: You could regenerate insights based on new mood here in the future
            }}

            // Event listeners
            container.addEventListener('mousedown', startDrag);
            window.addEventListener('mousemove', duringDrag);
            window.addEventListener('mouseup', endDrag);

            container.addEventListener('touchstart', startDrag, {{passive: false}});
            container.addEventListener('touchmove', duringDrag, {{passive: false}});
            container.addEventListener('touchend', endDrag);

            document.addEventListener('keydown', e => {{
                if (e.key === 'ArrowRight') goToNext();
                if (e.key === 'ArrowLeft') goToPrev();
            }});

            // Initialize
            loadCard(card1, currentIndex);
            loadCard(card2, (currentIndex + 1) % total);
            card2.style.transform = 'translateX(100%)';

            // Poll for mood every 15 seconds (you can make it faster during testing)
            setInterval(fetchCurrentMood, 15000);
            fetchCurrentMood(); // initial fetch
        </script>
    </body>
    </html>
    """

    st.components.v1.html(html_code, height=570, scrolling=False)

    st.caption("Listen. Feel. Learn.")
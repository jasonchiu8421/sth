import streamlit as st
import random
import json

# ====================== PAGE CONFIG + DARK THEME ======================
st.set_page_config(
    page_title="MoodSpark AI",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .stApp { background-color: #0f0f1e; color: #e0e0ff; }
        h1 { color: #a78bfa; text-align: center; margin-bottom: 0; }
        .stButton > button { border-radius: 12px; height: 52px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# ====================== AI INSIGHT FETCH FUNCTION ======================
def fetch_ai_insight():
    templates = [
        {
            "short": "That driving energy mirrors how transformers unlocked explosive progress in AI, turning massive datasets into breakthrough capabilities almost overnight.",
            "long": "The self-attention mechanism in transformers processes entire sequences in parallel — the key innovation that made modern large language models possible."
        },
        {
            "short": "The raw intensity of this track echoes the high-stakes disruption AI is causing across industries — and the ethical tensions that come with it.",
            "long": "Rapid AI adoption is already reshaping jobs and power structures; the real question is whether we can guide that disruption responsibly."
        },
        {
            "short": "In this calm moment, it's clear how AI is quietly becoming part of everyday applications.",
            "long": "Balanced progress means focusing on human-AI collaboration, making tools that genuinely augment our daily lives."
        },
        {
            "short": "In quieter moments like this, it's worth reflecting on the limitations and philosophical questions AI raises about creativity.",
            "long": "Current models still lack true understanding — keep human judgment at the center."
        }
    ]
    return random.choice(templates)

# ====================== SESSION STATE ======================
if "page" not in st.session_state:
    st.session_state.page = "init"
if "lastfm_username" not in st.session_state:
    st.session_state.lastfm_username = ""
if "ai_insights" not in st.session_state:
    st.session_state.ai_insights = [fetch_ai_insight() for _ in range(50)]

# ====================== PAGE ROUTING ======================
if st.session_state.page == "init":
    st.title("🎵 MoodSpark AI")
    st.markdown(
        "**A simple web-based prototype that detects the emotional tone of the music "
        "currently or recently playing via Last.fm and delivers short, useful AI-related insights.**"
    )
    st.subheader("🔑 First-time setup")
    username_input = st.text_input(
        label="Last.fm username",
        placeholder="e.g. loymathm",
        value=st.session_state.lastfm_username,
        help="Your public Last.fm username (case-sensitive)"
    )
    if st.button("Connect to Last.fm", type="primary", use_container_width=True, icon="🔑"):
        if username_input.strip():
            st.session_state.lastfm_username = username_input.strip()
            st.session_state.page = "main"
            st.success(f"✅ Connected! Welcome, **{username_input.strip()}**")
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
            st.session_state.page = "init"
            st.session_state.lastfm_username = ""
            st.rerun()

    st.markdown("### ")

    insights_json = json.dumps(st.session_state.ai_insights)

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
            
            body {{ 
                margin:0; 
                padding:0; 
                background:#0f0f1e; 
                font-family:'Inter',sans-serif; 
                overflow:hidden; 
            }}
            
            .container {{
                width: 100%;
                max-width: 520px;        /* Increased from 460px - feels better */
                height: 500px;           /* Slightly taller for comfort */
                margin: 0 auto;
                position: relative;
                overflow: hidden;
            }}

            .card {{
                width: 100%;             /* This is the key fix */
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
                top: 0;
                left: 0;
                transition: transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
                cursor: grab;
                user-select: none;
                box-sizing: border-box;   /* Important: prevents padding from increasing width */
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
            <!-- Two cards for smooth sliding transition -->
            <div id="card1" class="card"></div>
            <div id="card2" class="card" style="transform: translateX(100%);"></div>
        </div>
        <div style="text-align:center; margin-top:12px; color:#666; font-size:13px;">
            ← Swipe left (next) • Swipe right (previous) →
        </div>

        <script>
            let currentIndex = 0;
            const insights = {insights_json};
            const total = insights.length;
            
            const card1 = document.getElementById('card1');
            const card2 = document.getElementById('card2');
            
            let startX = 0;
            let isDragging = false;
            let velocity = 0;
            let lastX = 0;
            let lastTime = 0;

            function loadCard(card, index) {{
                card.querySelector('.short-text') ? null : card.innerHTML = `
                    <div class="short-text"></div>
                    <div class="long-text"></div>
                `;
                card.querySelector('.short-text').textContent = insights[index].short;
                card.querySelector('.long-text').textContent = insights[index].long;
                card.classList.remove('expanded');
            }}

            function animateCard(card, x, duration = 500) {{
                card.style.transition = `transform ${{duration}}ms cubic-bezier(0.25, 0.46, 0.45, 0.94)`;
                card.style.transform = `translateX(${{x}}px)`;
            }}

            function goToNext() {{
                // Current card (card1) slides out to the left
                animateCard(card1, -window.innerWidth * 1.1, 450);
                
                // Next card (card2) starts from the right and slides in
                card2.style.transition = 'none';
                card2.style.transform = `translateX(${{window.innerWidth * 1.1}}px)`;
                loadCard(card2, (currentIndex + 1) % total);
                
                // Trigger slide in
                setTimeout(() => {{
                    animateCard(card2, 0, 450);
                }}, 10);

                // After animation, swap roles
                setTimeout(() => {{
                    currentIndex = (currentIndex + 1) % total;
                    
                    // Make card2 the new main card (card1)
                    card1.innerHTML = card2.innerHTML;
                    card1.style.transition = 'none';
                    card1.style.transform = 'translateX(0)';
                    
                    // Reset card2 to be ready for next slide (off to the right)
                    card2.style.transition = 'none';
                    card2.style.transform = `translateX(100%)`;
                }}, 460);
            }}

            function goToPrev() {{
                // Current card (card1) slides out to the right
                animateCard(card1, window.innerWidth * 1.1, 450);
                
                // Previous card (card2) starts from the left and slides in
                card2.style.transition = 'none';
                card2.style.transform = `translateX(${{-window.innerWidth * 1.1}}px)`;
                loadCard(card2, (currentIndex - 1 + total) % total);
                
                setTimeout(() => {{
                    animateCard(card2, 0, 450);
                }}, 10);

                setTimeout(() => {{
                    currentIndex = (currentIndex - 1 + total) % total;
                    
                    card1.innerHTML = card2.innerHTML;
                    card1.style.transition = 'none';
                    card1.style.transform = 'translateX(0)';
                    
                    card2.style.transition = 'none';
                    card2.style.transform = `translateX(-100%)`;
                }}, 460);
            }}

            // Mouse + Touch Events (applied to container for better UX)
            const container = document.getElementById('container');
            
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
                
                const clientX = e.type.includes('mouse') ? e.clientX : (e.changedTouches ? e.changedTouches[0].clientX : startX);
                const diff = clientX - startX;
                const absDiff = Math.abs(diff);
                
                if (absDiff > 100 || Math.abs(velocity) > 0.7) {{
                    if (diff < 0) {{
                        goToNext();   // Swipe Left → Next
                    }} else {{
                        goToPrev();   // Swipe Right → Previous
                    }}
                }} else {{
                    // Snap back
                    animateCard(card1, 0, 280);
                }}
            }}

            // Event Listeners
            container.addEventListener('mousedown', startDrag);
            window.addEventListener('mousemove', duringDrag);
            window.addEventListener('mouseup', endDrag);

            container.addEventListener('touchstart', startDrag, {{ passive: false }});
            container.addEventListener('touchmove', duringDrag, {{ passive: false }});
            container.addEventListener('touchend', endDrag);

            // Click to expand on the visible card
            function toggleExpand() {{
                const visibleCard = card1;
                if (Math.abs(parseFloat(visibleCard.style.transform.replace('translateX(', '').replace('px)', '')) || 0) < 30) {{
                    visibleCard.classList.toggle('expanded');
                }}
            }}
            
            card1.addEventListener('click', toggleExpand);
            card2.addEventListener('click', toggleExpand);  // in case it's partially visible

            // Keyboard support
            document.addEventListener('keydown', e => {{
                if (e.key === 'ArrowRight') goToNext();
                if (e.key === 'ArrowLeft') goToPrev();
            }});

            // Initialize - load first card
            loadCard(card1, currentIndex);
            // Pre-load second card off-screen (for next)
            loadCard(card2, (currentIndex + 1) % total);
            card2.style.transform = 'translateX(100%)';
        </script>
    </body>
    </html>
    """

    st.components.v1.html(html_code, height=540, scrolling=False)

    st.markdown("### ")
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("⏭️ Next", use_container_width=True):
            st.rerun()
    with c2: 
        st.button("❌ Doesn’t fit", use_container_width=True)
    with c3: 
        st.button("💾 Save", use_container_width=True)

    st.caption("Listen. Feel. Learn.")
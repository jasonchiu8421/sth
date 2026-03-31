import streamlit as st

# ====================== PAGE CONFIG + DARK THEME ======================
st.set_page_config(
    page_title="MoodSpark AI",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Enhanced dark/relaxed theme
st.markdown("""
    <style>
        .stApp {
            background-color: #0f0f1e;
            color: #e0e0ff;
        }
        h1 {
            color: #a78bfa;
            text-align: center;
            margin-bottom: 0;
        }
        .insight-card {
            background-color: #1e1e38;
            padding: 32px 28px;
            border-radius: 20px;
            border: 2px solid #6366f1;
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.25);
            text-align: center;
            min-height: 260px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .insight-text {
            font-size: 1.25rem;
            line-height: 1.5;
            color: #e0e0ff;
        }
        .stButton > button {
            border-radius: 12px;
            height: 52px;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# ====================== SESSION STATE ======================
if "page" not in st.session_state:
    st.session_state.page = "init"
if "lastfm_username" not in st.session_state:
    st.session_state.lastfm_username = ""
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# ====================== DUMMY INSIGHTS (for now) ======================
dummy_insights = [
    {
        "text": "That driving energy mirrors how transformers unlocked explosive progress in AI, turning massive datasets into breakthrough capabilities almost overnight.",
        "more": "The self-attention mechanism in transformers processes entire sequences in parallel — the key innovation that made modern large language models possible."
    },
    {
        "text": "The raw intensity of this track echoes the high-stakes disruption AI is causing across industries — and the ethical tensions that come with it.",
        "more": "Rapid AI adoption is already reshaping jobs and power structures; the real question is whether we can guide that disruption responsibly."
    },
    {
        "text": "In this calm moment, it's clear how AI is quietly becoming part of everyday applications — from smart assistants to personalized recommendations.",
        "more": "Balanced progress means focusing on human-AI collaboration, making tools that genuinely augment our daily lives."
    },
    {
        "text": "In quieter moments like this, it's worth reflecting on the limitations and philosophical questions AI raises about creativity and what it means to be human.",
        "more": "Current models still lack true understanding, reminding us to keep human judgment at the center of AI development."
    }
]

# ====================== PAGE ROUTING ======================
if st.session_state.page == "init":
    # Initialization page (unchanged)
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
    # ====================== MAIN PAGE – INSIGHT CARD ONLY ======================
    # Minimal header with title + tiny disconnect
    col_title, col_disconnect = st.columns([9, 1])
    with col_title:
        st.title("🎵 MoodSpark AI")
    with col_disconnect:
        if st.button("❌", help="Disconnect & restart", use_container_width=True):
            st.session_state.page = "init"
            st.session_state.lastfm_username = ""
            st.rerun()

    # Swipeable Insight Card
    st.markdown("### ")  # small breathing space

    current = dummy_insights[st.session_state.current_index]

    # Left arrow | Card | Right arrow
    left_col, card_col, right_col = st.columns([1, 8, 1], vertical_alignment="center")

    with left_col:
        if st.button("←", use_container_width=True, key="left_swipe"):
            st.session_state.current_index = (st.session_state.current_index - 1) % len(dummy_insights)
            st.rerun()

    with card_col:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-text">{current["text"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Tap-to-expand
        with st.expander("👆 Tap for deeper details", expanded=False):
            st.write(current["more"])

    with right_col:
        if st.button("→", use_container_width=True, key="right_swipe"):
            st.session_state.current_index = (st.session_state.current_index + 1) % len(dummy_insights)
            st.rerun()

    # Controls (as per spec)
    st.markdown("### ")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⏭️ Skip", use_container_width=True):
            st.session_state.current_index = (st.session_state.current_index + 1) % len(dummy_insights)
            st.rerun()
    with c2:
        st.button("❌ Doesn’t fit", use_container_width=True)
    with c3:
        st.button("💾 Save", use_container_width=True)

    # Minimal footer
    st.caption("Browser tab must remain open • Last.fm • AI insights only")

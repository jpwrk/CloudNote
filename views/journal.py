import streamlit as st
from datetime import datetime
from components.header import branded_header
from utils.quotes_api import fetch_quote, THEME_TAGS

MOODS = ["☀️ great", "🌤️ good", "🌥️ okay", "🌧️ low", "⛈️ rough"]


def show():
    st.markdown(
        branded_header("what's on your mind? ˚˖𓍢ִ໋❀", "a calm space for your daily reflections"),
        unsafe_allow_html=True,
    )

    if "entries" not in st.session_state:
        st.session_state.entries = []

    # ── Initialize refresh counter (incremented to bust cache on demand) ──
    if "prompt_refresh" not in st.session_state:
        st.session_state.prompt_refresh = 0

    # API-Driven Prompt Section
    # User selects a theme → drives the Quotable API call

    st.markdown(
        "<p style='font-size: 0.8rem; color: #8A7CA8; text-transform: uppercase; "
        "letter-spacing: 0.5px; margin-bottom: 0.2rem;'>today's prompt theme</p>",
        unsafe_allow_html=True,
    )

    theme_label = st.radio(
        "prompt theme",
        options=list(THEME_TAGS.keys()),
        index=0,
        horizontal=True,
        label_visibility="collapsed",
        key="prompt_theme",
    )

    tag = THEME_TAGS[theme_label]

    # Fetch quote — cache_key forces a new call when user clicks refresh
    result = fetch_quote(tag, cache_key=st.session_state.prompt_refresh)

    # Display result
    if "error" in result:
        if result["error"] == "empty":
            st.warning(result["message"])
        else:
            st.error(result["message"])

        # Fallback static prompt so the page stays usable
        st.markdown(
            _prompt_card("What's one small thing that felt good today?", "CloudNote"),
            unsafe_allow_html=True,
        )

    else:
        st.success("✦ today's prompt loaded", icon=None)
        st.markdown(
            _prompt_card(result["content"], result["author"]),
            unsafe_allow_html=True,
        )

    # Refresh button — increments cache_key so fetch_quote runs fresh
    if st.button("✨ new prompt", key="refresh_prompt"):
        st.session_state.prompt_refresh += 1
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Journal Entry Section
    title = st.text_input(
        "Entry Title",
        placeholder="entry name",
        label_visibility="collapsed",
    )

    mood = st.select_slider(
        "how are you feeling?",
        options=MOODS,
        value="🌥️ okay",
    )

    body = st.text_area(
        "write freely here...",
        placeholder="what's on your mind? ⋆˚꩜｡",
        height=280,
        label_visibility="collapsed",
    )

    word_count = len(body.split()) if body.strip() else 0
    st.markdown(
        f"<p style='font-size: 0.8rem; color: #8A7CA8; text-align: right;'>"
        f"{word_count} words</p>",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("💾 save entry", use_container_width=True):
        if not body.strip():
            st.warning("your entry is empty — write a little something first. 🌿")
        else:
            _save_entry(title, mood, body)
            st.session_state.page = "History"
            st.rerun()


# Helper functions

def _prompt_card(content: str, author: str) -> str:
    return f"""
    <div style="
        background: linear-gradient(135deg, #F5F0FF 0%, #EEE9FF 100%);
        border-left: 4px solid #A78BFA;
        border-radius: 0 12px 12px 0;
        padding: 1.1rem 1.4rem;
        margin: 0.8rem 0 0.4rem 0;
    ">
        <p style="
            font-family: 'Lora', serif;
            font-style: italic;
            color: #4B4453;
            font-size: 1rem;
            margin: 0 0 0.5rem 0;
            line-height: 1.6;
        ">"{content}"</p>
        <p style="
            font-family: 'Lora', serif;
            font-size: 0.8rem;
            color: #8A7CA8;
            margin: 0;
            text-align: right;
        ">— {author}</p>
    </div>
    """


def _save_entry(title, mood, body):
    entry = {
        "date":  datetime.now().strftime("%Y-%m-%d"),
        "time":  datetime.now().strftime("%I:%M %p"),
        "title": title.strip() if title.strip() else "untitled",
        "mood":  mood,
        "body":  body.strip(),
    }
    st.session_state.entries.insert(0, entry)
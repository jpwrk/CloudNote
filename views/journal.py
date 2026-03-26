import streamlit as st
from datetime import datetime
from components.header import branded_header
from components.prompt_box import prompt_box
from utils.prompts import get_daily_prompt

MOODS = ["☀️ great", "🌤️ good", "🌥️ okay", "🌧️ low", "⛈️ rough"]

def show():
    st.markdown(
        branded_header("what's on your mind? ˚˖𓍢ִ໋❀", "a calm space for your daily reflections"),
        unsafe_allow_html=True
    )

    # Initialize session state
    if "entries" not in st.session_state:
        st.session_state.entries = []

    # Today's prompt
    st.markdown(
        prompt_box(get_daily_prompt()),
        unsafe_allow_html=True
    )

    # Entry form
    title = st.text_input(
        "Entry Title",
        placeholder="entry name",
        label_visibility="collapsed"
    )

    mood = st.select_slider(
        "how are you feeling?",
        options=MOODS,
        value="🌥️ okay"
    )

    body = st.text_area(
        "write freely here...",
        placeholder="what's on your mind? ⋆˚꩜｡",
        height=280,
        label_visibility="collapsed"
    )

    # Live word count
    word_count = len(body.split()) if body.strip() else 0
    st.markdown(
        f"<p style='font-size: 0.8rem; color: #8A7CA8; text-align: right;'>{word_count} words</p>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("💾 save entry", use_container_width=True):
        if not body.strip():
            st.warning("your entry is empty — write a little something first. 🌿")
        else:
            _save_entry(title, mood, body)
            st.session_state.page = "History"
            st.rerun()


def _save_entry(title, mood, body):
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%I:%M %p"),
        "title": title.strip() if title.strip() else "untitled",
        "mood": mood,
        "body": body.strip()
    }
    st.session_state.entries.insert(0, entry)
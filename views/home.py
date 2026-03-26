import streamlit as st
from components.header import branded_header
from components.cards import kpi_card
from components.prompt_box import prompt_box
from utils.prompts import get_daily_prompt

def show():
    # Header
    st.markdown(
        branded_header("☁️ CloudNote", "a calm space for your daily reflections .✦ ݁˖"),
        unsafe_allow_html=True
    )

    # Initialize session state
    if "entries" not in st.session_state:
        st.session_state.entries = []

    # Stats row
    total = len(st.session_state.entries)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            kpi_card("Total Entries", total, "📓", color="#7C6BAA"),
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            kpi_card("Entries This Week", _entries_this_week(), "🌙", color="#7C6BAA"),
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Today's prompt preview
    st.markdown(
        prompt_box(get_daily_prompt()),
        unsafe_allow_html=True
    )

    # CTA button
    if st.button("start today's entry", use_container_width=True):
        st.session_state.page = "Journal"
        


def _entries_this_week():
    from datetime import datetime, timedelta
    if "entries" not in st.session_state:
        return 0
    cutoff = datetime.now() - timedelta(days=7)
    return sum(
        1 for e in st.session_state.entries
        if datetime.strptime(e["date"], "%Y-%m-%d") >= cutoff
    )
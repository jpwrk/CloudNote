import streamlit as st
from components.header import branded_header

def show():
    st.markdown(
        branded_header("⚙️ settings", "adjust CloudNote to fit your life."),
        unsafe_allow_html=True
    )

    # Initialize session state defaults
    if "entries" not in st.session_state:
        st.session_state.entries = []
    if "reminder_enabled" not in st.session_state:
        st.session_state.reminder_enabled = False
    if "confirm_clear" not in st.session_state:
        st.session_state.confirm_clear = False

    # --- Daily Reminder ---
    st.markdown(
        "<p style='font-size: 0.85rem; color: #8A7CA8; text-transform: uppercase; "
        "letter-spacing: 0.5px; margin-bottom: 0.3rem;'>daily reminder</p>",
        unsafe_allow_html=True
    )

    reminder = st.toggle(
        "remind me to journal each day ˚˖𓍢ִ໋❀",
        value=st.session_state.reminder_enabled
    )
    st.session_state.reminder_enabled = reminder

    if reminder:
        st.markdown(
            "<p style='font-size: 0.9rem; color: #7C6BAA; margin-top: 0.3rem;'>"
            "🌙 reminder set — we'll nudge you gently each day.</p>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<p style='font-size: 0.9rem; color: #8A7CA8; margin-top: 0.3rem;'>"
            "reminders are off - journal whenever feels right. 🌿</p>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #E9D5FF;'>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- Clear All Entries ---
    st.markdown(
        "<p style='font-size: 0.85rem; color: #8A7CA8; text-transform: uppercase; "
        "letter-spacing: 0.5px; margin-bottom: 0.3rem;'>Data</p>",
        unsafe_allow_html=True
    )

    entry_count = len(st.session_state.entries)
    st.markdown(
        f"<p style='font-size: 0.95rem; color: #4B4453;'>You currently have "
        f"<strong>{entry_count}</strong> saved "
        f"{'entry' if entry_count == 1 else 'entries'}.</p>",
        unsafe_allow_html=True
    )

    if not st.session_state.confirm_clear:
        if st.button("clear all entries", use_container_width=True):
            if entry_count == 0:
                st.info("nothing to clear — your journal is already empty. 🌱")
            else:
                st.session_state.confirm_clear = True
                st.rerun()
    else:
        st.warning("are you sure? this will permanently delete all your entries.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ yes, clear everything", use_container_width=True):
                st.session_state.entries = []
                st.session_state.confirm_clear = False
                st.success("all entries cleared. fresh start. ☁️")
                st.rerun()
        with col2:
            if st.button("↩️ cancel", use_container_width=True):
                st.session_state.confirm_clear = False
                st.rerun()
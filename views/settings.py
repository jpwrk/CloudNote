import streamlit as st
from components.header import branded_header

def show():
    st.markdown(
        branded_header("⚙️ settings", "adjust CloudNote to fit your life."),
        unsafe_allow_html=True
    )

    if "entries" not in st.session_state:
        st.session_state.entries = []
    if "reminder_enabled" not in st.session_state:
        st.session_state.reminder_enabled = False
    if "confirm_clear" not in st.session_state:
        st.session_state.confirm_clear = False

    st.markdown(
        "<p style='font-size: 0.85rem; color: #8A7CA8; text-transform: uppercase; "
        "letter-spacing: 0.5px; margin-bottom: 0.3rem;'>daily reminder</p>",
        unsafe_allow_html=True
    )

    reminder = st.toggle(
        "remind me to journal each day",
        value=st.session_state.reminder_enabled,
        key="reminder_toggle"
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
            "reminders are off. journal whenever feels right. 🌿</p>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #E9D5FF;'>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- Writing Goals ---
    st.markdown(
        "<p style='font-size: 0.85rem; color: #8A7CA8; text-transform: uppercase; "
        "letter-spacing: 0.5px; margin-bottom: 0.3rem;'>writing goals</p>",
        unsafe_allow_html=True
    )

    goal_enabled = st.toggle(
        "set a writing goal",
        value=st.session_state.get("goal_enabled", False),
        key="goal_toggle"  # key lets us read this toggle's state to show/hide dependent controls
    )
    st.session_state.goal_enabled = goal_enabled

    # Dynamic UI: sliders only appear when goal toggle is on
    if goal_enabled:
        st.markdown(
            "<p style='font-size: 0.9rem; color: #7C6BAA; margin-top: 0.3rem; margin-bottom: 1rem;'>"
            "set your targets and we'll track your progress. 🌱</p>",
            unsafe_allow_html=True
        )
        word_goal = st.slider(
            "minimum words per entry",
            min_value=25, max_value=500, step=25,
            value=st.session_state.get("word_goal", 100),
            key="word_goal_slider"  # key preserves goal value across reruns without resetting
        )
        st.session_state.word_goal = word_goal
        st.markdown(
            f"<p style='font-size: 0.85rem; color: #8A7CA8;'>✦ target: "
            f"<strong>{word_goal} words</strong> per entry</p>",
            unsafe_allow_html=True
        )
        days_goal = st.slider(
            "days per week to journal",
            min_value=1, max_value=7,
            value=st.session_state.get("days_goal", 3),
            key="days_goal_slider"  # key preserves days goal independently from word goal slider
        )
        st.session_state.days_goal = days_goal
        st.markdown(
            f"<p style='font-size: 0.85rem; color: #8A7CA8;'>✦ target: "
            f"<strong>{days_goal} days</strong> per week</p>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<p style='font-size: 0.9rem; color: #8A7CA8; margin-top: 0.3rem;'>"
            "no goals set — journal freely at your own pace. ☁️</p>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #E9D5FF;'>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<p style='font-size: 0.85rem; color: #8A7CA8; text-transform: uppercase; "
        "letter-spacing: 0.5px; margin-bottom: 0.3rem;'>data</p>",
        unsafe_allow_html=True
    )

    entry_count = len(st.session_state.entries)
    st.markdown(
        f"<p style='font-size: 0.95rem; color: #4B4453;'>you currently have "
        f"<strong>{entry_count}</strong> saved "
        f"{'entry' if entry_count == 1 else 'entries'}.</p>",
        unsafe_allow_html=True
    )

    if not st.session_state.confirm_clear:
        if st.button("🗑️ clear all entries", use_container_width=True, key="clear_btn"):
            if entry_count == 0:
                st.info("nothing to clear — your journal is already empty. 🌱")
            else:
                st.session_state.confirm_clear = True
                st.rerun()
    else:
        st.warning("are you sure? this will permanently delete all your entries.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ yes, clear everything", use_container_width=True, key="confirm_clear_btn"):
                st.session_state.entries = []
                st.session_state.confirm_clear = False
                st.success("all entries cleared. fresh start. ☁️")
                st.rerun()
        with col2:
            if st.button("↩️ cancel", use_container_width=True, key="cancel_clear_btn"):
                st.session_state.confirm_clear = False
                st.rerun()
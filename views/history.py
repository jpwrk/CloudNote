import streamlit as st
from datetime import datetime, timedelta
from components.header import branded_header
from components.entry_card import entry_card

MOODS = ["All", "☀️ great", "🌤️ good", "🌥️ okay", "🌧️ low", "⛈️ rough"]
TIME_PERIODS = ["this week", "this month", "custom"]

# --- Callbacks ---

def reset_filters():
    # on_click callback: resets all filter widgets to default values at once
    st.session_state.history_mood_filter = "All"
    st.session_state.history_time_period = "this week"
    st.session_state.history_start_date = datetime.now().date() - timedelta(days=7)
    st.session_state.history_end_date = datetime.now().date()
    st.session_state.date_range_error = False

def validate_date_range():
    # on_change callback: warns user if start date is after end date
    start = st.session_state.history_start_date
    end = st.session_state.history_end_date
    st.session_state.date_range_error = start > end

def get_date_range(period):
    today = datetime.now().date()
    if period == "this week":
        return today - timedelta(days=7), today
    elif period == "this month":
        return today - timedelta(days=30), today
    else:
        return (
            st.session_state.get("history_start_date", today - timedelta(days=7)),
            st.session_state.get("history_end_date", today)
        )

def show():
    st.markdown(
        branded_header("📖 your journal", "look back on your reflections."),
        unsafe_allow_html=True
    )

    if "entries" not in st.session_state:
        st.session_state.entries = []
    if "date_range_error" not in st.session_state:
        st.session_state.date_range_error = False

    if not st.session_state.entries:
        st.markdown(
            """
            <div style="text-align: center; padding: 3rem; color: #8A7CA8;">
                <p style="font-size: 1.5rem;">🌿</p>
                <p style="font-size: 1rem;">no entries yet — your story starts when you're ready.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    # --- Filters row ---
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        mood_filter = st.selectbox(
            "mood",
            MOODS,
            label_visibility="collapsed",
            key="history_mood_filter"
        )

    with col2:
        # First dropdown: time period selector
        time_period = st.selectbox(
            "time period",
            TIME_PERIODS,
            label_visibility="collapsed",
            key="history_time_period"
        )

    with col3:
        st.button(
            "↩️ reset",
            use_container_width=True,
            key="reset_filters_btn",
            on_click=reset_filters  # on_click: clears all filters back to defaults in one action
        )

    # --- Dependent controls: only appear when "custom" is selected ---
    if time_period == "custom":
        col_start, col_end = st.columns(2)
        with col_start:
            st.date_input(
                "from",
                value=st.session_state.get("history_start_date", datetime.now().date() - timedelta(days=7)),
                label_visibility="collapsed",
                key="history_start_date",
                on_change=validate_date_range  # on_change: validates date range whenever start date changes
            )
        with col_end:
            st.date_input(
                "to",
                value=st.session_state.get("history_end_date", datetime.now().date()),
                label_visibility="collapsed",
                key="history_end_date",
                on_change=validate_date_range  # on_change: revalidates when end date changes
            )

        if st.session_state.date_range_error:
            st.warning("your start date is after your end date — no entries will match. 🌥️")
            return

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Filter logic ---
    start_date, end_date = get_date_range(time_period)

    filtered = [
        e for e in st.session_state.entries
        if (mood_filter == "All" or e["mood"] == mood_filter)
        and (start_date <= datetime.strptime(e["date"], "%Y-%m-%d").date() <= end_date)
    ]

    if not filtered:
        st.markdown(
            "<p style='color: #8A7CA8; text-align: center;'>no entries match your filters. 🌥️</p>",
            unsafe_allow_html=True
        )
        return

    # --- Entry list ---
    for i, entry in enumerate(filtered):
        preview = entry["body"][:120] + "..." if len(entry["body"]) > 120 else entry["body"]
        date_display = datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%B %d, %Y")

        st.markdown(
            entry_card(
                date=f"{date_display} · {entry['time']}",
                title=entry["title"],
                preview=preview,
                mood=entry["mood"]
            ),
            unsafe_allow_html=True
        )

        col_spacer, col_delete = st.columns([5, 1])
        with col_delete:
            if st.button("🗑️", key=f"delete_{i}", help="delete this entry"):
                original_index = st.session_state.entries.index(entry)
                st.session_state.entries.pop(original_index)
                st.rerun()

        st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
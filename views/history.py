import streamlit as st
from datetime import datetime, timedelta
from components.header import branded_header
from components.entry_card import entry_card

MOODS = ["all", "☀️ great", "🌤️ good", "🌥️ okay", "🌧️ low", "⛈️ rough"]

def show():
    st.markdown(
        branded_header("📖 your journal", "look back on your reflections ⋆˚꩜｡"),
        unsafe_allow_html=True
    )

    if "entries" not in st.session_state:
        st.session_state.entries = []

    if not st.session_state.entries:
        st.markdown(
            """
            <div style="text-align: center; padding: 3rem; color: #8A7CA8;">
                <p style="font-size: 1.5rem;">🌿</p>
                <p style="font-size: 1rem;">no entries yet — your story starts when you're ready ♡ </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    # --- Filters ---
    col1, col2, col3 = st.columns(3)

    with col1:
        mood_filter = st.selectbox("Mood", MOODS, label_visibility="collapsed")

    with col2:
        start_date = st.date_input(
            "From",
            value=datetime.now().date() - timedelta(days=30),
            label_visibility="collapsed"
        )

    with col3:
        end_date = st.date_input(
            "To",
            value=datetime.now().date(),
            label_visibility="collapsed"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Filter logic ---
    filtered = [
        e for e in st.session_state.entries
        if (mood_filter == "all" or e["mood"] == mood_filter)
        and (start_date <= datetime.strptime(e["date"], "%Y-%m-%d").date() <= end_date)
    ]

    if not filtered:
        st.markdown(
            "<p style='color: #8A7CA8; text-align: center;'>no entries match your filters</p>",
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

        # Delete button aligned right
        col_spacer, col_delete = st.columns([5, 1])
        with col_delete:
            if st.button("🗑️", key=f"delete_{i}", help="Delete this entry"):
                original_index = st.session_state.entries.index(entry)
                st.session_state.entries.pop(original_index)
                st.rerun()

        st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
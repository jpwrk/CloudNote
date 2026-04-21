import streamlit as st

st.set_page_config(
    page_title="CloudNote",
    page_icon="☁️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Global CSS ---
st.markdown("""
    <style>
        /* Dreamy font import */
        @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

        html, body, [class*="css"] {
            font-family: 'Lora', serif;
        }

        /* Soften the sidebar */
        section[data-testid="stSidebar"] {
            background-color: #EEE9FF;
            border-right: 1px solid #D8B4FE;
        }

        /* Sidebar text */
        section[data-testid="stSidebar"] * {
            color: #4B4453 !important;
        }

        /* Button styling */
        div.stButton > button {
            background-color: #A78BFA;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.5rem 1rem;
            font-family: 'Lora', serif;
            font-size: 0.95rem;
            transition: background-color 0.2s ease;
        }

        div.stButton > button:hover {
            background-color: #7C6BAA;
            color: white;
        }

        /* Soften text inputs */
        input, textarea {
            border-radius: 12px !important;
            border: 1px solid #D8B4FE !important;
            font-family: 'Lora', serif !important;
        }

        /* Hide default Streamlit footer */
        footer {visibility: hidden;}

        /* Hide "Made with Streamlit" */
        #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Session state defaults ---
if "entries" not in st.session_state:
    st.session_state.entries = []
if "reminder_enabled" not in st.session_state:
    st.session_state.reminder_enabled = False
if "confirm_clear" not in st.session_state:
    st.session_state.confirm_clear = False
if "page" not in st.session_state:
    st.session_state.page = "Home"

# --- Sidebar navigation ---
with st.sidebar:
    st.markdown(
        "<h2 style='font-family: Lora, serif; color: #6D5BA8;'>☁️ CloudNote</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size: 0.85rem; color: #8A7CA8; margin-top: -0.5rem;'>"
        "your daily reflection space</p>",
        unsafe_allow_html=True
    )
    st.markdown("<hr style='border: 1px solid #D8B4FE;'>", unsafe_allow_html=True)

    pages = {
        "🏠 Home": "Home",
        "✏️ Journal": "Journal",
        "📖 History": "History",
        "📊 Insights": "Insights",
        "☁️ Nimbus": "Assistant",
        "⚙️ Settings": "Settings"
    }

    for label, key in pages.items():
        if st.button(label, use_container_width=True, key=f"nav_{key}"):
            st.session_state.page = key
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    entry_count = len(st.session_state.entries)
    st.markdown(
        f"<p style='font-size: 0.8rem; color: #8A7CA8; text-align: center;'>"
        f"{entry_count} {'entry' if entry_count == 1 else 'entries'} written</p>",
        unsafe_allow_html=True
    )

# --- Page routing ---
page = st.session_state.page

if page == "Home":
    from views.home import show
    show()
elif page == "Journal":
    from views.journal import show
    show()
elif page == "History":
    from views.history import show
    show()
elif page == "Settings":
    from views.settings import show
    show()
elif page == "Insights":
    from views.insights import show
    show()
elif page == "Assistant":
    from views.assistant import show
    show()
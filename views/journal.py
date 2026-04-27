import streamlit as st
from datetime import datetime
from components.header import branded_header
from utils.quotes_api import fetch_prompt, THEME_PROMPTS

MOODS = ["☀️ great", "🌤️ good", "🌥️ okay", "🌧️ low", "⛈️ rough"]

# --- Validation constants ---
TITLE_MAX_CHARS = 80
BODY_MIN_WORDS  = 3     # must write at least 3 words
BODY_MAX_CHARS  = 5000  # soft cap to prevent runaway entries


def show():
    st.markdown(
        branded_header("what's on your mind? ˚˖𓍢ִ໋❀", "a calm space for your daily reflections"),
        unsafe_allow_html=True,
    )

    if "entries" not in st.session_state:
        st.session_state.entries = []
    if "prompt_refresh" not in st.session_state:
        st.session_state.prompt_refresh = 0

    # ── Mood selector ─────────────────────────────────────────────────────────
    mood = st.select_slider(
        "how are you feeling?",
        options=MOODS,
        value="🌥️ okay",
        key="mood_slider",  # key preserves mood selection across reruns
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Theme selector ────────────────────────────────────────────────────────
    st.markdown(
        "<p style='font-size: 0.8rem; color: #8A7CA8; text-transform: uppercase; "
        "letter-spacing: 0.5px; margin-bottom: 0.2rem;'>today's prompt theme</p>",
        unsafe_allow_html=True,
    )

    theme_label = st.radio(
        "prompt theme",
        options=list(THEME_PROMPTS.keys()),
        index=0,
        horizontal=True,
        label_visibility="collapsed",
        key="prompt_theme",  # key ensures theme selection persists when mood changes
    )

    mood_clean = mood.split(" ", 1)[1]  # strip emoji for cleaner API call

    # ── API call wrapped in spinner (Feedback Pattern 1: st.spinner) ──────────
    # Spinner communicates to the user that a network request is in progress,
    # preventing confusion when the page appears frozen during fetch.
    with st.spinner("fetching your prompt... ✨"):
        result = fetch_prompt(
            theme_description=theme_label,
            mood=mood_clean,
            cache_key=st.session_state.prompt_refresh,
        )

    # ── API result display (Feedback Pattern 3: st.success / st.error / st.warning)
    if "error" in result:
        if result["error"] == "empty":
            st.warning(result["message"])  # 200 OK but empty — warn, don't block
        else:
            st.error(result["message"])    # network / status error — surface clearly

        # Fallback: keep page usable even when API fails
        fallback = THEME_PROMPTS.get(theme_label, "What's on your mind today?")
        st.markdown(_prompt_card(fallback, None), unsafe_allow_html=True)

    else:
        st.success("✦ today's prompt ready")
        st.markdown(
            _prompt_card(result["prompt"], result["affirmation"]),
            unsafe_allow_html=True,
        )

    if st.button("new affirmation", key="refresh_prompt"):
        st.session_state.prompt_refresh += 1
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Journal entry fields ──────────────────────────────────────────────────
    title = st.text_input(
        "Entry Title",
        placeholder="entry name",
        label_visibility="collapsed",
        key="journal_title",   # key prevents stale title persisting across reruns
        max_chars=TITLE_MAX_CHARS,
    )

    # Validation 1: title character count feedback shown live
    if title and len(title) >= TITLE_MAX_CHARS - 10:
        chars_left = TITLE_MAX_CHARS - len(title)
        if chars_left == 0:
            st.warning(f"title has reached the {TITLE_MAX_CHARS}-character limit.")
        else:
            st.caption(f"{chars_left} characters remaining in title")

    body = st.text_area(
        "write freely here...",
        placeholder="what's on your mind? ⋆˚꩜｡",
        height=280,
        label_visibility="collapsed",
        key="journal_body",    # key allows body to be cleared via session state after save
    )

    # Live word count display
    word_count = len(body.split()) if body.strip() else 0
    wc_color   = "#A78BFA" if word_count >= BODY_MIN_WORDS else "#F3722C"
    st.markdown(
        f"<p style='font-size: 0.8rem; color: {wc_color}; text-align: right;'>"
        f"{word_count} words</p>",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Save button + validation ──────────────────────────────────────────────
    if st.button("💾 save entry", use_container_width=True, key="save_entry_btn"):

        # Validation 2: body cannot be empty or too short
        if not body.strip():
            st.warning("your entry is empty — write a little something first. 🌿")
            st.stop()  # fatal: nothing to save, halt execution here

        if word_count < BODY_MIN_WORDS:
            st.warning(
                f"your entry is very short ({word_count} word{'s' if word_count != 1 else ''}). "
                f"try writing at least {BODY_MIN_WORDS} words — even a few lines help. 🌿"
            )
            st.stop()  # fatal: too short to be a meaningful entry

        # Validation 3: body character cap (shouldn't happen via UI but defensive)
        if len(body) > BODY_MAX_CHARS:
            st.error(
                f"your entry is too long ({len(body):,} characters). "
                f"please keep it under {BODY_MAX_CHARS:,} characters."
            )
            st.stop()

        # Validation 4: duplicate entry guard — same title on the same date
        today_str = datetime.now().strftime("%Y-%m-%d")
        title_clean = title.strip().lower() if title.strip() else "untitled"
        is_duplicate = any(
            e["date"] == today_str and e["title"].lower() == title_clean
            for e in st.session_state.entries
        )
        if is_duplicate:
            st.warning(
                f'you already have an entry called "{title_clean}" today. '
                "rename it or update the existing one in History. 📖"
            )
            st.stop()  # fatal: would create a confusing duplicate

        # ── All validations passed — save ─────────────────────────────────
        _save_entry(title, mood, body)

        # Feedback Pattern 2: st.toast — brief, non-blocking confirmation
        # Toast disappears automatically so it doesn't clutter the next page
        st.toast("entry saved ☁️", icon="⭐️")

        st.session_state.page = "History"
        st.rerun()


# ── helpers ───────────────────────────────────────────────────────────────────

def _prompt_card(question: str, affirmation: str | None) -> str:
    affirmation_html = (
        f"<p style='font-family: Lora, serif; font-size: 0.8rem; "
        f"color: #8A7CA8; margin: 0.6rem 0 0 0; font-style: normal;'>"
        f"✦ {affirmation}</p>"
        if affirmation else ""
    )
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
            margin: 0;
            line-height: 1.6;
        ">{question}</p>
        {affirmation_html}
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

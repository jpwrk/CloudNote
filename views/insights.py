import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from collections import Counter
import re

try:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False

from components.header import branded_header

# --- Stop words to filter from word cloud ---
STOP_WORDS = {
    "i", "me", "my", "myself", "we", "our", "you", "your", "he", "she", "it",
    "they", "them", "the", "a", "an", "and", "or", "but", "in", "on", "at",
    "to", "for", "of", "with", "this", "that", "is", "was", "are", "were",
    "be", "been", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "not", "no", "so", "if", "as", "about", "up", "out",
    "just", "like", "very", "really", "feel", "felt", "feeling", "today",
    "got", "get", "its", "im", "it's", "i'm", "don't", "didn't", "can't",
    "there", "their", "then", "than", "when", "what", "which", "who", "how",
    "all", "one", "also", "still", "even", "more", "some", "into", "from",
    "after", "before", "been", "being", "am", "again", "too", "because"
}

# --- Mood ordering and colors ---
MOOD_ORDER = ["☀️ great", "🌤️ good", "🌥️ okay", "🌧️ low", "⛈️ rough"]
MOOD_COLORS = {
    "☀️ great": "#F9C74F",
    "🌤️ good":  "#90BE6D",
    "🌥️ okay":  "#A78BFA",
    "🌧️ low":   "#577590",
    "⛈️ rough": "#F3722C",
}
MOOD_SCORE = {
    "☀️ great": 5,
    "🌤️ good":  4,
    "🌥️ okay":  3,
    "🌧️ low":   2,
    "⛈️ rough": 1,
}

CLOUDNOTE_PURPLE = "#A78BFA"
CLOUDNOTE_SOFT   = "#EEE9FF"


# ── helpers ──────────────────────────────────────────────────────────────────

def _filter_entries(entries, range_key, custom_start=None, custom_end=None):
    today = datetime.now().date()
    if range_key == "This week":
        cutoff = today - timedelta(days=7)
        return [e for e in entries
                if datetime.strptime(e["date"], "%Y-%m-%d").date() >= cutoff]
    elif range_key == "This month":
        cutoff = today - timedelta(days=30)
        return [e for e in entries
                if datetime.strptime(e["date"], "%Y-%m-%d").date() >= cutoff]
    elif range_key == "Last 3 months":
        cutoff = today - timedelta(days=90)
        return [e for e in entries
                if datetime.strptime(e["date"], "%Y-%m-%d").date() >= cutoff]
    elif range_key == "Custom" and custom_start and custom_end:
        return [e for e in entries
                if custom_start
                <= datetime.strptime(e["date"], "%Y-%m-%d").date()
                <= custom_end]
    return entries  # "All time"


def _plotly_theme():
    """Shared layout kwargs to keep charts on-brand."""
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Lora, serif", color="#4B4453"),
        margin=dict(l=20, r=20, t=30, b=20),
    )


# ── main view ────────────────────────────────────────────────────────────────

def show():
    st.markdown(
        branded_header("📊 your insights", "patterns from your reflections ⋆˚꩜｡"),
        unsafe_allow_html=True,
    )

    if "entries" not in st.session_state:
        st.session_state.entries = []

    entries = st.session_state.entries

    if not entries:
        st.markdown(
            """
            <div style="text-align: center; padding: 3rem; color: #8A7CA8;">
                <p style="font-size: 1.5rem;">🌿</p>
                <p style="font-size: 1rem;">
                    no entries yet — start journaling to see your insights ♡
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # ── Inline time range filter ──────────────────────────────────────────────
    st.markdown(
        "<p style='font-size:0.8rem; color:#8A7CA8; text-transform:uppercase;"
        " letter-spacing:0.5px; margin-bottom:0.2rem;'>time range</p>",
        unsafe_allow_html=True,
    )

    RANGE_OPTIONS = ["This week", "This month", "Last 3 months", "All time", "Custom"]

    range_key = st.radio(
        "time range",
        RANGE_OPTIONS,
        index=1,
        horizontal=True,
        label_visibility="collapsed",
        key="insights_range",
    )

    custom_start = custom_end = None
    if range_key == "Custom":
        cc1, cc2 = st.columns(2)
        with cc1:
            custom_start = st.date_input(
                "from",
                value=datetime.now().date() - timedelta(days=30),
                key="insights_start",
            )
        with cc2:
            custom_end = st.date_input(
                "to",
                value=datetime.now().date(),
                key="insights_end",
            )

    st.markdown("<br>", unsafe_allow_html=True)

    filtered = _filter_entries(entries, range_key, custom_start, custom_end)

    if not filtered:
        st.info("no entries found for this time range. try a wider window. 🌿")
        return

    # ── Summary metrics ───────────────────────────────────────────────────────
    total_words = sum(len(e["body"].split()) for e in filtered)
    avg_words   = round(total_words / len(filtered))
    most_common_mood = Counter(e["mood"] for e in filtered).most_common(1)[0][0]

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("entries", len(filtered))
    with m2:
        st.metric("total words", f"{total_words:,}")
    with m3:
        st.metric("avg words / entry", avg_words)

    st.markdown(
        f"<p style='font-size:0.85rem; color:#8A7CA8; margin-top:0.2rem;'>"
        f"most frequent mood: {most_common_mood}</p>",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # CHART 1 — Mood frequency (bar chart)
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown(
        "<p style='font-size:0.85rem; color:#8A7CA8; text-transform:uppercase;"
        " letter-spacing:0.5px;'>mood frequency</p>",
        unsafe_allow_html=True,
    )

    mood_counts = Counter(e["mood"] for e in filtered)
    moods_present = [m for m in MOOD_ORDER if mood_counts.get(m, 0) > 0]
    counts = [mood_counts[m] for m in moods_present]
    bar_colors = [MOOD_COLORS[m] for m in moods_present]

    fig_mood = go.Figure(
        go.Bar(
            x=moods_present,
            y=counts,
            marker_color=bar_colors,
            marker_line_width=0,
            text=counts,
            textposition="outside",
            textfont=dict(family="Lora, serif", size=13, color="#4B4453"),
        )
    )
    fig_mood.update_layout(
        **_plotly_theme(),
        xaxis=dict(showgrid=False, tickfont=dict(size=13)),
        yaxis=dict(showgrid=True, gridcolor="#F3EDF9", zeroline=False,
                   title="entries"),
        showlegend=False,
        height=320,
    )
    st.plotly_chart(fig_mood, use_container_width=True)

    st.markdown("<hr style='border:1px solid #E9D5FF; margin: 1.5rem 0;'>",
                unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # CHART 2 — Word count by day (line chart)
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown(
        "<p style='font-size:0.85rem; color:#8A7CA8; text-transform:uppercase;"
        " letter-spacing:0.5px;'>words written per day</p>",
        unsafe_allow_html=True,
    )

    daily_words: dict = {}
    daily_mood_score: dict = {}
    daily_mood_count: dict = {}

    for e in filtered:
        d = e["date"]
        wc = len(e["body"].split())
        daily_words[d] = daily_words.get(d, 0) + wc
        daily_mood_score[d] = daily_mood_score.get(d, 0) + MOOD_SCORE[e["mood"]]
        daily_mood_count[d] = daily_mood_count.get(d, 0) + 1

    sorted_dates = sorted(daily_words.keys())
    word_vals    = [daily_words[d] for d in sorted_dates]
    mood_vals    = [round(daily_mood_score[d] / daily_mood_count[d], 2)
                    for d in sorted_dates]
    date_labels  = [datetime.strptime(d, "%Y-%m-%d").strftime("%b %d")
                    for d in sorted_dates]

    overlay = st.toggle("overlay mood score", value=False)

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=date_labels,
        y=word_vals,
        mode="lines+markers",
        name="words written",
        line=dict(color=CLOUDNOTE_PURPLE, width=2.5),
        marker=dict(size=6, color=CLOUDNOTE_PURPLE),
        fill="tozeroy",
        fillcolor="rgba(167,139,250,0.10)",
    ))

    if overlay:
        fig_line.add_trace(go.Scatter(
            x=date_labels,
            y=mood_vals,
            mode="lines+markers",
            name="mood score (1–5)",
            yaxis="y2",
            line=dict(color="#F9C74F", width=2, dash="dot"),
            marker=dict(size=5, color="#F9C74F"),
        ))
        fig_line.update_layout(
            yaxis2=dict(
                title="mood (1=rough · 5=great)",
                overlaying="y",
                side="right",
                range=[0, 6],
                showgrid=False,
                tickfont=dict(size=11),
            )
        )

    fig_line.update_layout(
        **_plotly_theme(),
        xaxis=dict(showgrid=False, tickangle=-30,
                   ticks="outside", tickfont=dict(size=11)),
        yaxis=dict(showgrid=True, gridcolor="#F3EDF9", zeroline=False,
                   title="words written"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="left", x=0, font=dict(size=12)),
        height=320,
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("<hr style='border:1px solid #E9D5FF; margin: 1.5rem 0;'>",
                unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # CHART 3 — Mood over time (line chart, numeric scale)
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown(
        "<p style='font-size:0.85rem; color:#8A7CA8; text-transform:uppercase;"
        " letter-spacing:0.5px;'>mood over time</p>",
        unsafe_allow_html=True,
    )

    mood_label_map = {5: "great", 4: "good", 3: "okay", 2: "low", 1: "rough"}

    fig_mood_line = go.Figure()
    fig_mood_line.add_trace(go.Scatter(
        x=date_labels,
        y=mood_vals,
        mode="lines+markers",
        line=dict(color="#90BE6D", width=2.5),
        marker=dict(size=7, color="#90BE6D"),
        fill="tozeroy",
        fillcolor="rgba(144,190,109,0.10)",
        hovertemplate="%{x}<br>mood: %{y:.1f}<extra></extra>",
    ))
    fig_mood_line.update_layout(
        **_plotly_theme(),
        xaxis=dict(showgrid=False, tickangle=-30, tickfont=dict(size=11)),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F3EDF9",
            zeroline=False,
            range=[0.5, 5.5],
            tickvals=[1, 2, 3, 4, 5],
            ticktext=["rough", "low", "okay", "good", "great"],
            title="mood",
        ),
        showlegend=False,
        height=300,
    )
    st.plotly_chart(fig_mood_line, use_container_width=True)

    st.markdown("<hr style='border:1px solid #E9D5FF; margin: 1.5rem 0;'>",
                unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # CHART 4 — Word cloud
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown(
        "<p style='font-size:0.85rem; color:#8A7CA8; text-transform:uppercase;"
        " letter-spacing:0.5px;'>most used words</p>",
        unsafe_allow_html=True,
    )

    all_text = " ".join(e["body"] for e in filtered)
    tokens = re.findall(r"\b[a-zA-Z']+\b", all_text.lower())
    tokens = [t.strip("'") for t in tokens if t.strip("'") not in STOP_WORDS and len(t) > 2]

    if not tokens:
        st.info("not enough text yet to build a word cloud. keep writing! 🌿")
        return

    if WORDCLOUD_AVAILABLE:
        # ── rendered word cloud via matplotlib ───────────────────────────────
        freq = Counter(tokens)
        wc = WordCloud(
            width=800,
            height=380,
            background_color="white",
            colormap=None,
            color_func=lambda *a, **k: _wc_color(),
            prefer_horizontal=0.85,
            max_words=80,
            font_path=None,
        ).generate_from_frequencies(freq)

        fig_wc, ax = plt.subplots(figsize=(10, 4.5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        fig_wc.patch.set_facecolor("none")
        st.pyplot(fig_wc, use_container_width=True)
    else:
        # ── fallback: top-30 word frequency bar chart ─────────────────────
        st.caption(
            "install `wordcloud` + `matplotlib` for the visual word cloud. "
            "showing top words as a chart instead."
        )
        freq = Counter(tokens).most_common(30)
        words, word_counts = zip(*freq)

        fig_words = go.Figure(
            go.Bar(
                x=list(word_counts)[::-1],
                y=list(words)[::-1],
                orientation="h",
                marker_color=CLOUDNOTE_PURPLE,
                marker_line_width=0,
            )
        )
        fig_words.update_layout(
            **_plotly_theme(),
            xaxis=dict(showgrid=True, gridcolor="#F3EDF9", title="count"),
            yaxis=dict(showgrid=False, tickfont=dict(size=12)),
            showlegend=False,
            height=max(400, len(words) * 22 + 60),
        )
        st.plotly_chart(fig_words, use_container_width=True)


def _wc_color():
    """Returns one of the CloudNote palette colors at random."""
    import random
    palette = ["#A78BFA", "#7C6BAA", "#C4B5FD", "#6D5BA8", "#D8B4FE", "#8B5CF6"]
    return random.choice(palette)
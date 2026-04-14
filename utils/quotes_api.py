import streamlit as st
import requests

# --- API Configuration ---
# ZenQuotes API: https://zenquotes.io/api
# Authentication: None required (public API)
# Rate limit: 5 requests/30 seconds per IP on the free tier

ZENQUOTES_BASE = "https://zenquotes.io/api"

# ZenQuotes doesn't support tag filtering on the free tier,
# so we maintain a local mapping of themes to drive the prompt UI.
THEME_TAGS = {
    "✨ inspiration": "inspirational",
    "🧠 wisdom":      "wisdom",
    "💪 motivation":  "motivational",
    "❤️ kindness":    "love",
    "🌿 mindfulness": "life",
    "😊 happiness":   "happiness",
}

# Fallback prompts per theme — shown if API is unavailable
FALLBACK_PROMPTS = {
    "inspirational": "What's one small thing that felt good today?",
    "wisdom":        "What's something you learned about yourself recently?",
    "motivational":  "What's one step you can take toward a goal this week?",
    "love":          "Who in your life are you most grateful for right now?",
    "life":          "What moment from today do you want to remember?",
    "happiness":     "Describe a simple thing that brought you joy lately.",
}


# TTL = 30 seconds: ZenQuotes enforces a 5 req/30s rate limit on the free tier,
# so caching for 30 seconds ensures we never exceed it while still allowing
# manual refreshes to feel responsive.
@st.cache_data(ttl=30)
def fetch_quote(tag: str, cache_key: int = 0) -> dict:
    """
    Fetch one random quote from ZenQuotes.
    cache_key is incremented by the caller to force a refresh on demand.

    Returns:
      {"content": str, "author": str}   on success
      {"error": str, "message": str}    on failure
    """
    try:
        response = requests.get(
            f"{ZENQUOTES_BASE}/random",
            timeout=5,
        )

        # ── Status-code error handling ────────────────────────────────────
        if response.status_code == 401:
            return {
                "error": "401",
                "message": "API key is missing or invalid. Check your configuration.",
            }

        if response.status_code == 404:
            return {
                "error": "404",
                "message": "No results found for this theme. Try a different one.",
            }

        if response.status_code == 429:
            return {
                "error": "429",
                "message": "API limit reached. Please wait a minute and try again.",
            }

        if response.status_code >= 500:
            return {
                "error": "500",
                "message": "The service is temporarily unavailable. Please try again later.",
            }

        response.raise_for_status()
        data = response.json()

        # ── Empty-result handling (200 OK but no content) ─────────────────
        if not data or not isinstance(data, list):
            return {
                "error": "empty",
                "message": "Your search returned no results. Try a different theme.",
            }

        quote   = data[0]
        content = quote.get("q", "").strip()
        author  = quote.get("a", "Unknown").strip()

        if not content:
            return {
                "error": "empty",
                "message": "Your search returned no results. Try a different theme.",
            }

        return {"content": content, "author": author}

    except requests.exceptions.Timeout:
        return {
            "error": "timeout",
            "message": "Could not connect. Check your internet connection.",
        }

    except requests.exceptions.ConnectionError:
        return {
            "error": "connection",
            "message": "Could not connect. Check your internet connection.",
        }

    except Exception:
        return {
            "error": "unknown",
            "message": "Something went wrong fetching your prompt. Please try again.",
        }
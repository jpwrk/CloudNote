import streamlit as st
import requests

# API Config
AFFIRMATIONS_URL = "https://www.affirmations.dev/"
 
# Theme-based writing prompts shown alongside each affirmation.
# User's theme selection drives which prompt is displayed.
THEME_PROMPTS = {
    "✨ inspiration": "What's one possibility you haven't let yourself imagine yet?",
    "🧠 wisdom":      "What's something you've learned about yourself recently?",
    "💪 motivation":  "What's one small step you could take toward a goal this week?",
    "❤️ kindness":    "Who in your life are you most grateful for right now, and why?",
    "🌿 mindfulness": "What moment from today do you want to hold onto?",
    "😊 happiness":   "Describe a simple thing that brought you joy lately.",
}
 
THEME_TAGS = {k: k for k in THEME_PROMPTS}  # kept for compatibility with journal.py
 
 
@st.cache_data(ttl=60)
def fetch_prompt(theme_description: str, mood: str, cache_key: int = 0) -> dict:
    """
    Fetches one affirmation from affirmations.dev, then pairs it with a
    theme-specific journaling question. Both theme (user radio) and
    cache_key (user refresh button) drive this call.
 
    Returns:
      {"affirmation": str, "prompt": str}  on success
      {"error": str,  "message": str}      on failure
    """
    # Resolve theme label → writing prompt
    writing_prompt = THEME_PROMPTS.get(theme_description, "What's on your mind today?")
 
    try:
        response = requests.get(AFFIRMATIONS_URL, timeout=5)
 
        # Status-code error handling
        if response.status_code == 401:
            return {
                "error": "401",
                "message": "API key is missing or invalid. Check your configuration.",
            }
 
        if response.status_code == 404:
            return {
                "error": "404",
                "message": "No results found for your search.",
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
 
        # Empty-result handling (200 OK but no content)
        affirmation = data.get("affirmation", "").strip()
        if not affirmation:
            return {
                "error": "empty",
                "message": "Your search returned no results. Try refreshing.",
            }
 
        return {"affirmation": affirmation, "prompt": writing_prompt}
 
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
 
    except Exception as e:
        return {
            "error": "unknown",
            "message": f"Something went wrong fetching your prompt. Please try again.",
        }
import random
from datetime import datetime

PROMPTS = [
    "What made you smile today, even briefly?",
    "What's one thing you're carrying that you'd like to set down?",
    "Describe your energy today in three words.",
    "What's something small you're proud of this week?",
    "What would make tomorrow feel a little lighter?",
    "Who or what gave you a moment of peace today?",
    "What's something you've been avoiding thinking about?",
    "If today had a color, what would it be and why?",
    "What's one thing you wish you could say to yourself right now?",
    "Describe a moment today when you felt truly present.",
    "What's something you wish you could change about today, and why?",
    "If you could give your future self one piece of advice based on today, what would it be?",
    "What's one thing you're looking forward to this week?",
    "Describe a moment today when you felt a sense of accomplishment, no matter how small.",
    "What's something you wish you could say to someone else about how you're feeling today?",
    "If you could bottle up one feeling from today to revisit later, what would it be and why?",
    "What's one thing you learned about yourself today, even if it was just a small insight?"
]

def get_daily_prompt():
    random.seed(datetime.now().strftime("%Y-%m-%d"))
    return random.choice(PROMPTS)
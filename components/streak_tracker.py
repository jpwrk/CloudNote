def streak_tracker(streak):
    return f"""
    <div style="
        background: linear-gradient(135deg, #E9D5FF, #F8F6FF);
        padding: 1.5rem;
        border-radius: 18px;
        border: 1px solid #D8B4FE;
        box-shadow: 0 4px 12px rgba(167, 139, 250, 0.08);
        text-align: center;
        margin-bottom: 1rem;
    ">
        <p style="
            font-size: 0.85rem;
            color: #8A7CA8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        ">
            Current Streak
        </p>
        <p style="
            font-size: 2.2rem;
            font-weight: 700;
            color: #6D5BA8;
            margin: 0;
        ">
            ☁️ {streak} days
        </p>
    </div>
    """
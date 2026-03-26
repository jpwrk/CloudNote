def entry_card(date, title, preview, mood=""):
    return f"""
    <div style="
        background: white;
        padding: 1.2rem;
        border-radius: 18px;
        border: 1px solid #E9D5FF;
        box-shadow: 0 4px 12px rgba(167, 139, 250, 0.08);
        margin-bottom: 1rem;
    ">
        <p style="
            font-size: 0.8rem;
            color: #8A7CA8;
            margin-bottom: 0.4rem;
        ">
            {date} {mood}
        </p>
        <h3 style="
            font-size: 1.1rem;
            color: #4B4453;
            margin-bottom: 0.5rem;
        ">
            {title}
        </h3>
        <p style="
            font-size: 0.95rem;
            color: #6D6875;
            margin: 0;
        ">
            {preview}
        </p>
    </div>
    """
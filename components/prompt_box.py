def prompt_box(prompt):
    return f"""
    <div style="
        background: linear-gradient(135deg, #F8F6FF, #EEE9FF);
        padding: 1.5rem;
        border-radius: 18px;
        border: 1px solid #E9D5FF;
        box-shadow: 0 4px 12px rgba(167, 139, 250, 0.08);
        margin-bottom: 1rem;
    ">
        <p style="
            font-size: 0.85rem;
            color: #8A7CA8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        ">
            Today's Prompt
        </p>
        <p style="
            font-size: 1.1rem;
            color: #4B4453;
            font-style: italic;
            margin: 0;
        ">
            {prompt}
        </p>
    </div>
    """
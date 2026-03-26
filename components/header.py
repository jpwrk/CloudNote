def branded_header(title, subtitle):
    return f"""
    <div style="
        background: linear-gradient(135deg, #CDB4FF, #E9D5FF);
        padding: 2rem 1.5rem;
        border-radius: 18px;
        margin-bottom: 1.2rem;
        color: #4B4453;
        box-shadow: 0 4px 16px rgba(167, 139, 250, 0.15);
    ">
        <h1 style="font-size: 1.8rem; font-weight: 700;">{title}</h1>
        <p style="opacity: 0.85; font-size: 1rem;">{subtitle}</p>
    </div>
    """
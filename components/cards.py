def kpi_card(label, value, icon="", color="#4B4453"):
    return f"""
    <div style="
        background: white;
        padding: 1.3rem;
        border-radius: 18px;
        border: 1px solid #E9D5FF;
        box-shadow: 0 4px 12px rgba(167, 139, 250, 0.08);
        text-align: center;
    ">
        <div style="font-size: 1.8rem; margin-bottom: 0.4rem;">{icon}</div>
        <p style="font-size: 0.8rem; color: #8A7CA8; letter-spacing: 0.5px; text-transform: uppercase;">{label}</p>
        <p style="font-size: 2rem; font-weight: 700; color: {color};">{value}</p>
    </div>
    """
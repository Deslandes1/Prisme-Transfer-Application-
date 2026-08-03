import streamlit as st
import datetime

# ====== PAGE CONFIG ======
st.set_page_config(
    page_title="Prisme Transfer – Global Money Transfer",
    page_icon="💸",
    layout="wide"
)

# ====== CUSTOM CSS ======
st.markdown("""
<style>
    /* Main app background – light blue */
    .stApp {
        background-color: #e6f2ff !important;
    }
    .stApp [data-testid="stAppViewContainer"] {
        background-color: #f0f8ff !important;
    }
    /* Sidebar – light blue */
    [data-testid="stSidebar"] {
        background-color: #cce5ff !important;
        border-right: 1px solid #99ccff;
    }
    [data-testid="stSidebar"] * {
        color: #003366 !important;
    }
    /* Main container */
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #00209F 0%, #1a3a8a 50%, #D21034 50%, #D21034 100%);
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        color: white !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        margin: 0;
    }
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.2rem;
        color: white !important;
    }
    .sidebar-logo {
        text-align: center;
        padding: 0.5rem 0;
    }
    .sidebar-logo img {
        max-width: 150px;
        border-radius: 12px;
        border: 2px solid #00209F;
    }
    .sidebar-title {
        text-align: center;
        font-size: 1.3rem;
        font-weight: 700;
        color: #00209F;
        margin-top: 0.5rem;
    }
    .sidebar-subtitle {
        text-align: center;
        font-size: 0.9rem;
        color: #1a2a3a;
        opacity: 0.8;
    }
    .partner-item {
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s;
        cursor: pointer;
        border-left: 3px solid transparent;
        background: rgba(255,255,255,0.3);
    }
    .partner-item:hover {
        background: rgba(255,255,255,0.6);
        transform: translateX(4px);
    }
    .partner-item a {
        color: inherit !important;
        text-decoration: none !important;
        display: block;
    }
    .partner-item a:hover {
        text-decoration: underline !important;
    }
    .region-title {
        font-weight: 700;
        font-size: 1.0rem;
        color: #0a2a44;
        margin-top: 12px;
        margin-bottom: 4px;
        border-bottom: 2px solid #00209F;
        padding-bottom: 4px;
    }
    .footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid #99ccff;
        font-size: 0.9rem;
        color: #003366;
        background: rgba(255,255,255,0.5);
        border-radius: 8px;
    }
    .footer strong {
        color: #00209F;
    }
    .form-container {
        background: rgba(255,255,255,0.85);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #b0d4f0;
        backdrop-filter: blur(4px);
    }
    .form-container h2 {
        color: #00209F;
        margin-bottom: 1.5rem;
    }
    .form-container .stButton button {
        background: linear-gradient(105deg, #D21034 0%, #b0102a 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 40px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: 0.2s;
    }
    .form-container .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 20px rgba(210, 16, 52, 0.4);
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1rem;
        text-align: center;
        color: #155724;
    }
    .success-box .checkmark {
        font-size: 3rem;
        display: block;
    }
    .help-box {
        background: rgba(230, 242, 255, 0.8);
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        border: 1px solid #99ccff;
        backdrop-filter: blur(4px);
    }
    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.8rem; }
    }
</style>
""", unsafe_allow_html=True)

# ====== SIDEBAR ======
with st.sidebar:
    st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
    
    # ---- YOUR LOGO ----
    st.image(
        "https://raw.githubusercontent.com/Deslandes1/Prisme-Transfer-Application-/main/New%20logo.png",
        width=150
    )
    
    st.markdown("""
    <div style='text-align: center; margin-top: -0.5rem;'>
        <div style='font-size: 1.5rem; font-weight: 800; color: #00209F;'>
            Prisme Transfer
        </div>
        <div style='font-size: 0.9rem; color: #1a2a3a; opacity: 0.8;'>
            Global Money Transfer
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style='text-align: center;'>
        <div style='font-size: 0.9rem; color: #1a2a3a;'>
            <strong>Gesner Deslandes</strong><br>
            <span style='font-size: 0.8rem;'>Chief Engineer at GlobalInternet.py</span>
        </div>
        <div style='margin-top: 10px; font-size: 0.85rem;'>
            📱 (509) 4738-5663<br>
            📧 deslandes78@gmail.com<br>
            🌐 <a href='https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/' target='_blank' style='color: #00209F; text-decoration: none;'>Visit Website</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("© 2026 GlobalInternet.py – All rights reserved")

# ====== MAIN HEADER ======
st.markdown("""
<div class="main-header">
    <h1>💸 Prisme Transfer</h1>
    <p>Connecting Haiti to the World – Fast, Secure, Reliable</p>
</div>
""", unsafe_allow_html=True)

# ====== TWO-COLUMN LAYOUT ======
col_left, col_right = st.columns([1, 1], gap="large")

# ====== LEFT COLUMN – PARTNER LIST WITH LINKS ======
with col_left:
    st.markdown("### 🌍 Our Global Partners")
    st.caption("Click any partner below to visit their platform")

    # Partner data with colors and URLs
    partners = {
        "🌎 North America": [
            ("Boss Revolution", "#1a73e8", "https://www.bossrevolution.com/"),
            ("SendWave", "#ff6b35", "https://www.sendwave.com/"),
            ("Tap Tap", "#00b894", "https://www.taptapsend.com/"),
            ("Share Money", "#6c5ce7", "https://www.sharemoney.com/"),
            ("C.A.M", "#fdcb6e", "https://www.camtransfer.com/"),
            ("Digicel International", "#e17055", "https://www.digicelgroup.com/"),
            ("Viamericas", "#00cec9", "https://www.viamericas.com/"),
            ("Girosol", "#fd79a8", "https://www.girosol.com/"),
            ("Cashela", "#0984e3", "https://www.cashela.com/"),
            ("Majority", "#6ab04c", "https://www.majority.com/"),
            ("Intercambio Express", "#f0932b", "https://www.intercambioexpress.com/"),
            ("RevoluSend", "#eb4d4b", "https://www.revolusend.com/"),
        ],
        "🌍 Worldwide": [
            ("Remitly", "#2ecc71", "https://www.remitly.com/"),
            ("RIA Money Transfer", "#3498db", "https://www.riamoneytransfer.com/"),
            ("Xoom", "#9b59b6", "https://www.xoom.com/"),
            ("UNFCU", "#1abc9c", "https://www.unfcu.com/"),
            ("MoneyGram", "#e67e22", "https://www.moneygram.com/"),
        ],
        "🌎 Latin America": [
            ("Girofacil", "#2ecc71", "https://www.girofacil.com/"),
            ("Uno Money Transfers", "#3498db", "https://www.unotransfer.com/"),
            ("More Money", "#f1c40f", "https://www.moremoney.com/"),
            ("Trans Fast", "#e74c3c", "https://www.transfast.com/"),
            ("AFEX", "#2c3e50", "https://www.afex.com/"),
        ],
        "🇪🇺 Europe": [
            ("Orange Money", "#e67e22", "https://www.orange.com/"),
            ("WorldRemit", "#2980b9", "https://www.worldremit.com/"),
        ],
        "🏝️ Caribbean": [
            ("Cibao Express", "#1abc9c", "https://www.cibaoexpress.com/"),
            ("C.A.M", "#fdcb6e", "https://www.camtransfer.com/"),
        ],
    }

    for region, partner_list in partners.items():
        st.markdown(f'<div class="region-title">{region}</div>', unsafe_allow_html=True)
        for name, color, url in partner_list:
            st.markdown(
                f'<div class="partner-item" style="border-left-color: {color}; color: {color};">'
                f'<a href="{url}" target="_blank" style="color: {color} !important;">'
                f'<span style="font-weight: 600;">{name}</span>'
                f'</a>'
                f'</div>',
                unsafe_allow_html=True
            )
        st.markdown("")

    st.info("💡 **Note:** Click any partner name to visit their official website and start your transfer.")

# ====== RIGHT COLUMN – USER REGISTRATION FORM ======
with col_right:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown("### 📝 Register to Send or Receive")
    st.caption("Fill in your details to start using Prisme Transfer services")

    with st.form("user_registration", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", placeholder="Jean")
        with col2:
            last_name = st.text_input("Last Name", placeholder="Pierre")

        street_address = st.text_input("Street Address", placeholder="123 Rue de la Paix")
        city = st.text_input("City", placeholder="Port-au-Prince")

        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("Email", placeholder="jean.pierre@example.com")
        with col2:
            phone = st.text_input("Phone Number", placeholder="+509 4738-5663")

        countries = [
            "Haiti", "United States", "Canada", "France", "Spain", "Germany",
            "United Kingdom", "Brazil", "Mexico", "Colombia", "Chile", "Argentina",
            "Dominican Republic", "Jamaica", "Trinidad and Tobago", "Other"
        ]
        country = st.selectbox("Country", countries)

        terms = st.checkbox("I agree to the terms and conditions of Prisme Transfer")

        submitted = st.form_submit_button("🚀 Register Now")

        if submitted:
            if not all([first_name, last_name, street_address, city, email, phone]):
                st.error("❌ Please fill in all fields.")
            elif not terms:
                st.warning("⚠️ You must agree to the terms and conditions.")
            else:
                st.markdown(f"""
                <div class="success-box">
                    <span class="checkmark">✅</span>
                    <strong>Registration Successful!</strong><br>
                    Welcome, {first_name} {last_name}!<br>
                    We will contact you at {email} or {phone} shortly.<br>
                    <span style="font-size: 0.85rem; opacity: 0.8;">You can now send or receive money through any of our partners listed on the left.</span>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="help-box">
        <strong>📌 Need help?</strong><br>
        <span style="font-size: 0.9rem;">Contact our support team at <strong>deslandes78@gmail.com</strong> or call <strong>(509) 4738-5663</strong></span>
    </div>
    """, unsafe_allow_html=True)

# ====== FOOTER ======
st.markdown(f"""
<div class="footer">
    <strong>Built by Gesner Deslandes</strong><br>
    <span style="font-size: 0.8rem;">
        Chief Engineer at GlobalInternet.py<br>
        📱 (509) 4738-5663 &nbsp;|&nbsp; 📧 deslandes78@gmail.com &nbsp;|&nbsp;
        🌐 <a href="https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/" target="_blank" style="color: #00209F;">Visit Website</a><br>
        <span style="opacity: 0.6;">© 2026 Prisme Transfer – Built for Haiti, Connected to the World 🇭🇹</span>
    </span>
</div>
""", unsafe_allow_html=True)

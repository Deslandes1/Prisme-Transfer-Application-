import streamlit as st
import datetime
import tempfile
import os
import subprocess
import time

# ====== CHECK FOR EDGE TTS ======
EDGE_TTS_AVAILABLE = False
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    pass

# ====== PAGE CONFIG ======
st.set_page_config(
    page_title="GlobalInternet.py – Money Transfer & Banking",
    page_icon="💸",
    layout="wide"
)

# ====== CUSTOM CSS ======
st.markdown("""
<style>
    .stApp { background-color: #e6f2ff !important; }
    .stApp [data-testid="stAppViewContainer"] { background-color: #f0f8ff !important; }
    [data-testid="stSidebar"] {
        background-color: #cce5ff !important;
        border-right: 1px solid #99ccff;
    }
    [data-testid="stSidebar"] * { color: #003366 !important; }
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
    .section-title {
        font-weight: 700;
        font-size: 1.1rem;
        color: #0a2a44;
        margin-top: 16px;
        margin-bottom: 8px;
        border-bottom: 2px solid #00209F;
        padding-bottom: 4px;
    }
    .link-item {
        padding: 6px 12px;
        margin: 3px 0;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s;
        border-left: 3px solid transparent;
        background: rgba(255,255,255,0.3);
    }
    .link-item:hover {
        background: rgba(255,255,255,0.6);
        transform: translateX(4px);
    }
    .link-item a {
        color: inherit !important;
        text-decoration: none !important;
        display: block;
    }
    .link-item a:hover {
        text-decoration: underline !important;
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
    .footer strong { color: #00209F; }
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
    .donate-box {
        background: rgba(255,215,0,0.15);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ffd700;
        text-align: center;
    }
    .voice-container {
        background: rgba(255,255,255,0.5);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid #99ccff;
    }
    .highlight-box {
        background: rgba(0,32,159,0.08);
        border-left: 4px solid #00209F;
        padding: 0.8rem;
        margin: 8px 0;
        border-radius: 4px;
    }
    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.8rem; }
    }
</style>
""", unsafe_allow_html=True)

# ====== VOICE SCRIPTS IN MULTIPLE LANGUAGES ======
VOICE_SCRIPTS = {
    "en": {
        "name": "English",
        "voice": "en-US-JennyNeural",
        "script": (
            "This app is brought to you by Gesner Deslandes, Chief Engineer at GlobalInternet.py. "
            "Prisme Transfer is a global money transfer platform that connects Haiti to the world. "
            "We partner with over 20 international money transfer companies to deliver funds directly into MonCash mobile wallets or for pick-up at Fonkoze locations. "
            "To use our service, simply register with your personal details on the right side of this page. "
            "First, enter your first name. Then your last name. Next, your street address, city, and your ID number. "
            "Then provide your email address and phone number. Select your country from the dropdown. "
            "Finally, check the terms and conditions box and click the register button. "
            "After registering, choose a partner from the list below. Each partner name is a clickable link that will take you to their official website. "
            "You can send or receive money to or from anywhere in the world. "
            "Our partners include Boss Revolution, SendWave, Tap Tap, Share Money, C.A.M, Digicel International, Viamericas, Girosol, Cashela, Majority, Intercambio Express, RevoluSend, Remitly, RIA, Xoom, UNFCU, MoneyGram, Girofacil, Uno Money Transfers, More Money, Trans Fast, AFEX, Orange Money, WorldRemit, Cibao Express, and many more. "
            "We also provide links to other popular transfer services like Western Union, UNITransfer, and others. "
            "We also list all major Haitian banks so you can access online banking directly. "
            "Prisme Transfer is built for Haiti, connected to the world. "
            "To support our platform, you can send donations to GlobalInternet.py. "
            "Our phone number for donations is (509) 4738-5663 and our email is deslandes78@gmail.com. "
            "Every contribution helps us improve and expand our services. "
            "Contact us at (509) 4738-5663 or deslandes78@gmail.com. "
            "Thank you for using GlobalInternet.py and Prisme Transfer."
        )
    },
    "fr": {
        "name": "Français",
        "voice": "fr-FR-DeniseNeural",
        "script": (
            "Cette application vous est présentée par Gesner Deslandes, Ingénieur en Chef chez GlobalInternet.py. "
            "Prisme Transfer est une plateforme mondiale de transfert d'argent qui connecte Haïti au monde. "
            "Nous nous associons à plus de 20 sociétés internationales de transfert d'argent pour livrer les fonds directement dans les portefeuilles mobiles MonCash ou pour les retirer dans les agences Fonkoze. "
            "Pour utiliser notre service, inscrivez-vous simplement avec vos coordonnées personnelles sur le côté droit de cette page. "
            "D'abord, entrez votre prénom. Ensuite, votre nom de famille. Puis, votre adresse, votre ville et votre numéro d'identité. "
            "Ensuite, fournissez votre adresse e-mail et votre numéro de téléphone. Sélectionnez votre pays dans le menu déroulant. "
            "Enfin, cochez la case des conditions générales et cliquez sur le bouton d'inscription. "
            "Après l'inscription, choisissez un partenaire dans la liste ci-dessous. Chaque nom de partenaire est un lien cliquable qui vous mènera à son site officiel. "
            "Vous pouvez envoyer ou recevoir de l'argent partout dans le monde. "
            "Nos partenaires incluent Boss Revolution, SendWave, Tap Tap, Share Money, C.A.M, Digicel International, Viamericas, Girosol, Cashela, Majority, Intercambio Express, RevoluSend, Remitly, RIA, Xoom, UNFCU, MoneyGram, Girofacil, Uno Money Transfers, More Money, Trans Fast, AFEX, Orange Money, WorldRemit, Cibao Express, et bien d'autres. "
            "Nous fournissons également des liens vers d'autres services de transfert populaires comme Western Union, UNITransfer, et d'autres. "
            "Nous listons également toutes les grandes banques haïtiennes pour que vous puissiez accéder directement à la banque en ligne. "
            "Prisme Transfer est construit pour Haïti, connecté au monde. "
            "Pour soutenir notre plateforme, vous pouvez envoyer des dons à GlobalInternet.py. "
            "Notre numéro de téléphone pour les dons est le (509) 4738-5663 et notre e-mail est deslandes78@gmail.com. "
            "Chaque contribution nous aide à améliorer et à étendre nos services. "
            "Contactez-nous au (509) 4738-5663 ou par e-mail à deslandes78@gmail.com. "
            "Merci d'utiliser GlobalInternet.py et Prisme Transfer."
        )
    },
    "es": {
        "name": "Español",
        "voice": "es-ES-ElviraNeural",
        "script": (
            "Esta aplicación es presentada por Gesner Deslandes, Ingeniero Jefe en GlobalInternet.py. "
            "Prisme Transfer es una plataforma global de transferencia de dinero que conecta a Haití con el mundo. "
            "Nos asociamos con más de 20 empresas internacionales de transferencia de dinero para entregar fondos directamente a billeteras móviles MonCash o para recoger en ubicaciones de Fonkoze. "
            "Para usar nuestro servicio, simplemente regístrese con sus datos personales en el lado derecho de esta página. "
            "Primero, ingrese su nombre. Luego su apellido. A continuación, su dirección, ciudad y su número de identificación. "
            "Luego proporcione su correo electrónico y número de teléfono. Seleccione su país en el menú desplegable. "
            "Finalmente, marque la casilla de términos y condiciones y haga clic en el botón de registro. "
            "Después de registrarse, elija un socio de la lista a continuación. Cada nombre de socio es un enlace en el que se puede hacer clic y que lo llevará a su sitio web oficial. "
            "Puede enviar o recibir dinero a o desde cualquier parte del mundo. "
            "Nuestros socios incluyen Boss Revolution, SendWave, Tap Tap, Share Money, C.A.M, Digicel International, Viamericas, Girosol, Cashela, Majority, Intercambio Express, RevoluSend, Remitly, RIA, Xoom, UNFCU, MoneyGram, Girofacil, Uno Money Transfers, More Money, Trans Fast, AFEX, Orange Money, WorldRemit, Cibao Express, y muchos más. "
            "También proporcionamos enlaces a otros servicios de transferencia populares como Western Union, UNITransfer, y otros. "
            "También enumeramos todos los principales bancos haitianos para que pueda acceder a la banca en línea directamente. "
            "Prisme Transfer está construido para Haití, conectado al mundo. "
            "Para apoyar nuestra plataforma, puede enviar donaciones a GlobalInternet.py. "
            "Nuestro número de teléfono para donaciones es (509) 4738-5663 y nuestro correo electrónico es deslandes78@gmail.com. "
            "Cada contribución nos ayuda a mejorar y expandir nuestros servicios. "
            "Contáctenos al (509) 4738-5663 o por correo a deslandes78@gmail.com. "
            "Gracias por usar GlobalInternet.py y Prisme Transfer."
        )
    },
    "zh": {
        "name": "中文",
        "voice": "zh-CN-XiaoxiaoNeural",
        "script": (
            "本应用由 GlobalInternet.py 首席工程师 Gesner Deslandes 为您呈现。"
            "Prisme Transfer 是一个全球性的汇款平台，将海地与世界连接起来。"
            "我们与超过 20 家国际汇款公司合作，直接将资金存入 MonCash 手机钱包或在 Fonkoze 网点取款。"
            "要使用我们的服务，只需在本页右侧填写您的个人信息。"
            "首先，输入您的名字。然后输入您的姓氏。接着输入您的地址、城市和身份证号码。"
            "然后提供您的电子邮件地址和电话号码。从下拉菜单中选择您的国家。"
            "最后，勾选条款和条件框，然后点击注册按钮。"
            "注册后，从下方列表中选择一个合作伙伴。每个合作伙伴名称都是一个可点击的链接，将带您进入其官方网站。"
            "您可以在世界任何地方发送或接收资金。"
            "我们的合作伙伴包括 Boss Revolution、SendWave、Tap Tap、Share Money、C.A.M、Digicel International、Viamericas、Girosol、Cashela、Majority、Intercambio Express、RevoluSend、Remitly、RIA、Xoom、UNFCU、MoneyGram、Girofacil、Uno Money Transfers、More Money、Trans Fast、AFEX、Orange Money、WorldRemit、Cibao Express 等等。"
            "我们还提供其他流行汇款服务的链接，如 Western Union、UNITransfer 等。"
            "我们还列出了所有主要的海地银行，方便您直接访问网上银行。"
            "Prisme Transfer 为海地而生，与世界相连。"
            "为了支持我们的平台，您可以向 GlobalInternet.py 捐款。"
            "我们的捐款电话是 (509) 4738-5663，电子邮件是 deslandes78@gmail.com。"
            "每一笔捐款都有助于我们改善和扩展服务。"
            "请通过 (509) 4738-5663 或 deslandes78@gmail.com 与我们联系。"
            "感谢您使用 GlobalInternet.py 和 Prisme Transfer。"
        )
    }
}

# ====== VOICE FUNCTIONS ======
def text_to_speech_subprocess(text, voice):
    """Generate speech using edge-tts via subprocess."""
    try:
        import tempfile
        import subprocess
        import os
        
        tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
        
        text_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8')
        text_file.write(text)
        text_file.close()
        
        cmd = [
            "edge-tts",
            "-f", text_file.name,
            "--voice", voice,
            "--write-media", tmp_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        os.unlink(text_file.name)
        
        if result.returncode != 0:
            raise RuntimeError(f"edge-tts failed: {result.stderr}")
        
        if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
            raise RuntimeError("Generated audio file is empty")
        
        with open(tmp_path, 'rb') as f:
            audio_bytes = f.read()
        os.unlink(tmp_path)
        return audio_bytes
    except Exception as e:
        st.error(f"❌ Voice generation failed: {e}")
        return None

def play_voice_explanation(lang):
    if lang not in VOICE_SCRIPTS:
        st.error("Language not supported.")
        return
    
    script_data = VOICE_SCRIPTS[lang]
    script = script_data["script"]
    voice = script_data["voice"]
    
    audio_bytes = text_to_speech_subprocess(script, voice)
    
    if audio_bytes:
        st.audio(audio_bytes, format='audio/mp3')
        st.success(f"✅ Voice explanation played in {script_data['name']}!")
    else:
        st.error("❌ Unable to generate voice. Please check edge-tts installation.")

# ====== SIDEBAR ======
with st.sidebar:
    st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
    st.image(
        "https://raw.githubusercontent.com/Deslandes1/Prisme-Transfer-Application-/main/New%20logo.png",
        width=150
    )
    st.markdown("""
    <div style='text-align: center; margin-top: -0.5rem;'>
        <div style='font-size: 1.5rem; font-weight: 800; color: #00209F;'>GlobalInternet.py</div>
        <div style='font-size: 0.9rem; color: #1a2a3a; opacity: 0.8;'>Money Transfer & Banking</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")

    # ---- AI VOICE SECTION ----
    st.markdown("### 🔊 AI Voice")
    
    lang_options = {key: val["name"] for key, val in VOICE_SCRIPTS.items()}
    selected_lang = st.selectbox(
        "Select Language",
        options=list(lang_options.keys()),
        format_func=lambda x: lang_options[x],
        index=0
    )
    
    st.markdown('<div class="voice-container">', unsafe_allow_html=True)
    if st.button("🎙️ Explain App (AI Voice)", use_container_width=True):
        play_voice_explanation(selected_lang)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ---- DONATION INFO ----
    st.markdown("### 💝 Support Our Work")
    st.markdown("""
    <div class="donate-box">
        <div style='font-size: 1.1rem; font-weight: 600; color: #00209F;'>🙏 Donate</div>
        <div style='font-size: 0.9rem; margin-top: 6px;'>
            📱 <strong>(509) 4738-5663</strong><br>
            📧 <strong>deslandes78@gmail.com</strong>
        </div>
        <div style='font-size: 0.8rem; opacity: 0.7; margin-top: 4px;'>Your support keeps us going 🇭🇹</div>
    </div>
    """, unsafe_allow_html=True)

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
    <h1>💸 GlobalInternet.py</h1>
    <p>Connecting Haiti to the World – Fast, Secure, Reliable</p>
</div>
""", unsafe_allow_html=True)

# ====== TWO-COLUMN LAYOUT ======
col_left, col_right = st.columns([1, 1], gap="large")

# ====== LEFT COLUMN – RESOURCES ======
with col_left:
    st.markdown("### 🌐 Financial Services & Resources")
    st.caption("Click any link to access the service")

    # ---- 1. ONLINE TRANSFER BUREAUS ----
    st.markdown('<div class="section-title">📤 Online Transfer Bureaus</div>', unsafe_allow_html=True)
    transfer_bureaus = [
        ("Western Union", "#ff6600", "https://www.westernunion.com/"),
        ("MoneyGram", "#e67e22", "https://www.moneygram.com/"),
        ("Ria Money Transfer", "#3498db", "https://www.riamoneytransfer.com/"),
        ("Xoom (PayPal)", "#9b59b6", "https://www.xoom.com/"),
        ("WorldRemit", "#2980b9", "https://www.worldremit.com/"),
        ("Remitly", "#2ecc71", "https://www.remitly.com/"),
        ("SendWave", "#ff6b35", "https://www.sendwave.com/"),
        ("Tap Tap", "#00b894", "https://www.taptapsend.com/"),
        ("UNITransfer", "#0044cc", "https://www.unitransfer.com/"),
        ("CAM Transfer", "#fdcb6e", "https://www.camtransfer.com/"),
    ]
    for name, color, url in transfer_bureaus:
        st.markdown(
            f'<div class="link-item" style="border-left-color: {color}; color: {color};">'
            f'<a href="{url}" target="_blank" style="color: {color} !important;">'
            f'<span style="font-weight: 600;">{name}</span>'
            f'</a>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ---- 2. HAITIAN BANKING SYSTEM ----
    st.markdown('<div class="section-title">🏦 Haitian Banking System</div>', unsafe_allow_html=True)
    banks = [
        ("UniBank", "#00209F", "https://www.unibank.net/"),
        ("Sogebank", "#1a5276", "https://www.sogebank.com/"),
        ("Banque Nationale de Crédit (BNC)", "#2e86c1", "https://www.bnc-haiti.com/"),
        ("Banque de la République d'Haïti (BRH)", "#1a3a8a", "https://www.brh.ht/"),
        ("Banque Populaire Haïtienne", "#28b463", "https://www.bphaiti.com/"),
        ("Société Générale Haïtienne (SOGEHA)", "#c0392b", "https://www.sogeha.com/"),
        ("Capital Bank", "#f39c12", "https://www.capitalbank.ht/"),
        ("BANCO", "#8e44ad", "https://www.banco.ht/"),
        ("La Fédérale", "#2c3e50", "https://www.lafederale.com/"),
        ("COOPEC", "#1abc9c", "https://www.coopec.ht/"),
    ]
    for name, color, url in banks:
        st.markdown(
            f'<div class="link-item" style="border-left-color: {color}; color: {color};">'
            f'<a href="{url}" target="_blank" style="color: {color} !important;">'
            f'<span style="font-weight: 600;">{name}</span>'
            f'</a>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ---- 3. PRISME TRANSFER PARTNERS ----
    st.markdown('<div class="section-title">🤝 Prisme Transfer Partners</div>', unsafe_allow_html=True)
    st.caption("Click to access Prisme Transfer's partner network")

    prisme_partners = [
        ("Boss Revolution", "#1a73e8", "https://www.bossrevolution.com/"),
        ("Share Money", "#6c5ce7", "https://www.sharemoney.com/"),
        ("C.A.M", "#fdcb6e", "https://www.camtransfer.com/"),
        ("Digicel International", "#e17055", "https://www.digicelgroup.com/"),
        ("Viamericas", "#00cec9", "https://www.viamericas.com/"),
        ("Girosol", "#fd79a8", "https://www.girosol.com/"),
        ("Cashela", "#0984e3", "https://www.cashela.com/"),
        ("Majority", "#6ab04c", "https://www.majority.com/"),
        ("Intercambio Express", "#f0932b", "https://www.intercambioexpress.com/"),
        ("RevoluSend", "#eb4d4b", "https://www.revolusend.com/"),
        ("UNFCU", "#1abc9c", "https://www.unfcu.com/"),
        ("Girofacil", "#2ecc71", "https://www.girofacil.com/"),
        ("Uno Money Transfers", "#3498db", "https://www.unotransfer.com/"),
        ("More Money", "#f1c40f", "https://www.moremoney.com/"),
        ("Trans Fast", "#e74c3c", "https://www.transfast.com/"),
        ("AFEX", "#2c3e50", "https://www.afex.com/"),
        ("Orange Money", "#e67e22", "https://www.orange.com/"),
        ("Cibao Express", "#1abc9c", "https://www.cibaoexpress.com/"),
    ]
    for name, color, url in prisme_partners:
        st.markdown(
            f'<div class="link-item" style="border-left-color: {color}; color: {color};">'
            f'<a href="{url}" target="_blank" style="color: {color} !important;">'
            f'<span style="font-weight: 600;">{name}</span>'
            f'</a>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.info("💡 **Note:** All links open in a new tab. Use these services to send or receive money globally.")

# ====== RIGHT COLUMN – REGISTRATION FORM ======
with col_right:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown("### 📝 Register to Send or Receive")
    st.caption("Fill in your details to start using our services")

    with st.form("user_registration", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", placeholder="Jean", key="first_name")
        with col2:
            last_name = st.text_input("Last Name", placeholder="Pierre", key="last_name")

        street_address = st.text_input("Street Address", placeholder="123 Rue de la Paix", key="street_address")
        city = st.text_input("City", placeholder="Port-au-Prince", key="city")
        id_number = st.text_input("ID Number (Passport, National ID, etc.)", placeholder="e.g., 1234-5678-9012", key="id_number")

        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("Email", placeholder="jean.pierre@example.com", key="email")
        with col2:
            phone = st.text_input("Phone Number", placeholder="+509 4738-5663", key="phone")

        countries = [
            "Haiti", "United States", "Canada", "France", "Spain", "Germany",
            "United Kingdom", "Brazil", "Mexico", "Colombia", "Chile", "Argentina",
            "Dominican Republic", "Jamaica", "Trinidad and Tobago", "Other"
        ]
        country = st.selectbox("Country", countries, key="country")

        terms = st.checkbox("I agree to the terms and conditions", key="terms")

        submitted = st.form_submit_button("🚀 Register Now")

        if submitted:
            if not all([first_name, last_name, street_address, city, id_number, email, phone]):
                st.error("❌ Please fill in all fields (including ID Number).")
            elif not terms:
                st.warning("⚠️ You must agree to the terms and conditions.")
            else:
                st.markdown(f"""
                <div class="success-box">
                    <span class="checkmark">✅</span>
                    <strong>Registration Successful!</strong><br>
                    Welcome, {first_name} {last_name}!<br>
                    ID: {id_number}<br>
                    We will contact you at {email} or {phone} shortly.<br>
                    <span style="font-size: 0.85rem; opacity: 0.8;">You can now send or receive money through any of the services listed on the left.</span>
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
        <span style="opacity: 0.6;">© 2026 GlobalInternet.py – Built for Haiti, Connected to the World 🇭🇹</span>
    </span>
</div>
""", unsafe_allow_html=True)

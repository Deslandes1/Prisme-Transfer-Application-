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
    .resources-container {
        background: rgba(255,255,255,0.6);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #b0d4f0;
        backdrop-filter: blur(4px);
    }
    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.8rem; }
    }
</style>
""", unsafe_allow_html=True)

# ====== VOICE SCRIPTS – GLOBALINTERNET.PY DIRECTORY ======
VOICE_SCRIPTS = {
    "en": {
        "name": "English",
        "voice": "en-US-JennyNeural",
        "script": (
            "Welcome to GlobalInternet.py. "
            "This app brings together a comprehensive list of money transfer bureaus and Haitian banking institutions in one place. "
            "You can access popular services like Western Union, MoneyGram, Ria, Xoom, WorldRemit, Remitly, SendWave, Tap Tap, UNITransfer, CAM Transfer, and many more. "
            "We also provide direct links to all major Haitian banks such as UniBank, Sogebank, BNC, BRH, and others. "
            "Whether you need to send money internationally or manage your local banking, all the resources are right here. "
            "This application is brought to you by Gesner Deslandes, Chief Engineer at GlobalInternet.py. "
            "To support our work, you can send donations to GlobalInternet.py. "
            "Our phone number is (509) 4738-5663 and email is deslandes78@gmail.com. "
            "Thank you for using GlobalInternet.py."
        )
    },
    "fr": {
        "name": "Français",
        "voice": "fr-FR-DeniseNeural",
        "script": (
            "Bienvenue sur GlobalInternet.py. "
            "Cette application rassemble en un seul endroit une liste complète des bureaux de transfert d'argent et des institutions bancaires haïtiennes. "
            "Vous pouvez accéder à des services populaires tels que Western Union, MoneyGram, Ria, Xoom, WorldRemit, Remitly, SendWave, Tap Tap, UNITransfer, CAM Transfer, et bien d'autres. "
            "Nous fournissons également des liens directs vers toutes les principales banques haïtiennes comme UniBank, Sogebank, BNC, BRH, et autres. "
            "Que vous ayez besoin d'envoyer de l'argent à l'international ou de gérer vos opérations bancaires locales, toutes les ressources sont ici. "
            "Cette application vous est présentée par Gesner Deslandes, Ingénieur en Chef chez GlobalInternet.py. "
            "Pour soutenir notre travail, vous pouvez envoyer des dons à GlobalInternet.py. "
            "Notre numéro de téléphone est le (509) 4738-5663 et notre e-mail est deslandes78@gmail.com. "
            "Merci d'utiliser GlobalInternet.py."
        )
    },
    "es": {
        "name": "Español",
        "voice": "es-ES-ElviraNeural",
        "script": (
            "Bienvenido a GlobalInternet.py. "
            "Esta aplicación reúne en un solo lugar una lista completa de oficinas de transferencia de dinero e instituciones bancarias haitianas. "
            "Puede acceder a servicios populares como Western Union, MoneyGram, Ria, Xoom, WorldRemit, Remitly, SendWave, Tap Tap, UNITransfer, CAM Transfer, y muchos más. "
            "También proporcionamos enlaces directos a todos los principales bancos haitianos como UniBank, Sogebank, BNC, BRH, y otros. "
            "Ya sea que necesite enviar dinero internacionalmente o administrar sus operaciones bancarias locales, todos los recursos están aquí. "
            "Esta aplicación es presentada por Gesner Deslandes, Ingeniero Jefe en GlobalInternet.py. "
            "Para apoyar nuestro trabajo, puede enviar donaciones a GlobalInternet.py. "
            "Nuestro número de teléfono es (509) 4738-5663 y nuestro correo electrónico es deslandes78@gmail.com. "
            "Gracias por usar GlobalInternet.py."
        )
    },
    "zh": {
        "name": "中文",
        "voice": "zh-CN-XiaoxiaoNeural",
        "script": (
            "欢迎来到 GlobalInternet.py。"
            "这个应用程序将汇款机构和海地银行机构的全面列表集中在一个地方。"
            "您可以访问流行的服务，如 Western Union、MoneyGram、Ria、Xoom、WorldRemit、Remitly、SendWave、Tap Tap、UNITransfer、CAM Transfer 等等。"
            "我们还提供所有主要海地银行的直接链接，如 UniBank、Sogebank、BNC、BRH 等。"
            "无论您是需要国际汇款还是管理本地银行业务，所有资源都在这里。"
            "此应用程序由 GlobalInternet.py 的首席工程师 Gesner Deslandes 为您呈现。"
            "为了支持我们的工作，您可以向 GlobalInternet.py 捐款。"
            "我们的电话号码是 (509) 4738-5663，电子邮件是 deslandes78@gmail.com。"
            "感谢您使用 GlobalInternet.py。"
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

# ====== RESOURCES (Full Width, No Right Form) ======
st.markdown('<div class="resources-container">', unsafe_allow_html=True)

st.markdown("### 🌐 Financial Services & Resources")
st.caption("Click any link to access the service directly")

# ---- 1. ONLINE TRANSFER BUREAUS ----
st.markdown('<div class="section-title">📤 Online Transfer Bureaus</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

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

for i, (name, color, url) in enumerate(transfer_bureaus):
    with [col1, col2, col3][i % 3]:
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

col1, col2, col3 = st.columns(3)

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

for i, (name, color, url) in enumerate(banks):
    with [col1, col2, col3][i % 3]:
        st.markdown(
            f'<div class="link-item" style="border-left-color: {color}; color: {color};">'
            f'<a href="{url}" target="_blank" style="color: {color} !important;">'
            f'<span style="font-weight: 600;">{name}</span>'
            f'</a>'
            f'</div>',
            unsafe_allow_html=True
        )

st.markdown("---")

# ---- 3. PRISME TRANSFER PARTNERS (still kept as a category) ----
st.markdown('<div class="section-title">🤝 Prisme Transfer Partners</div>', unsafe_allow_html=True)
st.caption("Click to access Prisme Transfer's partner network")

col1, col2, col3 = st.columns(3)

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

for i, (name, color, url) in enumerate(prisme_partners):
    with [col1, col2, col3][i % 3]:
        st.markdown(
            f'<div class="link-item" style="border-left-color: {color}; color: {color};">'
            f'<a href="{url}" target="_blank" style="color: {color} !important;">'
            f'<span style="font-weight: 600;">{name}</span>'
            f'</a>'
            f'</div>',
            unsafe_allow_html=True
        )

st.info("💡 **Note:** All links open in a new tab. Use these services to send or receive money globally.")

st.markdown('</div>', unsafe_allow_html=True)

# ====== HELP BOX ======
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

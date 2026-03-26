import streamlit as st
import re
import tempfile

from core.agent import agent_decision
from tools.file_parser import read_pdf
from tools.ocr_reader import extract_text_from_image, extract_text_from_scanned_pdf

# =========================
# ⚙️ Page Config
# =========================
st.set_page_config(
    page_title="Cyber Crime Scam Detection System",
    page_icon="🛡️",
    layout="wide"
)

# =========================
# 🧠 Session Memory
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# 🎨 Styling
# =========================
st.markdown("""
<style>
.block-container {padding-top: 1.5rem;}
.stButton>button {
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🛡️ HEADER
# =========================
st.title("🛡️ Cyber Crime Scam Detection System")
#st.caption("🚀 AI-powered scam detection with reasoning")

st.markdown(
    "<p style='font-size:24px; font-weight:bold; text-align:Left;'>🚀 AI-powered scam detection system with reasoning for *Text *Image * Barcode *UPI * Audio * WhatsApp and *LIVE</p>",
    unsafe_allow_html=True
)

colA, colB, colC = st.columns(3)
colA.metric("Scans Today", "12")
colB.metric("Threats Detected", "3")
colC.metric("Status", "🟢 Active")

# =========================
# 🔧 Utility Functions
# =========================
def safe_transcribe(file_path):
    from tools.voice_to_text import transcribe_audio
    return transcribe_audio(file_path)


def show_confidence(result):
    match = re.search(r"Confidence:\s*(\d+)%", result)
    if match:
        confidence = int(match.group(1))
        st.progress(confidence / 100)

        if confidence > 70:
            st.error("🔴 High Risk Scam")
        elif confidence > 40:
            st.warning("🟡 Suspicious")
        else:
            st.success("🟢 Likely Safe")


def highlight_scam_words(text):
    words = ["urgent", "blocked", "verify", "otp", "bank", "login", "click", "link", "payment", "fee", "suspend"]
    for w in words:
        text = text.replace(w, f"<span style='background-color:yellow'>{w}</span>")
    return text


def process_pdf_smart(file):
    text = ""

    try:
        text = read_pdf(file)
    except:
        text = ""

    if not text.strip():
        try:
            st.info("🔍 Using OCR...")
            text = extract_text_from_scanned_pdf(file)
        except:
            text = ""

    if not text.strip():
        try:
            file.seek(0)
            text = extract_text_from_image(file)
        except:
            text = ""

    return text


# =========================
# 📌 SIDEBAR = INPUT PANEL
# =========================
with st.sidebar:
    st.title("🛡️ Input Panel")

    option = st.radio(
        "Choose Input Type",
        [
            "💬 Chat",
            "📄 PDF",
            "🎤 Audio",
            "🖼️ Image",
            "📱 WhatsApp",
            "📷 Camera",
            "📦 Barcode",
            "💳 UPI QR"
        ]
    )

    # =========================
    # INPUTS INSIDE SIDEBAR
    # =========================

    if option == "📄 PDF":
        sidebar_file = st.file_uploader("Upload PDF", type=["pdf"])

    elif option == "🎤 Audio":
        sidebar_file = st.file_uploader("Upload Audio", type=["mp3", "wav"])

    elif option in ["🖼️ Image", "📱 WhatsApp", "📦 Barcode", "💳 UPI QR"]:
        sidebar_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    elif option == "📷 Camera":
        sidebar_file = st.camera_input("Capture Image")

    else:
        sidebar_file = None

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# =========================
# 🖥️ MAIN AREA = FULL ANALYSIS
# =========================

# =========================
# 💬 CHAT
# =========================
if option == "💬 Chat":

    user_input = st.chat_input("Type your message...")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                result = agent_decision(user_input)

            st.markdown(result)
            show_confidence(result)

        st.session_state.messages.append({"role": "assistant", "content": result})


# =========================
# 📄 PDF ANALYSIS
# =========================
elif option == "📄 PDF" and sidebar_file:

    text = process_pdf_smart(sidebar_file)

    st.subheader("📄 Extracted Text")
    st.text_area("", text, height=250)

    if st.button("Analyze PDF"):
        result = agent_decision(text)
        st.markdown(result)
        show_confidence(result)


# =========================
# 🎤 AUDIO
# =========================
elif option == "🎤 Audio" and sidebar_file:

    st.audio(sidebar_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(sidebar_file.read())
        temp_path = tmp.name

    with st.spinner("Transcribing..."):
        text = safe_transcribe(temp_path)

    st.text_area("Transcribed Text", text)

    if st.button("Analyze Audio"):
        result = agent_decision(text)
        st.markdown(result)
        show_confidence(result)


# =========================
# 🖼️ IMAGE
# =========================
elif option == "🖼️ Image" and sidebar_file:

    st.image(sidebar_file)

    text = extract_text_from_image(sidebar_file)

    st.text_area("Extracted Text", text)

    if st.button("Analyze Image"):
        result = agent_decision(text)
        st.markdown(result)
        show_confidence(result)


# =========================
# 📱 WHATSAPP
# =========================
elif option == "📱 WhatsApp" and sidebar_file:

    st.image(sidebar_file)

    text = extract_text_from_image(sidebar_file)

    st.text_area("Chat Text", text)

    if st.button("Detect Scam"):
        result = agent_decision(text)
        st.markdown(result)
        show_confidence(result)

        st.markdown(highlight_scam_words(text.lower()), unsafe_allow_html=True)


# =========================
# 📷 CAMERA
# =========================
elif option == "📷 Camera" and sidebar_file:

    st.image(sidebar_file)

    text = extract_text_from_image(sidebar_file)

    if st.button("Analyze"):
        result = agent_decision(text)
        st.markdown(result)
        show_confidence(result)


# =========================
# 📦 BARCODE
# =========================
elif option == "📦 Barcode" and sidebar_file:

    st.image(sidebar_file)

    from tools.barcode_scanner import scan_barcode

    results = scan_barcode(sidebar_file)

    if not results:
        st.info("Trying OCR fallback...")
        text = extract_text_from_image(sidebar_file)
        if text.strip():
            results = [text]

    if not results:
        st.warning("No data detected")
    else:
        for data in results:
            st.code(data)
            result = agent_decision(data)
            st.markdown(result)


# =========================
# 💳 UPI QR
# =========================
elif option == "💳 UPI QR" and sidebar_file:

    st.image(sidebar_file)

    from tools.barcode_scanner import scan_barcode, analyze_upi_qr

    results = scan_barcode(sidebar_file)

    if not results:
        st.warning("No QR detected")
    else:
        for data in results:
            st.code(data)

            upi_result = analyze_upi_qr(data)
            st.markdown(upi_result)

            ai_result = agent_decision(data)
            st.markdown(ai_result)
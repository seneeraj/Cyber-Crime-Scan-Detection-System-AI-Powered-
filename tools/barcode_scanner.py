import cv2
import numpy as np
from PIL import Image
import urllib.parse as urlparse
import re

# =========================
# 🔍 QR Scanner (OpenCV)
# =========================
def scan_barcode(file):
    try:
        image = Image.open(file).convert("RGB")
        img = np.array(image)

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)

        if data:
            return [data]

        # 🔄 Try multiple scales for better detection
        for scale in [0.5, 1.5, 2]:
            resized = cv2.resize(img, None, fx=scale, fy=scale)
            data, _, _ = detector.detectAndDecode(resized)
            if data:
                return [data]

        return []

    except Exception:
        return []


# =========================
# 💳 UPI CONFIG
# =========================
TRUSTED_UPI_HANDLES = [
    "@upi",
    "@okaxis",
    "@okhdfcbank",
    "@okicici",
    "@oksbi",
    "@pthdfc",   # HDFC Pay
    "@ybl",      # PhonePe
    "@ibl"       # ICICI
]

TRUSTED_BRANDS = [
    "amazon", "paytm", "phonepe", "gpay", "flipkart"
]


# =========================
# 🧠 Smart Lookalike Detection
# =========================
def is_lookalike(upi_id):
    suspicious_patterns = [
        "amaz0n", "g00gle", "paytmm", "faceb00k"
    ]
    return any(p in upi_id.lower() for p in suspicious_patterns)


# =========================
# 💳 UPI QR ANALYZER
# =========================
def analyze_upi_qr(data):

    # ❌ Not UPI
    if not data.startswith("upi://"):
        return "❌ Not a UPI QR code"

    parsed = urlparse.urlparse(data)
    params = urlparse.parse_qs(parsed.query)

    upi_id = params.get("pa", [""])[0]
    name = params.get("pn", [""])[0]
    amount = params.get("am", [""])[0]

    # =========================
    # 🧾 Base Info
    # =========================
    result = f"""
### 💳 UPI QR Details
- UPI ID: {upi_id}
- Name: {name if name else "Not provided"}
- Amount: {amount if amount else "Not specified"}
"""

    risks = []
    score = 0

    # =========================
    # 🧠 Smart Rules
    # =========================

    # ✅ Phone number UPI (safe pattern)
    if re.match(r"^\d{10}@", upi_id):
        score -= 10

    # ⚠️ Lookalike brand attack
    if is_lookalike(upi_id):
        risks.append("⚠️ Possible fake brand-style UPI ID")
        score += 10

    # ⚠️ Unknown handle
    if not any(h in upi_id for h in TRUSTED_UPI_HANDLES):
        risks.append("⚠️ Unknown or uncommon UPI handle")
        score += 15

    # ⚠️ High amount
    if amount:
        try:
            if float(amount) > 5000:
                risks.append("⚠️ High payment amount")
                score += 20
        except:
            pass

    # ⚠️ Brand mismatch
    if name:
        name_lower = name.lower()
        if any(b in name_lower for b in TRUSTED_BRANDS):
            if not any(b in upi_id.lower() for b in TRUSTED_BRANDS):
                risks.append("⚠️ Brand name mismatch with UPI ID")
                score += 20

    # ⚠️ Missing name
    if not name:
        risks.append("⚠️ Missing receiver name")
        score += 10

    # =========================
    # 🎯 Final Classification
    # =========================
    if score >= 60:
        level = "🔴 High Risk"
    elif score >= 30:
        level = "🟡 Suspicious"
    else:
        level = "🟢 Likely Safe"

    # Clamp score between 0–100
    score = max(0, min(score, 100))

    result += f"\n### 📊 Risk Score: {score}% ({level})\n"

    # =========================
    # 🚨 Issues Section
    # =========================
    if risks:
        result += "\n### 🚨 Issues Detected\n" + "\n".join(risks)
    else:
        result += "\n### ✅ No major risks detected"

    return result
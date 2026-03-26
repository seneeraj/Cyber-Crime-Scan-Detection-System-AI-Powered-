# core/agent.py

import re


# =========================
# 🎯 Scam Categories
# =========================
SCAM_CATEGORIES = {
    "banking": ["bank", "account", "blocked", "suspend", "verify", "kyc"],
    "otp": ["otp", "code", "verification", "pin"],
    "lottery": ["won", "prize", "lottery", "reward"],
    "job": ["earn", "salary", "income", "work", "job", "fee", "payment"],
    "tech_support": ["virus", "infected", "support", "call"],
}


# =========================
# 🔍 URL Extract
# =========================
def extract_url(text):
    pattern = r"(https?://[^\s]+)"
    match = re.search(pattern, text)
    return match.group(0) if match else None


# =========================
# 🔍 Scam Detection Logic
# =========================
def detect_scam(text):
    text_lower = text.lower()
    score = 0
    category = "unknown"

    for cat, keywords in SCAM_CATEGORIES.items():
        for word in keywords:
            if word in text_lower:
                score += 15
                category = cat

    if any(w in text_lower for w in ["urgent", "immediately", "blocked", "suspend"]):
        score += 25

    if any(w in text_lower for w in ["₹", "rs", "fee", "payment"]):
        score += 20

    if re.search(r"\d{10}", text):
        score += 10

    confidence = min(score, 100)

    return category, confidence


# =========================
# 🧠 Explanation Generator
# =========================
def generate_explanation(text, category):
    text_lower = text.lower()

    reasons = []
    flags = []

    if "urgent" in text_lower or "immediately" in text_lower:
        reasons.append("creates urgency")
        flags.append("Urgency detected")

    if "₹" in text_lower or "fee" in text_lower:
        reasons.append("asks for money")
        flags.append("Financial request")

    if "http" in text_lower:
        reasons.append("contains suspicious link")
        flags.append("Suspicious URL")

    if "otp" in text_lower:
        reasons.append("involves OTP")
        flags.append("OTP risk")

    if not reasons:
        reasons.append("matches known scam patterns")

    explanation = f"""
### 🧠 AI Reasoning
This message looks like a **{category.upper()} scam** because it {", ".join(reasons)}.

### 🚨 Red Flags
""" + "\n".join([f"- {f}" for f in flags]) + """

### 🛡️ Advice
- Do not click links
- Do not share personal data
- Verify with official source
"""

    return explanation


# =========================
# 🤖 MAIN FUNCTION
# =========================
def agent_decision(user_input):

    if not user_input:
        return "⚠️ No input provided."

    url = extract_url(user_input)

    category, confidence = detect_scam(user_input)
    if is_safe_context(user_input):
        return f"""
    Likely safe content
    This appears to be normal informational content (eg: resume, contact details).
    **Confidence:** Low risk
    No scam pattern detected in context
    """    

    # High confidence → show result
    if confidence >= 50:

        explanation = generate_explanation(user_input, category)

        result = f"""
## ⚠️ Scam Detected ({category.upper()})

**Confidence:** {confidence}%

{explanation}
"""

        # Simple URL note (no API yet)
        if url:
            result += "\n\n---\n\n### 🌐 URL Detected\n⚠️ This message contains a link. Be cautious."

        return result

    # Low confidence
    return f"""
🟢 Likely Safe

**Confidence:** {confidence}%

No strong scam signals detected.
"""

def is_safe_context(text):
    text_lower = text.lower()

    safe_patterns = [
        "contact",
        "resume",
        "cv",
        "linkedin",
        "email",
        "mobile",
        "skills",
        "profile"
    ]

    matches = sum(1 for word in safe_patterns if word in text_lower)

    return matches >= 2   # threshold
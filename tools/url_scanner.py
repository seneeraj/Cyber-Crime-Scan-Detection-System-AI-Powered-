import requests
import time
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    if "VIRUSTOTAL_API_KEY" in st.secrets:
        return st.secrets["VIRUSTOTAL_API_KEY"]
    return os.getenv("VIRUSTOTAL_API_KEY")


def scan_url(url):
    api_key = get_api_key()
    headers = {"x-apikey": api_key}

    # Step 1: Submit URL for scanning
    data = {"url": url}
    response = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers=headers,
        data=data
    )

    if response.status_code != 200:
        return "⚠️ Error submitting URL"

    analysis_id = response.json()["data"]["id"]

    # Step 2: Wait for analysis
    time.sleep(3)

    # Step 3: Fetch results
    result = requests.get(
        f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
        headers=headers
    )

    if result.status_code != 200:
        return "⚠️ Error fetching results"

    stats = result.json()["data"]["attributes"]["stats"]

    malicious = stats.get("malicious", 0)
    suspicious = stats.get("suspicious", 0)

    # Step 4: Decision logic
    if malicious > 0:
        status = "❌ Malicious"
    elif suspicious > 0:
        status = "⚠️ Suspicious"
    else:
        status = "✅ Safe"

    return f"""
🔍 **URL Scan Result**

Status: {status}

Details:
- Malicious: {malicious}
- Suspicious: {suspicious}
- Harmless: {stats.get("harmless", 0)}
"""
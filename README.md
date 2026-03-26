# 🛡️ Cyber Crime Scan Detection System (AI-Powered)

🚀 An intelligent, multi-modal AI system to detect scams, frauds, and cyber threats using text, images, audio, QR codes, and UPI analysis.

---

## 🌟 Features

### 💬 AI Chat (Reasoning Engine)
- ChatGPT-like interface
- Detect scam messages instantly
- Provides explanation + confidence score

### 📄 PDF Analysis
- Reads normal + scanned PDFs
- Uses OCR fallback for image-based PDFs

### 🎤 Voice Scam Detection
- Upload audio files (MP3/WAV)
- Converts speech → text → scam analysis

### 🖼️ Image OCR Scanner
- Extracts text from screenshots
- Detects phishing / fraud messages

### 📱 WhatsApp Screenshot Detector
- Upload chat screenshots
- Detect scam patterns automatically
- Highlights risky keywords

### 📷 Live Camera Scanner
- Capture image using webcam
- Real-time scam detection

### 📦 QR / Barcode Scanner
- Extracts data from QR codes
- OCR fallback for non-readable codes

### 💳 UPI QR Fraud Detection (India Focus 🇮🇳)
- Detect fake UPI QR codes
- Risk scoring system
- Checks:
  - Fake UPI IDs
  - Brand mismatch
  - Suspicious handles
  - High payment traps

---

## 🧠 How It Works

```text
Input (Text / Image / Audio / QR)
        ↓
Extraction (OCR / Speech-to-Text / QR Decode)
        ↓
AI Agent (Rule-based + Reasoning)
        ↓
Output:
- Scam Detection
- Risk Score
- Explanation
````

---

## 🖥️ Tech Stack

* **Frontend:** Streamlit
* **AI Logic:** Custom Rule-based + Reasoning Engine
* **OCR:** EasyOCR / Tesseract
* **Audio:** Faster-Whisper
* **QR Detection:** OpenCV
* **Language:** Python

---

## 📁 Project Structure

```
ai_cyber_guardian/
│
├── app.py
├── requirements.txt
├── LICENSE
├── README.md
├── .gitignore
│
├── core/
│   └── agent.py
│
└── tools/
    ├── barcode_scanner.py
    ├── ocr_reader.py
    ├── voice_to_text.py
    ├── file_parser.py
```

---

## 🚀 Run Locally

### 1️⃣ Clone repository

```bash
git clone https://github.com/your-username/ai_cyber_guardian.git
cd ai_cyber_guardian
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run app

```bash
streamlit run app.py
```

---

## 🌐 Deploy on Streamlit Cloud

1. Push code to GitHub
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Click **New App**
4. Select repo
5. Set:

```
Main file: app.py
```

6. Deploy 🚀

---

## ⚠️ Important Notes

* Use **Whisper tiny model** for faster performance
* OCR may require optimization on cloud
* Avoid uploading large files

---

## 🎯 Use Cases

* Detect phishing messages
* Identify fake payment QR codes
* Analyze suspicious WhatsApp chats
* Prevent UPI fraud
* Assist cybercrime awareness

---

## 🔮 Future Enhancements

* 🔐 Browser extension for real-time protection
* 📱 Android app version
* 🧠 AI model fine-tuning
* 🌍 Multi-language support
* 👨‍👩‍👧 Family safety dashboard

---

## 👨‍💻 Author

**Neeraj Bhatia**
AI & Data Science Enthusiast

---

## 📜 License

This project is licensed under the MIT License.

---

## ⭐ Support

If you like this project:

👉 Star ⭐ the repo
👉 Share with others
👉 Contribute improvements

---

🚀 *Building safer digital experiences with AI*

```



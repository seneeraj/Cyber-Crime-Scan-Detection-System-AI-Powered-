import easyocr
from PIL import Image
from pdf2image import convert_from_bytes
import numpy as np
import streamlit as st

# 🔥 Load OCR model once
reader = easyocr.Reader(['en'], gpu=False)


def extract_text_from_image(file):
    image = Image.open(file)
    image_np = np.array(image)

    results = reader.readtext(image_np, detail=0)

    return " ".join(results)


def extract_text_from_scanned_pdf(file):
    images = convert_from_bytes(file.read())

    full_text = ""

    for img in images:
        img_np = np.array(img)
        results = reader.readtext(img_np, detail=0)
        full_text += " ".join(results) + "\n"

    return full_text.strip()

@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'], gpu=False)


def extract_text_from_image(file):
    reader = load_reader()
    image = Image.open(file)
    image_np = np.array(image)

    results = reader.readtext(image_np, detail=0)
    return " ".join(results)


def extract_text_from_scanned_pdf(file):
    try:
        images = convert_from_bytes(file.read())
    except Exception:
        return ""   # return empty instead of crashing

    full_text = ""

    for img in images:
        try:
            img_np = np.array(img)
            results = reader.readtext(img_np, detail=0)
            full_text += " ".join(results) + "\n"
        except:
            continue

    return full_text.strip()   
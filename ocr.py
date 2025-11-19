import cv2
import pytesseract
import numpy as np
import re

def preprocess_image_for_ocr(img_bgr):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th

def extract_score_from_image_path(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return None
    proc = preprocess_image_for_ocr(img)
    texto = pytesseract.image_to_string(proc, config='--psm 6')
    m = re.search(r"(\d{1,2})\s*[-:xX]\s*(\d{1,2})", texto)
    if m:
        return f"{int(m.group(1))}x{int(m.group(2))}"
    return None

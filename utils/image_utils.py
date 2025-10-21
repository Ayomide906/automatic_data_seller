
import os
from PIL import Image, ImageEnhance
import cv2
import numpy as np
from pathlib import Path
from config import config


def ensure_image_directory():
    """Ensure the image storage directory exists"""
    config.RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    return config.RECEIPTS_DIR


def save_receipt_image(image_data, customer_phone):
    """Save receipt image with organized filename"""
    image_dir = ensure_image_directory()

    # Create organized filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"receipt_{customer_phone}_{timestamp}.jpg"
    file_path = image_dir / filename

    with open(file_path, 'wb') as f:
        f.write(image_data)

    return str(file_path)


def preprocess_image_for_ocr(image_path):
    """Preprocess image to improve OCR accuracy"""
    try:
        # Read image
        image = cv2.imread(image_path)

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply noise reduction
        denoised = cv2.medianBlur(gray, 3)

        # Apply thresholding
        _, thresholded = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Convert back to PIL Image for consistency
        pil_image = Image.fromarray(thresholded)

        return pil_image

    except Exception as e:
        print(f"Error preprocessing image: {e}")
        # Return original image if preprocessing fails
        return Image.open(image_path)


def extract_text_from_image(image_path):
    """Extract text from image using OCR"""
    try:
        processed_image = preprocess_image_for_ocr(image_path)
        text = pytesseract.image_to_string(processed_image)
        return text.strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""
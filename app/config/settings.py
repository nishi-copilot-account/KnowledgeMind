"""
Application configuration.
"""

from pathlib import Path

# -----------------------------
# OCR Configuration
# -----------------------------

TESSERACT_PATH = Path(
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# -----------------------------
# Data Directories
# -----------------------------

DATA_DIR = Path("data")

DOCUMENT_DIR = DATA_DIR / "documents"

IMAGE_DIR = DATA_DIR / "extracted_images"
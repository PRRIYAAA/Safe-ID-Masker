# Safe ID Masker

**Safe ID Masker** is a web-based application for automatic detection and masking of personally identifiable information (PII) in uploaded images and documents. It leverages OCR (Tesseract) to extract text and OpenAI GPT models to classify sensitive data, masking it directly on the image without affecting the rest of the document.

---

## Features

- **OCR Text Extraction:** Uses Tesseract to extract text and bounding box coordinates from images or PDF pages.
- **Automatic PII Detection:** Uses OpenAI GPT to identify sensitive information such as names, addresses, phone numbers, invoice numbers, amounts, and dates.
- **Pixel-Level Masking:** Draws black rectangles over detected PII areas while keeping the rest of the document intact.
- **File Upload & Download:** Supports PNG, JPG, and PDF file uploads; masked outputs can be downloaded immediately.
- **Simple Web Interface:** Users can upload documents, preview masked output, and download securely.
- **Environment Configuration:** API keys, file paths, and other settings stored in a `.env` file.
- **Optional Docker Support:** Includes Dockerfile and docker-compose setup for containerized deployment.

---

## Requirements

- Python 3.9+
- Flask
- OpenAI Python SDK
- pytesseract
- opencv-python
- pdf2image (for PDFs)
- Pillow
- python-dotenv

Optional:

- Docker & Docker Compose

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/safe-id-masker.git
cd safe-id-masker

## Configuration (.env)
# OpenAI API key
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx

# Tesseract OCR executable path
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe

# Folder to save masked files
UPLOAD_FOLDER=static/masked

```

## Architecture

User Upload
     │
     ▼
   Flask Server
     │
     ▼
  OCR Extraction (Tesseract)
     │
     ▼
 PII Detection (OpenAI GPT)
     │
     ▼
   Masking (OpenCV / PIL)
     │
     ▼
 Save & Download Masked File

```
## Web Interface
python app.py
```
1. Open a browser at http://127.0.0.1:5000/ to:

2. Upload a document (PNG, JPG, PDF)

3. Preview masked output

4.Download the masked file


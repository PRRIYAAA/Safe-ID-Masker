import os
import cv2
import pytesseract
from pytesseract import Output
import json
from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/masked"

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("API_KEY"))

# Tell pytesseract where tesseract.exe is installed (Windows only)
pytesseract.pytesseract.tesseract_cmd = r"E:\Tesseract-OCR\tesseract.exe"

@app.route("/", methods=["GET", "POST"])
def index():
    filename = None

    if request.method == "POST":
        if "image" not in request.files:
            return redirect(request.url)

        file = request.files["image"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(image_path)

            # Step 1: Load image
            img = cv2.imread(image_path)

            # Step 2: OCR
            data = pytesseract.image_to_data(img, output_type=Output.DICT)
            all_text = " ".join(data["text"])

            # Step 3: Ask LLM to detect PII
            prompt = f"""
            Here is extracted text from an invoice:

            {all_text}

            Identify which parts are sensitive PII (like names, addresses, phone numbers, 
            invoice numbers, PO numbers, customer IDs, amounts, dates). 

            Return only a JSON list of exact words to mask. Example: ["28510500", "Altoona", "104.67"]
            """

            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a PII detection tool. Return only valid JSON (a list of strings)."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            response_text = resp.choices[0].message.content.strip()
            try:
                if response_text.startswith("```"):
                    response_text = response_text.strip("```json").strip("```")
                pii_words = json.loads(response_text)
            except Exception:
                pii_words = []

            # Step 4: Mask detected PII
            for i, word in enumerate(data["text"]):
                if word in pii_words:
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)

            # Save masked image
            masked_path = os.path.join(app.config["UPLOAD_FOLDER"], "masked_" + file.filename)
            cv2.imwrite(masked_path, img)

            filename = "masked_" + file.filename

    return render_template("index.html", filename=filename)

if __name__ == "__main__":
    os.makedirs("static/masked", exist_ok=True)
    app.run(debug=True)

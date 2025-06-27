import os
from flask import Flask, render_template, request, jsonify
from openai_helper import get_openai_response
from PyPDF2 import PdfReader
from docx import Document

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '../templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '../static')
)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../uploads')
DOC_TEXT_PATH = os.path.join(UPLOAD_FOLDER, 'latest_doc.txt')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_pdf(filepath):
    text = ""
    try:
        reader = PdfReader(filepath)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"PDF extraction error: {e}")
    return text

def extract_text_from_docx(filepath):
    text = ""
    try:
        doc = Document(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"DOCX extraction error: {e}")
    return text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message")
    doc_context = ""
    if os.path.exists(DOC_TEXT_PATH):
        with open(DOC_TEXT_PATH, "r", encoding="utf-8") as f:
            doc_context = f.read()
    try:
        reply = get_openai_response(user_message, doc_context)
        return jsonify({"response": reply})
    except Exception as e:
        print("Error in /ask:", e)
        return jsonify({"response": "Sorry, I couldn't process your request. Please try again later."}), 500

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    # Extract text if PDF or DOCX
    ext = file.filename.lower().split('.')[-1]
    text = ""
    if ext == "pdf":
        text = extract_text_from_pdf(filepath)
    elif ext == "docx":
        text = extract_text_from_docx(filepath)
    if text:
        with open(DOC_TEXT_PATH, "w", encoding="utf-8") as f:
            f.write(text)
    return jsonify({"success": True, "message": f"File '{file.filename}' uploaded and processed."})

if __name__ == "__main__":
    app.run(debug=True) 
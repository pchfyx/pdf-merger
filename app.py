from flask import Flask, request, send_file, render_template_string, jsonify
from PyPDF2 import PdfMerger
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_TEMPLATE_INDEX = open('index.html').read()
HTML_TEMPLATE_SORT = open('sort.html').read()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE_INDEX)

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('files')
    if len(files) < 2:
        return "Please upload at least two PDF files to merge.", 400

    filepaths = []
    for file in files:
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        filepaths.append(unique_filename)

    return jsonify({'filepaths': filepaths})

@app.route('/sort')
def sort():
    return render_template_string(HTML_TEMPLATE_SORT)

@app.route('/merge', methods=['POST'])
def merge():
    data = request.get_json()
    files = data.get('files', [])
    if len(files) < 2:
        return "Please upload at least two PDF files to merge.", 400

    merger = PdfMerger()
    filepaths = [os.path.join(UPLOAD_FOLDER, file) for file in files]

    for file_path in filepaths:
        merger.append(file_path)

    output_filename = os.path.join(UPLOAD_FOLDER, 'merged.pdf')
    merger.write(output_filename)
    merger.close()

    return send_file(output_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

# app.py
from flask import Flask, request, render_template, jsonify
import tempfile, os, base64
import fitz  # PyMuPDF
from datetime import datetime
from your_pdf_script import insert_image_and_text_into_pdf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/generate', methods=['POST'])
def generate_pdf():
    try:
        # Collect form data
        name = request.form.get('name', '')
        disaster = request.form.get('disaster', '')
        location = request.form.get('location', '')
        timestamp = request.form.get('datetime', datetime.now().strftime("%d-%m-%Y %H:%M"))

        photo = request.files.get('photo')
        if not photo:
            return jsonify({'error': 'No photo uploaded'}), 400

        with tempfile.TemporaryDirectory() as tmpdir:
            # Save uploaded image
            temp_img_path = os.path.join(tmpdir, 'photo.jpg')
            photo.save(temp_img_path)

            # Output PDF path
            output_pdf_path = os.path.join(tmpdir, 'output.pdf')

            # Text entries to insert
            text_entries = [
                {'text': name,      'x': 60,  'y': 280, 'fontsize': 12},
                {'text': disaster,  'x': 60,  'y': 437, 'fontsize': 12},
                {'text': timestamp, 'x': 60,  'y': 475, 'fontsize': 12},
                {'text': location,  'x': 60,  'y': 511, 'fontsize': 12},
            ]

            # Insert image + text into certificate template
            insert_image_and_text_into_pdf(
                pdf_path="certificate.pdf",   # base template
                image_path=temp_img_path,
                output_path=output_pdf_path,
                page_number=0,
                x=230, y=230, width=350, height=280,
                text_entries=text_entries
            )

            # Generate preview image (optimized)
            with fitz.open(output_pdf_path) as doc:
                page = doc.load_page(0)
                # 🔹 Use normal scale (1x) or 1.5x for balance
                pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))
                # 🔹 Export as JPEG instead of PNG (much smaller)
                img_bytes = pix.tobytes("jpeg")
                # img_bytes = pix.tobytes("png")

            # Read PDF bytes
            with open(output_pdf_path, 'rb') as f:
                pdf_bytes = f.read()

        # Encode to base64 for frontend
        return jsonify({
            'pdf': base64.b64encode(pdf_bytes).decode('utf-8'),
            'image': base64.b64encode(img_bytes).decode('utf-8'),
            'filename_pdf': 'report.pdf',
            'filename_img': 'report.png'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, send_from_directory, render_template
from werkzeug.utils import secure_filename
import subprocess, os
from PIL import Image
from docx import Document
import cairosvg
import logging
import sys

app = Flask(__name__)

# Configuration

app.config['UPLOAD_FOLDER'] = os.path.abspath('uploads')  # Absolute path to the uploads folder
app.logger.info(f"Upload folder absolute path: {app.config['UPLOAD_FOLDER']}")
app.config['ALLOWED_EXTENSIONS'] = {'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'jpg', 'png', 'svg'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Set up logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def convert_docx_to_pdf(input_path, output_path):
    try:
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', input_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Error during DOCX to PDF conversion: {e}")
        return False

def convert_jpg_to_png(input_path, output_path):
    try:
        with Image.open(input_path) as img:
            img.save(output_path, format='PNG')
        return True
    except Exception as e:
        app.logger.error(f"Error converting JPG to PNG: {e}")
        return False

def convert_png_to_jpg(input_path, output_path):
    try:
        with Image.open(input_path) as img:
            rgb_im = img.convert('RGB')
            rgb_im.save(output_path, format='JPEG')
        return True
    except Exception as e:
        app.logger.error(f"Error converting PNG to JPG: {e}")
        return False

def convert_odt_to_docx(input_path, output_path):
    try:
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'docx', input_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Error converting ODT to DOCX: {e}")
        return False

def convert_excel_to_pdf(input_path, output_path):
    try:
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', input_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Error during Excel to PDF conversion: {e}")
        return False

def convert_ppt_to_pdf(input_path, output_path):
    try:
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', input_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Error during PPT to PDF conversion: {e}")
        return False

def convert_doc_to_pdf(input_path, output_path):
    try:
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', input_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Error during DOC to PDF conversion: {e}")
        return False

def convert_txt_to_doc(input_path, output_path):
    try:
        doc = Document()
        with open(input_path, 'r') as file:
            for line in file:
                doc.add_paragraph(line)
        doc.save(output_path)
        return True
    except Exception as e:
        app.logger.error(f"Error converting TXT to DOC: {e}")
        return False
    
def convert_svg_to_png(input_path, output_path):
    try:
        cairosvg.svg2png(url=input_path, write_to=output_path)
        return True
    except Exception as e:
        app.logger.error(f"Error converting SVG to PNG: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        # Extract the file extension and convert it to lowercase
        file_ext = filename.rsplit('.', 1)[1].lower()

        # Modify output_path to be in the same folder as app.py
        output_filename = filename.rsplit('.', 1)[0] + '.pdf'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        success = False
        if file_ext == 'docx':
            success = convert_docx_to_pdf(input_path, output_path)
        elif file_ext == 'jpg':
            success = convert_jpg_to_png(input_path, output_path)
        elif file_ext == 'png':
            success = convert_png_to_jpg(input_path, output_path)
        elif file_ext == 'odt':
            success = convert_odt_to_docx(input_path, output_path)
        elif file_ext == 'ods':
            success = convert_excel_to_pdf(input_path, output_path)
        elif file_ext == 'odp':
            success = convert_ppt_to_pdf(input_path, output_path)
        elif file_ext == 'txt':
            success = convert_txt_to_doc(input_path, output_path)
        elif file_ext == 'svg':
            success = convert_svg_to_png(input_path, output_path)
        # Note: Add additional file conversion cases here as required

        if success:
            return send_from_directory(os.path.abspath(os.path.dirname(__file__)), filename=output_filename, as_attachment=True)

        else:
            return 'File conversion failed', 500

    return 'File not allowed', 400

if __name__ == '__main__':
    app.run(threaded=True, debug=True)

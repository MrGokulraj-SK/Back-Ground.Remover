from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def removebg(img_path):
    input_image = Image.open(img_path)
    return remove(input_image)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            original_filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, original_filename)
            file.save(file_path)

            result_path = os.path.join(UPLOAD_FOLDER, 'result.png')
            result = removebg(file_path)
            result.save(result_path)

            return render_template('result.html', original_img=original_filename, result_img=result_path)

    return render_template('index.html')

@app.route('/static/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/<filename>')
def download_result(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.static_url_path = '/static'
    app.run(debug=True)

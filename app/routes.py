import os
from flask import Blueprint, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from app.utils import resize_image, upload_to_blob
from io import BytesIO
import requests

bp = Blueprint('routes', __name__)

# Max size in bytes (1 MB = 1 * 1024 * 1024)
MAX_SIZE = 1 * 1024 * 1024

@bp.route('/')
def index():
    return render_template('upload.html')

@bp.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)

        # Resize image
        img_stream = BytesIO(file.read())  # Read the file into a byte stream
        resized_image = resize_image(img_stream, MAX_SIZE)

        # Upload to Azure Blob Storage
        blob_url = upload_to_blob(resized_image, filename)

        # Download the image from Azure Blob Storage
        image_data = requests.get(blob_url).content

        return jsonify({
            'url': blob_url,
            'filename': filename
        }), 200

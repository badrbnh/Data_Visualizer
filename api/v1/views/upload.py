from api.v1.views import app_views
from models.user import User
from models import db_storage
from flask import jsonify, abort, make_response, request
import os
from werkzeug.utils import secure_filename
from models.data import Data
from models.img import Img

FILE_ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'csv'}
IMG_ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'}
UPLOAD_FOLDER = '/home/chikara/Programming/Projects/Data_Visualizer/data'
STATIC_FOLDER = '/home/chikara/Programming/Projects/Data_Visualizer/web_flask/static/resources'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app_views.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    user_id = request.form.get('user_id')

    if allowed_file(file.filename, IMG_ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        file_path = os.path.join(STATIC_FOLDER, filename)
        file.save(file_path)
        img = Img(img_name=filename, user_id=user_id)
        db_storage.new(img)
        db_storage.save()

        return make_response(jsonify({'success': 'Image uploaded successfully'}), 200)

    if allowed_file(file.filename, FILE_ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, 'dr', filename)
        file.save(file_path)
        data = Data(file_name=filename, user_id=user_id)
        db_storage.new(data)
        db_storage.save()
        data.save_df()

        return make_response(jsonify({'success': 'File uploaded successfully'}), 200)

    return make_response(jsonify({'error': 'Invalid file format'}), 400)
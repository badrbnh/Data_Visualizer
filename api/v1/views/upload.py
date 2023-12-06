from api.v1.views import app_views
from models.user import User
from models import db_storage
from flask import jsonify, abort, make_response, request
import os
from werkzeug.utils import secure_filename
from models.data import Data

ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'csv'}
UPLOAD_FOLDER = '/home/ubuntu/Data_Visualizer/data/dr'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app_views.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Get the user_id from the request payload
    user_id = request.form.get('user_id')  # Assuming user_id is passed in the form data
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        data = Data(file_name=filename, user_id=user_id)  # Pass the user_id to the Data object
        db_storage.new(data)
        db_storage.save()
        data.save_df()

        return make_response(jsonify({'success': 'File uploaded successfully'}), 200)

    return make_response(jsonify({'error': 'Invalid file format'}), 400)

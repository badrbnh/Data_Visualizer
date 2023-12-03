from flask import jsonify, make_response, abort
from api.v1.views import app_views
from models.data import Data
from models import db_storage
import pandas as pd
import os
@app_views.route("/data", methods=['POST', 'GET'], strict_slashes=False)
def get_all_data():
    """Retrieve all files."""
    data = db_storage.all(Data)
    files = []
    for file in data.values():
        files.append(file.to_dict())
    return jsonify(files)
    
    

@app_views.route("/data/<file_id>", methods=['POST', 'GET'], strict_slashes=False)
def get_data(file_id):
    """Retrieve the processed data."""
    
    #retrieve file naem
    data = file = db_storage.get(Data, file_id)
    
    full_file_name = data.file_name
    file_name = full_file_name.split(".")[0]


        # Check if the file exists
    file_path = os.path.join("data/df", file_name + ".csv")
    if os.path.exists(file_path):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Convert DataFrame to dictionary and return as JSON
        data_dict = df.to_dict(orient='records')
        return make_response(jsonify(data_dict), 200)
    else:
        return make_response(jsonify({'error': 'CSV file not found'}), 404)

@app_views.route("/data/<file_id>", methods=['DELETE'], strict_slashes=False)
def delete_data(file_id):
    data = db_storage.get(Data, file_id)
    if not data:
        abort(404)
    
    db_storage.delete(data)
    db_storage.save()
    return make_response(jsonify({}), 200)

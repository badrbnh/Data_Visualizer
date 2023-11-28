from flask import jsonify, make_response
from api.v1.views import app_views
from models.data import Data
from models import db_storage
import pandas as pd
import os

@app_views.route("/data", methods=['GET'], strict_slashes=False)
def get_data():
    """Retrieve the processed data."""
    file_name_value = "Data-for-Practice.xlsx"
    
    # Retrieve the user with the specified file name
    user = next((user for user in db_storage.all(Data).values() if user.file_name == file_name_value), None)

    if user:
        # Check if the file exists
        file_path = os.path.join("data/df", "Book1.csv")
        if os.path.exists(file_path):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Convert DataFrame to dictionary and return as JSON
            data_dict = df.to_dict(orient='records')
            return make_response(jsonify(data_dict), 200)
        else:
            return make_response(jsonify({'error': 'CSV file not found'}), 404)
    else:
        return make_response(jsonify({'error': 'User not found for the specified file name'}), 404)

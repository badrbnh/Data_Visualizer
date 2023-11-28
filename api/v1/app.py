from models import db_storage
from api.v1.views import app_views
from os import environ
from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close_db(error):
    """close database"""
    db_storage.close()
    
@app.errorhandler(HTTPException)
def handle_error(e):
    """Return Json 404 error response"""
    response = jsonify(error="Not found")
    response.status_code = 404
    return response


if __name__ == '__main__':
    host = environ.get("DV_API_HOST")
    port = environ.get("DV_API_PORT")
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True, debug=True)
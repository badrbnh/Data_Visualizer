from api.v1.views import app_views
from models.user import User
from models.data import Data
from models import db_storage
from flask import jsonify

@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """return status of the api"""
    return jsonify({"status": "OK"})

@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    classes = [User, Data]
    names = ["User", "Data"]
    
    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = db_storage.count(classes[i])
    return jsonify(num_objs)
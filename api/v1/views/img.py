from flask import jsonify, make_response, abort
from api.v1.views import app_views
from models.img import Img
from models import db_storage

@app_views.route("/img", methods=['POST', 'GET'], strict_slashes=False)
def get_all_imgs():
    """Retrieve all images."""
    img = db_storage.all(Img)
    content = []
    for obj in img.values():
        content.append(obj.to_dict())
    return jsonify(content)

@app_views.route("/img/user/<user_id>", methods=["POST", "GET"], strict_slashes=False)
def get_user_img(user_id):
    """Retrive image of a specific user"""
    img = db_storage.all(Img)
    content = []
    for obj in img.values():
        if obj.user_id == user_id:
            content.append(obj.to_dict())
    if content:
        return jsonify(content)
    else:
        abort(404)

@app_views.route("/img/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_img(user_id):
    """delete image of a specific user"""
    img = db_storage.all(Img)
    if not img:
        abort(404)
    for obj in img.values():
        if obj.user_id == user_id:
            db_storage.delete(obj)
            db_storage.save()
    return make_response(jsonify({}), 200)

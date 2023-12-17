from flask import jsonify, make_response, abort, render_template
from api.v1.views import app_views
from models.user import User
from models import db_storage

@app_views.route('/verify/<receiver_email>/<verification_token>', methods=['GET'], strict_slashes=False)
def verify_email_token(receiver_email, verification_token):
    users = db_storage.all(User)
    for user in users.values():
        if user.verification_token == verification_token:
            if not user or user.email != receiver_email:
                abort(404)
            user.is_verified = 1
            db_storage.save()
    return render_template("verification_email.html")

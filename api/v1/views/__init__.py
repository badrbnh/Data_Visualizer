from flask.blueprints import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.data import *
from api.v1.views.img import *
from api.v1.views.emailVerification import *
from api.v1.views.upload import *
from models.engine.dbStorage import DBStorage
from os import getenv
from web_flask import app
storage_t = getenv("DV_TYPE_STORAGE")
db_storage = DBStorage(app)
db_storage.reload()
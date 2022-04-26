from flask import Blueprint

bp = Blueprint('hospital_management', __name__)


from . import routes
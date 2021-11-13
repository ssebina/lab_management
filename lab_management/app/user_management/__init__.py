from flask import Blueprint

bp = Blueprint('user_management', __name__)

from . import routes
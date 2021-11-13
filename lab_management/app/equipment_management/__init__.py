from flask import Blueprint

bp = Blueprint('equipment_management', __name__)

from . import routes
from flask import Blueprint
from flask import current_app as app

auth_bp = Blueprint(
    'auth_bp', __name__,
    url_prefix='/auth',
    template_folder='templates',
    static_folder='static'
)
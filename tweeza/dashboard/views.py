from flask import Blueprint

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/')
def index():
    return "hi from dashboard"

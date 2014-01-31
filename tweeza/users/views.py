from flask import Blueprint, abort, render_template
from flask.ext.login import login_required, current_user

users = Blueprint('users', __name__, url_prefix='/profile')


@users.route('/')
@login_required
def index():
    if not current_user.is_authenticated():
        abort(403)
    return render_template('users/index.html', user=current_user)


@users.route('/setup')
def setup():
    pass

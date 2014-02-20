from flask import Blueprint, abort, render_template
from flask.ext.login import login_required, current_user
from users.models import User
from items.models import Item

users = Blueprint('users', __name__, url_prefix='/profile')


@users.route('/')
@login_required
def index():
    if not current_user.is_authenticated():
        abort(403)
    return render_template('users/index.html', user=current_user)


@users.route('/user/<int:id>')
def user_profile(id):
    user = User.objects.get_or_404(user_id=id)
    items_count = Item.objects(submitter=user).count()
    return render_template('users/user_profile.html',
                           user=user,
                           items_count=items_count)


@users.route('/setup')
def setup():
    pass

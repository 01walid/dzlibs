from flask import (Blueprint, render_template, flash, request, redirect,
                   url_for)
from flask.ext.login import login_required, current_user
from users.models import User
from items.models import Item
from users.forms import EditProfileForm
from flask.ext.babel import gettext as _

users = Blueprint('users', __name__, url_prefix='/profile')


@users.route('/')
@login_required
def index():
    items_count = Item.objects(submitter=current_user.id).count()
    return render_template('users/user_profile.html', user=current_user,
                           items_count=items_count)


@users.route('/edit/', methods=['GET', 'POST'])
@login_required
def edit():

    form = EditProfileForm()

    if request.method == 'POST':

        if form.validate_on_submit():
            user = User.objects.get(id=current_user.id)
            user.name = form.name.data.strip()
            user.email = form.email.data.strip()
            user.website = form.website.data.strip()
            user.twitter_username = form.twitter.data.strip('@')
            facebook = form.facebook.data.strip().strip('/').split('/')[-1]
            user.facebook_username = facebook
            user.location = form.location.data.strip()
            user.hireable = bool(form.hireable.data)
            user.bio = form.bio.data.strip()
            user.save()
            flash(_('Profile updated successfully'), category='success')
            return redirect(url_for('users.index'))
        else:
            flash(_('Error happened, see below'), category='alert')
            return render_template('users/edit_profile.html', form=form)
    else:
        form.hireable.default = int(bool(current_user.hireable))
        form.bio.default = current_user.bio or ''
        form.process()

    return render_template('users/edit_profile.html', form=form)


@users.route('/user/<int:id>')
def user_profile(id):
    user = User.objects.get_or_404(user_id=id)
    items_count = Item.objects(submitter=user).count()
    return render_template('users/user_profile.html',
                           user=user,
                           items_count=items_count)

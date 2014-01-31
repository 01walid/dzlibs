from flask import (Blueprint, request, redirect, session, url_for,
                   render_template, flash)
from flask.ext.login import (login_required, login_user, current_user,
                             logout_user)
from users import User
from flask.ext.babel import gettext as _
from forms import LoginForm, SignupForm, CreateProfileForm
from extensions import github
from items.models import Item

frontend = Blueprint('frontend', __name__)


@frontend.route("/")
def index():
    items = Item.objects.all()
    return render_template('frontend/index.html', items=items)


@frontend.route("/about")
def about():
    return render_template('frontend/about.html')


@frontend.route("/oauth/github")
def oauth_github():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    redirect_uri = url_for('frontend.callback',
                           next=request.args.get('next') or
                           request.referrer or None, _external=True)

    params = {'redirect_uri': redirect_uri, 'scope': 'user:email'}
    return redirect(github.get_authorize_url(**params))


# Step 2: User authorization, this happens on the provider.

@frontend.route("/callback")
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    if not 'code' in request.args:
        flash('You did not authorize the request')
        return redirect(url_for('frontend.login'))

    # make a request for the access token credentials using code
    redirect_uri = url_for('frontend.callback', _external=True)

    data = dict(code=request.args['code'],
                redirect_uri=redirect_uri,
                scope='user:email,public_repo')

    auth = github.get_auth_session(data=data)

    # the "me" response
    githuber = auth.get('user').json()
    # return jsonify(githuber)
    try:
        user = User.objects.get(github_id=githuber['id'])
    except User.DoesNotExist:
        user = None

    if user:
        login_user(user)
        flash('Logged in as ' + githuber['name'])
        return redirect(url_for('users.index'))
    else:
        session['github_id'] = githuber['id']
        session['name'] = githuber['name']
        session['email'] = githuber['email']
        session['location'] = githuber['location']
        session['github_username'] = githuber['login']
        session['oauth_token'] = auth.access_token

        form = CreateProfileForm(email=githuber['email'])
        return render_template('frontend/create_profile.html',
                               form=form)
        # return redirect(url_for('frontend.create_profile'))


@frontend.route('/create_profile', methods=['POST'])
def create_profile():
    if current_user.is_authenticated():
        return redirect(url_for('users.index'))

    form = CreateProfileForm()

    if form.validate_on_submit():
        user = User()
        user.email = form.email.data.strip()
        user.password = form.password.data
        user.github_id = session['github_id']
        user.name = session['name']
        user.github_username = session['github_username']
        user.oauth_token = session['oauth_token']
        user.location = session['location']
        user.save()

        if login_user(user):
            flash(_("Logged in"), 'success')

        return redirect(url_for('users.index'))

    return render_template('frontend/create_profile.html',
                           form=form)


@frontend.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('users.index'))

    next = request.args.get('next', None)

    loginForm = LoginForm(login=request.args.get('login', None),
                          next=next)

    signupForm = SignupForm(next=next)

    if loginForm.validate_on_submit():
        user = User.objects.get(email=loginForm.email.data.strip())
        if user:
            if user.check_password(loginForm.password.data):
                remember = loginForm.remember.data
                if login_user(user, remember=remember):
                    flash(_("Logged in"), 'success')
                return redirect(loginForm.next.data or url_for('users.index'))
            else:
                flash(_('Sorry, invalid password'), 'error')
        else:
            flash(_("Sorry, incorrect email!"), 'error')

    return render_template('frontend/login.html',
                           loginForm=loginForm,
                           signupForm=signupForm)


@frontend.route('/logout')
@login_required
def logout():
    logout_user()
    flash(_('Logged out'), 'success')
    return redirect(url_for('frontend.index'))


@frontend.route('/signup', methods=['POST'])
def signup():
    if current_user.is_authenticated():
        return redirect(url_for('user.index'))

    loginForm = LoginForm()
    form = SignupForm(next=request.args.get('next'))

    if form.validate_on_submit():
        user = User()
        user.email = form.email.data.strip()
        user.name = form.name.data.strip()
        user.password = form.password.data
        user.save()

        if login_user(user):
            return redirect(form.next.data or url_for('users.index'))

    return render_template('frontend/login.html',
                           loginForm=loginForm,
                           signupForm=form)


@frontend.route('/help')
def help():
    return render_template('frontend/footers/help.html', active="help")

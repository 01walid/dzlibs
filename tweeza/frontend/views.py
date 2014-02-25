from flask import (Blueprint, request, redirect, url_for, abort,
                   render_template, flash, current_app as app)
from flask.ext.login import (login_required, login_user, current_user,
                             logout_user)
from users.models import User
from frontend.forms import ContactForm
from flask.ext.babel import gettext as _
from items.models import Item, Category
from flask.ext.mongoengine import Pagination
from flask_mail import Message
from extensions import cache, mail

frontend = Blueprint('frontend', __name__)

github = None  # Global object


@frontend.route("/")
@cache.cached(60)
def index():
    items = Item.objects[:12]
    categories = Category.objects.all()
    return render_template('frontend/index.html', items=items,
                           categories=categories)


@frontend.route("/about/")
@cache.cached(60)
def about():
    return render_template('frontend/about.html')


@frontend.route("/oauth/github")
def oauth_github():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    from extensions import github_oauth
    global github
    github = github_oauth(app)
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
        flash('You did not authorize the request', category='alert')
        return redirect(url_for('frontend.login'))

    # make a request for the access token credentials using code
    redirect_uri = url_for('frontend.callback', _external=True)

    data = dict(code=request.args['code'],
                redirect_uri=redirect_uri,
                scope='user:email,public_repo')

    auth = github.get_auth_session(data=data)

    # the "me" response
    githuber = auth.get('user').json()
    user = None
    try:
        user = User.objects.get(github_id=githuber['id'])
    except User.DoesNotExist:
        user = None

    if user:
        login_user(user)
        flash('Logged in as ' + githuber['name'], category='success')
        return redirect(url_for('frontend.index'))
    else:
        user = User()
        # mandatory information
        user.email = githuber['email'] if 'email' in githuber else None
        location = githuber['location'] if 'location' in githuber else None
        user.location = location
        name = githuber['name'] if 'name' in githuber else githuber['login']
        user.name = name

        # required information
        user.github_id = githuber['id']
        user.github_username = githuber['login']
        user.oauth_token = auth.access_token

        user.save()

        if login_user(user):
            flash(_("Logged in as %s, now get a shiny profile :)" % user.name),
                  category='success')

        return redirect(url_for('users.edit'))


@frontend.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        flash('Already Logged in as %s' % current_user, category='success')
        return redirect(url_for('frontend.index'))

    return render_template('frontend/login.html')


@frontend.route('/logout')
@login_required
def logout():
    logout_user()
    flash(_('Logged out'), 'success')
    return redirect(url_for('frontend.index'))


# for anything that have pagination, don't change <param> to something else
# we use this generic name to generate pagination

@frontend.route('/tag/<param>/<int:page>/')
@frontend.route('/tag/<param>/')
@cache.cached(60)
def tag(param, page=1):
    items = Pagination(Item.objects(tags=param), page, 12)
    if len(items.items) == 0:
        return abort(404)
    return render_template('frontend/tag.html', tag=param, items=items)


@frontend.route('/category/<param>/<int:page>/')
@frontend.route('/category/<param>/')
@cache.cached(60)
def category(param, page=1):
    categories = Category.objects.all()
    category = categories.get_or_404(name_en__iexact=param)

    items = Pagination(Item.objects(category=category), page, 12)

    return render_template('frontend/category_listing.html',
                           items=items,
                           current_category=category,
                           categories=categories)


@frontend.route('/user/<int:param>/items/')
@frontend.route('/user/<int:param>/items/<int:page>')
def user_items(param, page=1):
    user = User.objects.get_or_404(user_id=param)
    items = Pagination(Item.objects(submitter=user), page, 12)

    if len(items.items) == 0:
        return abort(404)

    return render_template('frontend/user_items.html',
                           items=items,
                           user=user)


@frontend.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':

        if form.validate_on_submit():

            name = form.name.data.strip()
            email = form.email.data.strip()
            subject = form.subject.data.strip()
            message = form.message.data.strip()

            msg = Message(subject, sender=email,
                          recipients=app.config['ADMINS'])
            msg.body = """
            From: %s <%s>
            Message:
            %s
            """ % (name, email, message)
            mail.send(msg)

            flash(_('Message sent successfully'), category='success')
            return render_template('frontend/contact.html', form=form)
        else:
            flash(_('Error happened, see below'), category='alert')
            return render_template('frontend/contact.html', form=form)
    else:
        return render_template('frontend/contact.html', form=form)


@frontend.route('/search/')
def search_page():
    return render_template('frontend/search_result.html', items=None)


@frontend.route('/search/<param>/<page>')
@frontend.route('/search/<param>')
@cache.cached(60)
def search(param, page=1):

    items = Pagination(Item.objects(titles__title__icontains=param),
                       1, 12)
    return render_template('frontend/search_result.html', items=items)


@frontend.route('/', defaults={'path': ''}, subdomain='api')
def api():
    return url_for('frontend.api')


# just for fun
@frontend.route("/404/")
@cache.cached(3000)
def _404():
    return abort(404)

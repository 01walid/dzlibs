from flask import (Blueprint, request, render_template, flash,
                   Response, stream_with_context, abort, send_file,
                   current_app as app)
from werkzeug import secure_filename
from flask.views import MethodView
from users.models import User
from models import Item, Titles
from flask.ext.login import login_required, current_user
from forms import AddItemForm
from utils import allowed_thumbnails, allowed_file, make_dir
from mongoengine.fields import GridFSProxy
from extensions import cache
import requests
import os
import tempfile

items = Blueprint('items', __name__)


class ListView(MethodView):
    decorators = [cache.cached(3600 * 24 * 7)]

    def get(self, page=1):
        items = Item.objects.paginate(page=page, per_page=5)
        return render_template('items/items_list.html', items=items)


class DetailView(MethodView):
    decorators = [cache.cached(400)]

    def get(self, item_id):
        item = Item.objects.get_or_404(item_id=item_id)

        if item.github:
            repo = item.github.strip('/').split('/')  # remove trailing slahes
            repo_name = repo[-1]
            user = repo[-2]
            url = 'https://api.github.com/repos/%s/%s/readme' \
                  % (user, repo_name)
            payload = {'client_id': app.config['GITHUB_CONSUMER_KEY'],
                       'client_secret': app.config['GITHUB_CONSUMER_SECRET']}
            headers = {'Accept': 'application/vnd.github.v3.raw'}
            description = requests.get(url, headers=headers, params=payload)
            zip_link = "https://api.github.com/repos/%s/%s/tarball" \
                       % (item.submitter.github_username, repo_name)
            clone_string = 'git clone https://github.com/%s/%s.git' \
                           % (item.submitter.github_username, repo_name)
            return render_template('items/item_details.html', item=item,
                                   content=description.text,
                                   zip_link=zip_link,
                                   clone_string=clone_string)
        return render_template('items/item_details.html', item=item)


class AddView(MethodView):

    def get(self):
        form = AddItemForm()
        return render_template('items/add_item.html', form=form)

    def post(self):

        form = AddItemForm()
        item = Item()

        if form.validate_on_submit():
            ar_title = Titles()
            fr_title = Titles()
            en_title = Titles()

            ar_title.title = form.ar_title.data.strip()
            ar_title.lang = 'ar'

            fr_title.title = form.fr_title.data.strip()
            fr_title.lang = 'fr'

            en_title.title = form.en_title.data.strip()
            en_title.lang = 'en'

            item.titles.append(ar_title)
            item.titles.append(fr_title)
            item.titles.append(en_title)

            item.description = form.description.data
            item.tags = form.tags.data.split(',')

            item.submitter = User.objects.get(id=current_user.id)

            thumbnail = request.files['thumbnail']
            thumbnail_name = secure_filename(thumbnail.filename)

            if thumbnail and allowed_thumbnails(thumbnail_name):
                ext = thumbnail.mimetype.split('/')[-1]
                # use the 'thumbnail' name for all thumbnails
                filename = '.'.join(["thumbnail", ext])
                item.thumbnail.put(thumbnail.stream,
                                   content_type=thumbnail.mimetype,
                                   filename=filename)

            if form.github.data:
                item.github = form.github.data
                item.save()
                # no need to process any uploaded files
                flash('Item submitted successfully', category='success')
                return render_template('items/add_item.html', form=form)

        else:
            flash('upload unsuccessful', category='error')
            return render_template('items/add_item.html', form=form)

        uploaded_files = request.files.getlist("files")
        for file in uploaded_files:
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Check if the file is one of the allowed types/extensions
            if file and allowed_file(filename):
                # put the file in the ListField.
                # see https://gist.github.com/tfausak/1299339
                file_ = GridFSProxy()
                file_.put(file.stream,
                          content_type=file.mimetype,
                          filename=filename)
                item.files.append(file_)
        # Save the thing
        item.save()
        flash('upload successful')
        return render_template('items/add_item.html', form=form)


@items.route('/thumbnails/<int:item_id>/<filename>')
def serve_thumbnail(item_id, filename):
    tmp_path = tempfile.gettempdir()
    path = os.path.join(tmp_path, 'dzlibs', str(item_id), filename)
    if os.path.isfile(path):
        return send_file(path)

    # else
    item = Item.objects.get(item_id=item_id)
    if filename == item.thumbnail.filename:
        dzlibs_path = os.path.join(tmp_path, 'dzlibs')
        make_dir(dzlibs_path)
        make_dir(os.path.join(dzlibs_path, str(item_id)))
        f = open(path, 'wb')
        f.write(item.thumbnail.read())
        f.close
        return send_file(path)

    return abort(404)


@items.route('/uploads/<int:item_id>/<filename>')
def serve_file(item_id, filename):
    item = Item.objects.get(item_id=item_id)
    for file in item.files:
        if file.filename == filename:
            return Response(stream_with_context(file.read()),
                            mimetype=file.content_type,
                            headers={"Content-Disposition":
                                     "attachment;filename=%s" % (filename)})
    return abort(404)

# Register the urls
items.add_url_rule('/items/', view_func=ListView.as_view('index'))
items.add_url_rule('/items/<int:page>/',
                   view_func=ListView.as_view('paginate'))
items.add_url_rule('/<int:item_id>/', view_func=DetailView.as_view('detail'))

# login required urls
add_view = login_required(AddView.as_view('add'))
# add_view = AddView.as_view('add')
items.add_url_rule('/add/', view_func=add_view)

from flask import (Blueprint, request, render_template, flash,
                   Response, stream_with_context, abort)
from werkzeug import secure_filename
from flask.views import MethodView
from users.models import User
from models import Item, Titles
from flask.ext.login import login_required, current_user
from forms import AddItemForm
from utils import allowed_thumbnails, allowed_file
from mongoengine.fields import GridFSProxy

items = Blueprint('items', __name__)


class ListView(MethodView):

    def get(self):
        items = Item.objects.all()
        return render_template('items/items_list.html', items=items)


class DetailView(MethodView):

    def get(self, item_id):
        return "hi from " + str(item_id)
        item = Item.objects.get_or_404(item_id=item_id)
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

        else:
            flash('upload unsuccessful', 'error')
            return render_template('items/add_item.html', form=form)

        uploaded_files = request.files.getlist("files")
        thumbnail = request.files['thumbnail']

        thumbnail_name = secure_filename(thumbnail.filename)

        if thumbnail and allowed_thumbnails(thumbnail_name):
            ext = thumbnail.mimetype.split('/')[-1]
            # use the 'thumbnail' name for all thumbnails
            filename = '.'.join(["thumbnail", ext])
            item.thumbnail.put(thumbnail.stream,
                               content_type=thumbnail.mimetype,
                               filename=filename)

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
    item = Item.objects.get(item_id=item_id)
    if filename == item.thumbnail.filename:
        return Response(stream_with_context(item.thumbnail.read()),
                        mimetype=item.thumbnail.content_type)

    return abort(404)


@items.route('/uploads/<int:item_id>/<filename>')
def serve_file(item_id, filename):
    item = Item.objects.get(item_id=item_id)
    for file in item.files:
        if file.filename == filename:
            return Response(stream_with_context(file.read()),
                            mimetype=file.content_type)
    return abort(404)

# Register the urls
items.add_url_rule('/items/', view_func=ListView.as_view('index'))
items.add_url_rule('/<int:item_id>/', view_func=DetailView.as_view('detail'))

# login required urls
add_view = login_required(AddView.as_view('add'))
# add_view = AddView.as_view('add')
items.add_url_rule('/add/', view_func=add_view)

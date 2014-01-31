from flask import (Blueprint, request, render_template, flash,
                   send_from_directory, current_app as app)
from werkzeug import secure_filename
from flask.views import MethodView
from users.models import User
from models import Item, Meta
from flask.ext.login import login_required, current_user
from forms import AddItemForm
from utils import allowed_file, make_dir
import os

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
            ar_meta = Meta()
            fr_meta = Meta()
            en_meta = Meta()

            ar_meta.title = form.ar_title.data.strip()
            ar_meta.short_description = form.ar_short_description.data
            ar_meta.lang = 'ar'

            fr_meta.title = form.fr_title.data.strip()
            fr_meta.short_description = form.fr_short_description.data
            fr_meta.lang = 'fr'

            en_meta.title = form.en_title.data.strip()
            en_meta.short_description = form.en_short_description.data
            en_meta.lang = 'en'

            item.meta_info.append(ar_meta)
            item.meta_info.append(fr_meta)
            item.meta_info.append(en_meta)

            item.description = form.description.data

            item.submitter = User.objects.get(id=current_user.id)

        else:
            flash('upload unsuccesful', 'error')
            return render_template('items/add_item.html', form=form)

        uploaded_files = request.files.getlist("files")
        thumbnail = request.files['thumbnail']
        thumbnail_name = secure_filename(thumbnail.filename)

        path = os.path.join(app.config['UPLOAD_FOLDER'], str(item.item_id))
        make_dir(path)

        if thumbnail and allowed_file(thumbnail.filename):
            thumbnail.save(os.path.join(path, thumbnail_name))

        filenames = []
        for file in uploaded_files:
            # Check if the file is one of the allowed types/extensions
            if file and allowed_file(file.filename):
                # Make the filename safe, remove unsupported chars
                filename = secure_filename(file.filename)
                # Move the file form the temporal folder to the upload
                # folder we setup
                file.save(os.path.join(path, filename))
                # Save the filename into a list, we'll use it later
                # filenames.append(filename)
                item.item_data.append(filename)
                # Redirect the user to the uploaded_file route, which
                # will basicaly show on the browser the uploaded file
        # Load an html page with a link to each uploaded file
        # item.item_data.append(filenames)
        item.save()
        flash('upload succesful')
        return render_template('items/add_item.html', form=form)


@items.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Register the urls
items.add_url_rule('/items/', view_func=ListView.as_view('index'))
items.add_url_rule('/<int:item_id>/', view_func=DetailView.as_view('detail'))

# login required urls
add_view = login_required(AddView.as_view('add'))
# add_view = AddView.as_view('add')
items.add_url_rule('/add/', view_func=add_view)

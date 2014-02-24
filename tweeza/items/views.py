from flask import (Blueprint, request, render_template, flash,
                   Response, stream_with_context, abort, send_file,
                   current_app as app, redirect, url_for, g)
from werkzeug import secure_filename
from flask.views import MethodView
from users.models import User
from models import Item, Title, Category, License
from flask.ext.login import login_required, current_user
from forms import AddItemForm, EditGithubItemForm, EditItemForm
from utils import allowed_thumbnails, allowed_file, make_dir
from mongoengine.fields import GridFSProxy
from extensions import cache
import requests
import os
import tempfile

items = Blueprint('items', __name__)


class ListView(MethodView):
    decorators = [cache.cached(60)]

    def get(self, page=1):
        items = Item.objects.paginate(page=page, per_page=12)
        categories = Category.objects.all()
        return render_template('items/items_list.html',
                               items=items, categories=categories)


class DetailView(MethodView):
    decorators = [cache.cached(60)]

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
                       % (user, repo_name)
            clone_string = 'git clone https://github.com/%s/%s.git' \
                           % (user, repo_name)
            return render_template('items/item_details.html', item=item,
                                   content=description.text,
                                   zip_link=zip_link,
                                   clone_string=clone_string)
        return render_template('items/item_details.html', item=item)


class AddView(MethodView):

    def get(self):
        form = AddItemForm()

        categories = Category.objects.all()
        licenses = License.objects.all()
        form.set_categories(categories, g.lang)
        form.set_licenses(licenses)
        return render_template('items/add_item.html', form=form)

    def post(self):

        form = AddItemForm()
        item = Item()

        categories = Category.objects.all()
        licenses = License.objects.all()
        form.set_categories(categories, g.lang)
        form.set_licenses(licenses)

        if form.validate_on_submit():
            # first, the user has to share something !
            if not form.github.data and not form.files.data:
                flash('Neither a repo URL nor files has been shared, come on!',
                      category='alert')
                return render_template('items/add_item.html', form=form)

            # give that something at least one title
            if not form.ar_title.data and not form.fr_title.data and \
               not form.en_title.data:

                flash('You need to give this item at least one title, \
                       just pick one language and name it!',
                      category='alert')
                return render_template('items/add_item.html', form=form)

            # now we can proceed
            ar_title = Title()
            fr_title = Title()
            en_title = Title()

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
            item.tags = form.tags.data.strip().split(',')
            item.category = form.category.data

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
                item.license = form.license.data

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
        flash('Item uploaded successfully', category='success')
        return render_template('items/add_item.html', form=form)


class EditView(MethodView):

    def get(self, item_id):
        item = Item.objects.get_or_404(item_id=item_id)
        # only admins or the item submitter can edit the item
        if item.submitter.id != current_user.id:
            if not current_user.is_admin:
                abort(403)

        form = None
        if item.github:
            form = EditGithubItemForm()
        else:
            form = EditItemForm()
            form.description.default = item.description

            licenses = License.objects.all()
            form.set_licenses(licenses)
            form.license.default = str(item.license.license_id)

        categories = Category.objects.all()
        form.set_categories(categories, g.lang)
        form.category.default = str(item.category.category_id)
        form.process()

        return render_template('items/edit_item.html', form=form, item=item)

    def post(self, item_id):
        item = Item.objects.get_or_404(item_id=item_id)

        # only admins or the item submitter can edit the item
        if item.submitter.id != current_user.id:
            if not current_user.is_admin:
                abort(403)

        form = None
        if item.github:
            form = EditGithubItemForm()
        else:
            form = EditItemForm()
            licenses = License.objects.all()
            form.set_licenses(licenses)

        categories = Category.objects.all()
        form.set_categories(categories, g.lang)

        if form.validate_on_submit():
            for title in item.titles:  # ugly, I'll make it shorter, later...
                if title.lang == 'ar':
                    title.title = form.ar_title.data.strip()
                elif title.lang == 'en':
                    title.title = form.en_title.data.strip()
                else:
                    title.title = form.fr_title.data.strip()

            item.tags = form.tags.data.strip().split(',')
            item.category = Category.objects.get(category_id=
                                                 int(form.category.data))

            if form.thumbnail.data:  # if the user has uploaded new thumbnail
                # remove the old one
                item.thumbnail.delete()
                # replace it with the new one
                thumbnail = request.files['thumbnail']
                thumbnail_name = secure_filename(thumbnail.filename)

                if thumbnail and allowed_thumbnails(thumbnail_name):
                    ext = thumbnail.mimetype.split('/')[-1]
                    # use the 'thumbnail' name for all thumbnails
                    filename = '.'.join(["thumbnail", ext])
                    item.thumbnail.put(thumbnail.stream,
                                       content_type=thumbnail.mimetype,
                                       filename=filename)

            if form.blog_post.data.strip():
                item.blog_post = form.blog_post.data
            if not item.github:
                item.description = form.description.data
                item.license = License.objects.get(license_id=
                                                   int(form.license.data))
            else:
                item.github = form.github.data
                item.save()
                # no need to process any uploaded files
                flash('Item updated successfully', category='success')
                return render_template('items/edit_item.html', form=form,
                                       item=item)

        else:
            flash("Couldn't update item", category='error')
            return render_template('items/edit_item.html', form=form,
                                   item=item)

        if form.files.data:  # if the user is uploading new files
            # delete old files first
            for file in item.files:
                file.delete()

            # now, replace them with the new ones
            uploaded_files = request.files.getlist("files")
            new_files = []
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
                    new_files.append(file_)
            item.files = new_files
        # Save the thing
        item.save()
        flash('Item updated successfully', category='success')
        return render_template('items/edit_item.html', form=form,
                               item=item)


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


@items.route('/item/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_item(item_id):

    item = Item.objects.get_or_404(item_id=item_id)

    if item.submitter.id != current_user.id:
        if not current_user.is_admin:
            abort(403)

    # delete physical files
    item.thumbnail.delete()
    for file in item.files:
        file.delete()

    # delete the item itself (the document)
    item.delete()
    flash('Item deleted successfully', category='success')
    return redirect(url_for('frontend.index'))


# Register the urls
items.add_url_rule('/items/', view_func=ListView.as_view('index'))
items.add_url_rule('/items/<int:page>/',
                   view_func=ListView.as_view('paginate'))
items.add_url_rule('/item/<int:item_id>/',
                   view_func=DetailView.as_view('detail'))

# login required urls
add_view = login_required(AddView.as_view('add'))
# add_view = AddView.as_view('add')
items.add_url_rule('/add/', view_func=add_view)

# Edit item
edit_view = login_required(EditView.as_view('edit'))
items.add_url_rule('/item/<int:item_id>/edit/', view_func=edit_view)

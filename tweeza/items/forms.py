# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField
from wtforms.fields.html5 import URLField
from flask.ext.babel import lazy_gettext as _
from flask_wtf.file import FileField


class AddItemForm(Form):

    github = URLField(_('Remote repository URL'))

    blog_post = URLField(_('Blog post URL'))

    ar_title = TextField(_('Item title in Arabic'))
    en_title = TextField(_('Item title in English'))
    fr_title = TextField(_('Item title in French'))

    description = TextAreaField(_('Description'))
    thumbnail = FileField(_('Thumbnail (minimum dimensions 230x230)'))

    files = FileField(_('Thumbnail (minimum dimensions 230x230)'))

    tags = TextField(_('Tags'))

    submit = SubmitField(_('Add item'))

# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import (ValidationError, BooleanField, TextField,
                     TextAreaField, SubmitField)
from wtforms.validators import Required, url
from wtforms.fields.html5 import URLField
from flask.ext.babel import lazy_gettext as _
from flask_wtf.file import FileField


class AddItemForm(Form):

    vcs_url = URLField(_('Remote repository URL')) # , validators=[url()])

    ar_title = TextField(_('Item title in Arabic'))
    en_title = TextField(_('Item title in English'))
    fr_title = TextField(_('Item title in French'))

    ar_short_description = TextAreaField(_('Short description in Arabic'))
    en_short_description = TextAreaField(_('Short description in English'))
    fr_short_description = TextAreaField(_('Short description in French'))

    description = TextAreaField(_('Long description'))
    thumbnail = FileField(_('Thumbnail (minimum dimensions 230x230)'),
                          validators=[Required()])

    files = FileField(_('Thumbnail (minimum dimensions 230x230)'),
                      validators=[Required()])

    tags = TextField(_('Tags'))
    
    submit = SubmitField(_('Add item'))

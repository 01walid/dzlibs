# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, SelectField
from wtforms.fields.html5 import URLField
from flask.ext.babel import lazy_gettext as _
from flask_wtf.file import FileField


class BaseForm(Form):
    """
    this contains shared fields among other forms
    """

    blog_post = URLField(_('Blog post URL'))

    ar_title = TextField(_('Item title in Arabic'))
    en_title = TextField(_('Item title in English'))
    fr_title = TextField(_('Item title in French'))

    thumbnail = FileField(_('Thumbnail (minimum dimensions 230x230)'))

    tags = TextField(_('Tags'))

    category = SelectField(_('Category'), choices=[], coerce=int)

    def set_categories(self, categories, lang):
        choices = []
        for category in categories:
            choices.append((category.id, category.get_name(lang)))

        self.category.choices = choices


class AddItemForm(BaseForm):

    github = URLField(_('Remote repository URL'))
    description = TextAreaField(_('Description'))

    files = FileField(_('Files'))

    license = SelectField(_('License'), choices=[], coerce=int)

    submit = SubmitField(_('Add item'))

    def set_licenses(self, licenses):
        choices = []
        for license in licenses:
            choices.append((license.id, license.name))

        self.license.choices = choices


class EditGithubItemForm(BaseForm):

    github = URLField(_('Remote repository URL'))

    submit = SubmitField(_('Update'))


class EditItemForm(BaseForm):

    files = FileField(_('Files'))

    description = TextAreaField(_('Description'))

    license = SelectField(_('License'), choices=[], coerce=int)

    submit = SubmitField(_('Update'))

    def set_licenses(self, licenses):
        choices = []
        for license in licenses:
            choices.append((license.id, license.name))

        self.license.choices = choices

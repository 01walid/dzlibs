# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, SelectField
from wtforms.validators import Required
from flask.ext.wtf.html5 import URLField, EmailField
from flask.ext.babel import lazy_gettext as _


class EditProfileForm(Form):

    name = TextField(_('Full name'), validators=[Required()])

    twitter = TextField(_('Twitter'))
    facebook = TextField(_('Facebook'))

    website = URLField(_('Website or blog'))

    email = EmailField(_('Email'))

    location = TextField(_('Location'))

    hireable = SelectField(_('Hireable'),
                           choices=[(0, _("No")), (1, _('Yes'))],
                           coerce=int,
                           description=_("Are you free to hire ?"))

    bio = TextAreaField(_('Bio'))

    submit = SubmitField(_('Update profile'))

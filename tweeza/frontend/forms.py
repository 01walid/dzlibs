# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import Required, Email
from flask.ext.wtf.html5 import EmailField
from flask.ext.babel import lazy_gettext as _


class ContactForm(Form):

    name = TextField(_('Name'), Required())

    subject = TextField(_('Subject'), Required())

    email = EmailField(_('Email'),
                       [Required(), Email()],
                       description=u"What's your email address?")

    message = TextAreaField(_('Message'))

    submit = SubmitField(u'Send')

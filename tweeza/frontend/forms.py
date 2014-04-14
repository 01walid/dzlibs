# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import Required
from flask.ext.wtf.html5 import EmailField
from flask.ext.babel import lazy_gettext as _


class ContactForm(Form):

    name = TextField(_('Name'), validators=[Required()])

    subject = TextField(_('Subject'), validators=[Required()])

    email = EmailField(_('Email'), validators=[Required()],
                       description=u"What's your email address?")

    message = TextAreaField(_('Message'), validators=[Required()])

    recaptcha = RecaptchaField()

    submit = SubmitField(u'Send')

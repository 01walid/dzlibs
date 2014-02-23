# -*- coding: utf-8 -*-

from flask import Markup

from flask.ext.wtf import Form
from wtforms import (ValidationError, HiddenField, BooleanField, TextField,
                     PasswordField, SubmitField)
from wtforms.validators import Required, Length, EqualTo, Email
from flask.ext.wtf.html5 import EmailField

from users.models import User
from utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX,
                   USERNAME_LEN_MIN, USERNAME_LEN_MAX)


class LoginForm(Form):
    next = HiddenField()
    email = TextField(u'email', [Required()])
    password = PasswordField('Password',
                             [Required(), Length(PASSWORD_LEN_MIN,
                                                 PASSWORD_LEN_MAX)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class SignupForm(Form):
    next = HiddenField()
    email = EmailField(u'Email', [Required(), Email()],
                       description=u"What's your email address?")
    password = PasswordField(u'Password',
                             [Required(),
                              Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
                             description=u'%s characters or more! Be tricky.'
                             % PASSWORD_LEN_MIN)
    name = TextField(u'Choose your username',
                     [Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
                     description=u"Don't worry. you can change it later.")

    agreeMessage = u'Agree to the'
    TOSlink = '<a target="blank" href="/terms">Terms of Service</a>'

    agree = BooleanField(agreeMessage + ' ' + Markup(TOSlink), [])
    submit = SubmitField('Sign up')

    def validate_email(self, field):
        try:
            user = User.objects.get(email=field.data.strip())
        except User.DoesNotExist:
            user = None
        if user is not None:
            raise ValidationError(u'This email is taken')


class RecoverPasswordForm(Form):
    email = EmailField(u'Your email', [Email()])
    submit = SubmitField('Send instructions')


class ChangePasswordForm(Form):
    activation_key = HiddenField()
    password = PasswordField(u'Password', [Required()])
    password_again = PasswordField(u'Password again',
                                   [EqualTo('password',
                                            message="Passwords don't match")])
    submit = SubmitField('Save')


class ReauthForm(Form):
    next = HiddenField()
    password = PasswordField(u'Password',
                             [Required(),
                              Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    submit = SubmitField('Reauthenticate')


class CreateProfileForm(Form):

    email = EmailField(u'Email',
                       [Required(), Email()],
                       description=u"What's your email address?")

    password = PasswordField(u'Password',
                             [Required(),
                              Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
                             description=u'%s characters or more! Be tricky.' %
                             PASSWORD_LEN_MIN)

    submit = SubmitField(u'Create Profile')

    def validate_email(self, field):
        try:
            user = User.objects.get(email=field.data.strip())
        except User.DoesNotExist:
            user = None
        if user is not None:
            raise ValidationError(u'This email is taken')

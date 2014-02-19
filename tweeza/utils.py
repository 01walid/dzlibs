# -*- coding: utf-8 -*-
"""
    Utils has nothing to do with models and views.
"""

import string
import random
import os

from datetime import datetime

ALLOWED_THUMBNAILS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip',
                          'doc', 'docx', 'php', 'gzip', 'rar', 'java',
                          'python'])
# Form validation

USERNAME_LEN_MIN = 4
USERNAME_LEN_MAX = 25

REALNAME_LEN_MIN = 4
REALNAME_LEN_MAX = 25

PASSWORD_LEN_MIN = 6
PASSWORD_LEN_MAX = 16

AGE_MIN = 1
AGE_MAX = 300

DEPOSIT_MIN = 0.00
DEPOSIT_MAX = 9999999999.99

# Sex type.
MALE = 1
FEMALE = 2
OTHER = 9
SEX_TYPE = {
    MALE: u'Male',
    FEMALE: u'Female',
    OTHER: u'Other',
}

# Model
STRING_LEN = 64


def get_current_time():
    return datetime.utcnow()


def current_year():
    from datetime import date
    return date.today().year


def allowed_thumbnails(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_THUMBNAILS


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def id_generator(size=10, chars=string.ascii_letters + string.digits):
    #return base64.urlsafe_b64encode(os.urandom(size))
    return ''.join(random.choice(chars) for x in range(size))


def make_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception as e:
        raise e

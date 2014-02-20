from extensions import db
from users.models import User
import datetime


class Titles(db.EmbeddedDocument):

    title = db.StringField()
    lang = db.StringField(max_length=3)


class Category(db.Document):

    created_at = db.DateTimeField(default=datetime.datetime.now,
                                  required=True)
    name_ar = db.StringField(max_length=50)
    name_fr = db.StringField(max_length=50)
    name_en = db.StringField(max_length=50)
    description = db.StringField()


class Item(db.Document):

    item_id = db.SequenceField(primary_key=True)

    submitted_at = db.DateTimeField(default=datetime.datetime.now,
                                    required=True)

    titles = db.ListField(db.EmbeddedDocumentField(Titles),
                          required=True)

    submitter = db.ReferenceField(User)

    category = db.ReferenceField(Category)

    files = db.ListField(db.FileField())

    github = db.URLField()

    blog_post = db.URLField()

    tags = db.ListField(db.StringField(max_length=30))

    description = db.StringField()

    thumbnail = db.ImageField(thumbnail_size=(230, 230, True))

    license_name = db.StringField(max_length=50)

    meta = {
        'indexes': ['-submitted_at', 'tags'],
        'ordering': ['-submitted_at']
    }

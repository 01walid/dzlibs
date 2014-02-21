from extensions import db
from users.models import User
import datetime


class Title(db.EmbeddedDocument):

    title = db.StringField()
    lang = db.StringField(max_length=3)


class Category(db.DynamicDocument):
    """
    Why dynamic document ?
    So we can add other languages fields dynamically (e.g. Tamazight language)
    and add the new translation to all existing categories, see:

    docs.mongoengine.org/guide/defining-documents.html#dynamic-document-schemas

    """

    created_at = db.DateTimeField(default=datetime.datetime.now,
                                  required=True)

    category_id = db.SequenceField(primary_key=True)

    # you can add your name_[lang] at runtime with no worries,
    # it's a Dynamic Document!
    name_ar = db.StringField(max_length=50)
    name_fr = db.StringField(max_length=50)
    name_en = db.StringField(max_length=50)

    description = db.StringField()


class Item(db.Document):

    item_id = db.SequenceField(primary_key=True)

    submitted_at = db.DateTimeField(default=datetime.datetime.now,
                                    required=True)

    titles = db.ListField(db.EmbeddedDocumentField(Title),
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

    has_api = db.BooleanField()
    api_url = db.URLField()

    def get_thumbnail(self):
        from flask import url_for
        if self.thumbnail:
            return url_for('items.serve_thumbnail',
                           item_id=self.item_id,
                           filename=self.thumbnail.filename)

        return url_for('static',
                       filename='images/no-thumbnail.png')

    def get_title(self, lang):
        for title in self.titles:
            if title.lang == lang:
                return title.title

        return ''

    meta = {
        'indexes': ['-submitted_at', 'tags'],
        'ordering': ['-submitted_at']
    }

from datetime import datetime
from mongoengine import connect, fields, Document, ReferenceField
from config import app_config
from flask_login import UserMixin, current_user
from flask import session
from werkzeug.security import generate_password_hash


connect(app_config.MONGODB_NAME, host=app_config.MONGODB_HOST, port=app_config.MONGODB_PORT)


class User(Document, UserMixin):
    user_group = {
        'admin': 'admin',
        'staff': 'staff'
        }

    name = fields.StringField()
    password = fields.StringField()
    group = fields.StringField(required=True, choices=user_group.keys())

    @classmethod
    def add_user(cls, name, password, user_group='staff'):
        obj = cls()
        obj.name = name
        obj.password = generate_password_hash(password)
        obj.group = user_group
        obj.save()
        return obj

    @classmethod
    def check_admin_rights(cls):
        if current_user.group == 'admin':
            return True
        return False


class Blog(Document):
    name = fields.StringField()
    posted_user = ReferenceField(User)
    content = fields.StringField()
    created_date = fields.DateTimeField(default=datetime.now())
    updated_date = fields.DateTimeField()

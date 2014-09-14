import datetime
from mongoengine import StringField
from mongoengine import DateTimeField


class BaseEntity(object):
    id = StringField(max_length=255, required=True)
    created = DateTimeField(default=datetime.datetime.now, required=True)
    timestamp = DateTimeField(default=datetime.datetime.now, required=True)
    meta = {'allow_inheritance': True}
from base_entity import BaseEntity
from mongoengine import Document
from mongoengine import StringField


class User(Document, BaseEntity):
    name = StringField(max_length=255, required=True, default='Entity_Name')
    password = StringField(max_length=128,required=True, default='pass')
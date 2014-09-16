from base_entity import BaseEntity
from mongoengine import Document
from mongoengine import StringField


class Group(Document, BaseEntity):

    name = StringField(max_length=255, required=True, default='Entity_Name')
    description = StringField(max_length=255, required=False)
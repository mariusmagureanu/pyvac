__author__ = 'mariusmagureanu'
from mongoengine import Document, StringField
from base_entity import BaseEntity


class Snippet(Document, BaseEntity):
    content = StringField(max_length=255, required=True)
    comment = StringField(max_length=255, required=False)
__author__ = 'mariusmagureanu'
from mongoengine import Document, StringField
from base_entity import BaseEntity


class Ban(Document, BaseEntity):
    expression = StringField(max_length=255, required=True)
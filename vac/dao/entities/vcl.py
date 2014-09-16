__author__ = 'mariusmagureanu'
from mongoengine import Document, StringField
from base_entity import BaseEntity


class Vcl(Document, BaseEntity):
    description = StringField(max_length=255, required=False)
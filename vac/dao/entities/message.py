from base_entity import BaseEntity
from mongoengine import Document
from mongoengine import StringField
from mongoengine import IntField


class Message(Document, BaseEntity):
    title = StringField(max_length=255, required=True)
    message = StringField(max_length=512, required=True)
    internal_message = StringField(max_length=255, required=True)
    severity = IntField(required=True)

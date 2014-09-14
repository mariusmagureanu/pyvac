from base_entity import BaseEntity
from mongoengine import Document
from mongoengine import StringField


class Node(Document, BaseEntity):
    name = StringField(max_length=255, required=True)
    description = StringField(max_length=255, required=False)
    agent_host = StringField(max_length=128, required=True)
    agent_username = StringField(max_length=255, required=True)
    agent_password = StringField(max_length=64, required=True)
    dash_n = StringField(max_length=64, required=False)
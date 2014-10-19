__author__ = 'mariusmagureanu'

import datetime
from mongoengine import StringField, \
    Document, DateTimeField, ListField, \
    ReferenceField, IntField


class BaseEntity(object):
    id = StringField(max_length=255, required=True)
    created = DateTimeField(default=datetime.datetime.now, required=True)
    timestamp = DateTimeField(default=datetime.datetime.now, required=True)
    meta = {'allow_inheritance': True}


class Ban(Document, BaseEntity):
    expression = StringField(max_length=255, required=True)


class Group(Document, BaseEntity):
    name = StringField(max_length=255, required=True, default='Entity_Name', unique=True)
    description = StringField(max_length=255, required=False)
    caches = ListField(ReferenceField('Node'))


class Message(Document, BaseEntity):
    title = StringField(max_length=255, required=True)
    message = StringField(max_length=512, required=True)
    internal_message = StringField(max_length=255, required=True)
    severity = IntField(required=True)


class Node(Document, BaseEntity):
    name = StringField(max_length=255, required=True, default='Entity_Name', unique=True)
    description = StringField(max_length=255, required=False)
    agent_host = IntField(required=True)
    agent_username = StringField(max_length=255, required=True)
    agent_password = StringField(max_length=64, required=True)
    dash_n = StringField(max_length=64, required=False)
    group = ReferenceField(Group)


class Snippet(Document, BaseEntity):
    content = StringField(max_length=255, required=True)
    comment = StringField(max_length=255, required=False)


class User(Document, BaseEntity):
    name = StringField(max_length=255, required=True, default='Entity_Name')
    password = StringField(max_length=128, required=True, default='pass')


class Vcl(Document, BaseEntity):
    name = StringField(required=True, max_length=48, default='boot')
    description = StringField(required=False)

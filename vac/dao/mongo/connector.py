__author__ = 'mariusmagureanu'
from mongoengine import connect


def connect_to_mongo():
    connect('vacpi')

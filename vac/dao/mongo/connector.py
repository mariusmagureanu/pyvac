__author__ = 'mariusmagureanu'
from mongoengine import connect
from mongoengine.connection import disconnect

connected = False
test_connected = False


def connect_to_mongo():
    global connected
    if not connected:
        connect('vacpi')
        connected = True


def connect_to_mongo_test():
    global test_connected
    if not test_connected:
        print('connected...')
        connect('vacpi_test')
        test_connected = True


def disconnect_mongo():
    disconnect()

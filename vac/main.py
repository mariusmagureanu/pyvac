__author__ = 'mariusmagureanu'
from dao.mongo.connector import connect_to_mongo
from dao.entities.user import User
from dao.facade.user_facade import UserFacade
from test.dao.base_test import BaseDaoTest
from web.base_resource import run_flask
import unittest


def test_mongo():
    connect_to_mongo()
    u = User()
    uff = UserFacade(u, User)

    u.drop_collection()
    uff.save()

    print uff.get_by_name('Rambo')
    print uff.is_valid('Rambo', 'pass')
    uff.change_password('Rambo', 'passs')
    print uff.is_valid('Rambo', 'passs')


if __name__ == '__main__':
    #run_flask()
    connect_to_mongo()
    unittest.main()
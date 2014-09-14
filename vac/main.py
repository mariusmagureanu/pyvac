__author__ = 'mariusmagureanu'
from dao.mongo.connector import connect_to_mongo
from dao.entities.user import User
from dao.facade.user_facade import UserFacade
from web.base_resource import run_flask


def test_mongo():
    connect_to_mongo()
    u = User()
    uf = UserFacade()
    u.drop_collection()
    u.save()
    print uf.get_by_name('Rambo')
    print uf.is_valid('Rambo', 'pass')
    uf.change_password('Rambo', 'passs')
    print uf.is_valid('Rambo', 'passs')


if __name__ == '__main__':
    run_flask()
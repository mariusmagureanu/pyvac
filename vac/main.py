__author__ = 'mariusmagureanu'
from vac.dao.mongo.connector import connect_to_mongo
from vac.dao.entities.model import User
from vac.dao.facade.user_facade import UserFacade


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
    pass

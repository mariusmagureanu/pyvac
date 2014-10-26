__author__ = 'mariusmagureanu'
from .base_test import BaseDaoTest
from vac.dao.facade.user_facade import UserFacade
from vac.dao.entities.model import User


class UserDaoTest(BaseDaoTest):

    __test__ = True

    def setUp(self):
        super(self.__class__, self).setUp()
        super(self.__class__, self)._set_model(User(), UserFacade())

    def tearDown(self):
        super(self.__class__, self).tearDown()

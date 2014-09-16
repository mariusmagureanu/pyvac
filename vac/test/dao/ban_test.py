__author__ = 'mariusmagureanu'
from base_test import BaseDaoTest
from vac.dao.entities.ban import Ban
from vac.dao.facade.ban_facade import BanFacade


class BanDaoTest(BaseDaoTest):

    __test__ = True

    def setUp(self):
        super(self.__class__, self).setUp()
        super(self.__class__, self)._set_model(Ban(expression="Some funky expression"), BanFacade())

    def tearDown(self):
        super(self.__class__, self).tearDown()
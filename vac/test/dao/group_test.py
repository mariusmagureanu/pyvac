__author__ = 'mariusmagureanu'
from .base_test import BaseDaoTest
from vac.dao.facade.group_facade import GroupFacade
from vac.dao.entities.model import Group


class GroupDaoTest(BaseDaoTest):

    __test__ = True

    def setUp(self):
        super(self.__class__, self).setUp()
        super(self.__class__, self)._set_model(Group(), GroupFacade())

    def tearDown(self):
        super(self.__class__, self).tearDown()

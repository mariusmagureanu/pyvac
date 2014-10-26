__author__ = 'mariusmagureanu'
from .base_test import BaseDaoTest
from vac.dao.entities.model import Vcl
from vac.dao.facade.vcl_facade import VclFacade


class VclDaoTest(BaseDaoTest):

    __test__ = True

    def setUp(self):
        super(self.__class__, self).setUp()
        super(self.__class__, self)._set_model(Vcl(), VclFacade())

    def tearDown(self):
        super(self.__class__, self).tearDown()

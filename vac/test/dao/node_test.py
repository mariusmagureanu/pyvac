__author__ = 'mariusmagureanu'
from .base_test import BaseDaoTest
from vac.dao.facade.node_facade import NodeFacade
from vac.dao.entities.model import Node


class NodeDaoTest(BaseDaoTest):

    __test__ = True

    def setUp(self):
        super(self.__class__, self).setUp()
        node = Node(description="N/A", agent_host="6085", agent_username="vac",
                    agent_password="vac", dash_n="N/A")
        super(self.__class__, self)._set_model(node, NodeFacade())

    def tearDown(self):
        super(self.__class__, self).tearDown()

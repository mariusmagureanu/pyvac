__author__ = 'mariusmagureanu'
from vac.dao.entities.node import Node
from base_facade import BaseFacade


class NodeFacade(BaseFacade):

    def __init__(self):
        """

        :return:
        """
        super(NodeFacade, self).__init__(Node)


__author__ = 'mariusmagureanu'
from vac.dao.entities.model import Node
from .base_facade import BaseFacade


class NodeFacade(BaseFacade):

    def __init__(self):
        """

        :return:
        """
        super(NodeFacade, self).__init__(Node)

    def remove(self, document):
        if document.group is not None:
            document.group.caches.remove(document)
            document.group.save()
        self.__model__.delete(document)

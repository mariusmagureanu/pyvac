__author__ = 'mariusmagureanu'
from vac.dao.entities.group import Group
from base_facade import BaseFacade


class GroupFacade(BaseFacade):

    def __init__(self):
        """

        :return:
        """
        super(GroupFacade, self).__init__(Group)
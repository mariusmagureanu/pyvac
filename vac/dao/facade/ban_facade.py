__author__ = 'mariusmagureanu'
from vac.dao.entities.model import Ban
from base_facade import BaseFacade


class BanFacade(BaseFacade):

    def __init__(self):
        """

        :return:
        """
        super(BanFacade, self).__init__(Ban)
__author__ = 'mariusmagureanu'
from base_facade import BaseFacade
from vac.dao.entities.model import Vcl


class VclFacade(BaseFacade):

    def __init__(self):
        """

        :return:
        """
        super(VclFacade, self).__init__(Vcl)
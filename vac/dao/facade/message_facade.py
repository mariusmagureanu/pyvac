__author__ = 'mariusmagureanu'
from vac.dao.entities.model import Message
from .base_facade import BaseFacade


class MessageFacade(BaseFacade):

    def __init__(self):
        """

        :return:
        """
        super(MessageFacade, self).__init__(Message)

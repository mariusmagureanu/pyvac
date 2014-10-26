__author__ = 'mariusmagureanu'
from .base_facade import BaseFacade
from vac.dao.entities.model import Snippet


class SnippetFacade(BaseFacade):

    def __init__(self):
        """

        :return:
        """
        super(SnippetFacade, self).__init__(Snippet)

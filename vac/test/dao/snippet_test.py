__author__ = 'mariusmagureanu'
from base_test import BaseDaoTest
from vac.dao.entities.snippet import Snippet
from vac.dao.facade.snippet_facade import SnippetFacade


class SnippetDaoTest(BaseDaoTest):

    __test__ = True

    def setUp(self):
        super(self.__class__, self).setUp()
        super(self.__class__, self)._set_model(Snippet(content="Some funky content"), SnippetFacade())

    def tearDown(self):
        super(self.__class__, self).tearDown()
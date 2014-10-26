__author__ = 'mariusmagureanu'
from .base_test import BaseDaoTest
from vac.dao.entities.model import Message
from vac.dao.facade.message_facade import MessageFacade


class MessageDaoTest(BaseDaoTest):

    __test__ = True

    def setUp(self):
        super(self.__class__, self).setUp()
        mess = Message(
            message='Something Something',
            internal_message='Some other thing',
            title='N/A',
            severity=1)
        super(self.__class__, self)._set_model(mess, MessageFacade())

    def tearDown(self):
        super(self.__class__, self).tearDown()

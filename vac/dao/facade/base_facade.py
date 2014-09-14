__author__ = 'mariusmagureanu'
from abc import abstractmethod


class BaseFacade(object):

    def __init__(self, doc):
        self.document = doc

    @abstractmethod
    def save(self):
        pass

    def do_stuff(self):
        pass

__author__ = 'mariusmagureanu'
from mongoengine import Document


class BaseFacade(object):

    def __init__(self, model):
        """

        :param model:
        :return:
        """
        assert (issubclass(model, Document))
        self.__model__ = model

    @staticmethod
    def save(document):
        """

        :param document:
        :return:
        """
        document.save()

    def remove(self, document):
        """

        :param document:
        :return:
        """
        self.__model__.delete(document)

    def find(self, object_id):
        """

        :param object_id:
        :return:
        """
        return  self.__model__.objects.get(id=object_id)

    def find_based_on_field(self, field_name, field_value):
        """

        :param field_name:
        :param field_value:
        :return:
        """
        return self.__model__(**{field_name: field_value})

    def find_one_based_on_field(self, field_name, field_value):
        """

        :param field_name:
        :param field_value:
        :return:
        """
        return self.__model__.objects.get(**{field_name: field_value})

    def count(self):
        """

        :return:
        """
        return len(self.__model__.objects)




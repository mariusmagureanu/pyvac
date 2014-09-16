__author__ = 'mariusmagureanu'
from vac.dao.entities.user import User
from base_facade import BaseFacade


class UserFacade(BaseFacade):

    def __init__(self):
        """

        :return:
        """
        super(UserFacade, self).__init__(User)

    def get_by_name(self, user_name):
        """

        :param user_name:
        :return:
        """
        return self.__model__.objects(name=user_name).to_json()

    def is_valid(self, user_name, password):
        """

        :param user_name:
        :param password:
        :return:
        """
        try:
            self.__model__.objects.get(name=user_name, password=password)
        except User.DoesNotExist:
            return False
        except User.MultipleObjectsReturned:
            return False
        return True

    def change_password(self, user_name, password):
        """

        :param user_name:
        :param password:
        :return:
        """
        self.__model__.objects(name=user_name).update_one(set__password=password)
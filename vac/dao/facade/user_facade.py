__author__ = 'mariusmagureanu'
from ..entities.user import User
from mongoengine import Document


class UserFacade(object):

    def get_by_name(self, user_name):
        return User.objects(name=user_name)

    def is_valid(self, user_name, password):
        try:

            User.objects.get(name=user_name, password=password)
        except User.DoesNotExist:
            return False
        except User.MultipleObjectsReturned:
            return False
        return True

    def change_password(self, user_name, password):
        User.objects(name=user_name).update_one(set__password=password)

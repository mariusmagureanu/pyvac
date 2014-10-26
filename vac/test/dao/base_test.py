__author__ = 'mariusmagureanu'
from unittest import TestCase
from vac.dao.mongo.connector import connect_to_mongo_test


class BaseDaoTest(TestCase):

    __test__ = False

    def __init__(self, *args, **kwargs):
        super(BaseDaoTest, self).__init__(*args, **kwargs)
        self._entity = None
        self._facade = None
        print(self.__class__.__name__)

    def _set_model(self, e, f):
        self._facade = f
        self._entity = e

    def setUp(self):
        connect_to_mongo_test()

    def tearDown(self):
        self._entity.drop_collection()

    def test_get_all(self):
        self.assertTrue(True)

    def test_save_entity(self):
        self._facade.save(self._entity)
        self.assertIsNotNone(
            self._facade.find_one_based_on_field(
                'id',
                self._entity.id))

    def test_count(self):
        self._facade.save(self._entity)
        self.assertEqual(1, self._facade.count())

    def test_remove_entity(self):
        self._facade.save(self._entity)
        self.assertEqual(1, self._facade.count())
        self._facade.remove(self._entity)
        self.assertEqual(0, self._facade.count())

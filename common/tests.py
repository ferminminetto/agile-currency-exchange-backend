from django.test import TestCase
from common.BaseModel import BaseModel


class BaseModelTests(TestCase):

    def test_delete_method(self):
        new_model = BaseModel()
        self.assertIs(new_model.deleted, False)
        new_model.delete()
        self.assertIs(new_model.pldeleted, True)

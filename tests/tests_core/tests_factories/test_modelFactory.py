import unittest

from vfxDatabaseORM.core import models
from vfxDatabaseORM.core.interfaces import IManager
from vfxDatabaseORM.core.factories import ModelFactory


class FakeManager(IManager):
    def get(self, uid):
        return None

    def all(self):
        return []

    def filters(self, **kwargs):
        return []

    def create(self, data):
        return True

    def update(self, uid, new_data):
        return True

    def delete(self):
        return True


class ExampleModel(models.Model):
    manager_class = FakeManager

    name = models.StringField("name")
    is_valid = models.BooleanField("foo_is_valid", default=False)


class TestModelFactory(unittest.TestCase):
    def test_CASE_build_WITH_valid_data_SHOULD_return_instance(self):
        raw_values = {"id": 50, "name": "foo", "foo_is_valid": True}

        instance = ModelFactory.build(ExampleModel, raw_values)

        print(instance.uid)

        self.assertIsInstance(instance, ExampleModel)
        self.assertEqual(instance.uid, 50)
        self.assertEqual(instance.name, "foo")
        self.assertEqual(instance.is_valid, True)

    def test_CASE_build_WITH_incomplete_valid_data_SHOULD_return_instance(
        self,
    ):
        raw_values = {"name": "foo"}

        instance = ModelFactory.build(ExampleModel, raw_values)

        self.assertIsInstance(instance, ExampleModel)
        self.assertEqual(
            instance.uid, 0
        )  # default value defined in model.Model
        self.assertEqual(instance.name, "foo")
        self.assertEqual(instance.is_valid, False)  # defined in the field

    def test_CASE_build_WITH_incomplete_valid_data_SHOULD_return_instance(
        self,
    ):
        raw_values = {"name": "foo"}

        instance = ModelFactory.build(ExampleModel, raw_values)

        self.assertIsInstance(instance, ExampleModel)
        self.assertEqual(
            instance.uid, 0
        )  # default value defined in model.Model
        self.assertEqual(instance.name, "foo")
        self.assertEqual(instance.is_valid, False)  # defined in the field

    def test_CASE_build_WITH_no_data_SHOULD_return_instance(self):
        raw_values = {}

        instance = ModelFactory.build(ExampleModel, raw_values)

        self.assertIsInstance(instance, ExampleModel)
        self.assertEqual(
            instance.uid, 0
        )  # default value defined in model.Model
        self.assertEqual(
            instance.name, None
        )  # default value defined in the field
        self.assertEqual(instance.is_valid, False)  # defined in the field

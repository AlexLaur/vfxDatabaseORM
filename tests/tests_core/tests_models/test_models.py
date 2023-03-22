import unittest

from vfxDatabaseORM.core import models, exceptions
from vfxDatabaseORM.core.interfaces import IManager

class FakeManager(IManager):

    def get(self, uid):
        return self.model_class(uid=1)

    def all(self):
        return [self.model_class(uid=i) for i in range(2)]

    def filters(self, **kwargs):
        return [self.model_class(uid=i) for i in range(2)]

    def create(self, data):
        return True

    def update(self, uid, new_data):
        return True

    def delete(self):
        return True


class FakeModelA(models.Model):
    manager_class = FakeManager

class FakeModelB(models.Model):
    entity_name = "FakeModel"
    manager_class = FakeManager

    related_field = models.OneToOneField("related_b", to="FakeModelA", related_db_name="retaled_a")


class TestModel(unittest.TestCase):

    def test_CASE_model_without_manager_SHOULD_raise(self):

        with self.assertRaises(exceptions.ManagerNotDefined):

            class BadModelWithNoManager(models.Model):
                pass

    def test_CASE_get_fields_SHOULD_return_fields(self):

        result = FakeModelA.get_fields()
        self.assertEqual(result, FakeModelA._meta.fields)

    def test_CASE_get_related_fields_SHOULD_return_fields(self):

        result = FakeModelA.get_related_fields()
        self.assertEqual(result, FakeModelA._meta.related_fields)

    def test_CASE_get_related_fields_SHOULD_return_fields(self):

        result = FakeModelA.get_related_fields()
        self.assertEqual(result, FakeModelA._meta.related_fields)

    def test_CASE_get_field_by_name_WITH_valid_field_SHOULD_return_field(self):

        result = FakeModelA.get_field("uid")
        self.assertEqual(result, FakeModelA._meta.fields[0])

    def test_CASE_get_field_by_name_WITH_valid_related_field_SHOULD_return_field(self):

        result = FakeModelB.get_field("related_field")
        self.assertEqual(result, FakeModelB._meta.related_fields[0])

    def test_CASE_get_field_by_name_WITH_invalid_field_SHOULD_raise(self):

        with self.assertRaises(exceptions.FieldNotFound):
            FakeModelA.get_field("nothing")

    def test_CASE_get_all_fields_SHOULD_return_all_fields(self):

        result = FakeModelB.get_all_fields()

        expected = []
        expected.extend(FakeModelB.get_fields())
        expected.extend(FakeModelB.get_related_fields())

        self.assertEqual(result, expected)


    def test_CASE_equal_SHOULD_return_bool(self):

        model_a_0 = FakeModelA(uid=5)
        model_a_1 = FakeModelA(uid=5)

        self.assertTrue(model_a_0 == model_a_1)

        model_a_2 = FakeModelA(uid=7)

        self.assertFalse(model_a_0 == model_a_2)

        model_b_0 = FakeModelB(uid=5)

        self.assertFalse(model_a_0 == model_b_0)

    def test_CASE_save_SHOULD_save(self):
        # TODO
        with self.assertRaises(NotImplementedError):

            model = FakeModelA(uid=5)
            model.save()

    def test_CASE_delete_SHOULD_delete(self):
        # TODO
        with self.assertRaises(NotImplementedError):

            model = FakeModelA(uid=5)
            model.delete()

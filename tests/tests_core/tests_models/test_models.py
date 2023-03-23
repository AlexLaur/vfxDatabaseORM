import unittest

from vfxDatabaseORM.core import models, exceptions
from vfxDatabaseORM.core.interfaces import IManager


class FakeManager(IManager):
    update_was_called = False
    insert_was_called = False

    def get(self, uid):
        return self.model_class(uid=1)

    def all(self):
        return [self.model_class(uid=i) for i in range(2)]

    def filters(self, **kwargs):
        return [self.model_class(uid=i) for i in range(2)]

    def create(self, **kwargs):
        return self.model_class(uid=1)

    def insert(self, instance):
        FakeManager.insert_was_called = True
        return self.model_class(uid=1)

    def update(self, instance):
        FakeManager.update_was_called = True
        return True

    def delete(self):
        return True


class FakeModelA(models.Model):
    manager_class = FakeManager


class FakeModelB(models.Model):
    entity_name = "FakeModel"
    manager_class = FakeManager

    name = models.StringField("name")
    related_field = models.OneToOneField(
        "related_b", to="FakeModelA", related_db_name="retaled_a"
    )


class TestModel(unittest.TestCase):
    def tearDown(self):
        FakeManager.update_was_called = False
        FakeManager.insert_was_called = False

    def test_CASE_model_without_manager_SHOULD_raise(self):
        with self.assertRaises(exceptions.ManagerNotDefined):

            class BadModelWithNoManager(models.Model):
                pass

    # get_fields() tests
    def test_CASE_get_fields_SHOULD_return_fields(self):
        result = FakeModelA.get_fields()
        self.assertEqual(result, FakeModelA._meta.fields)

    # get_related_fields() tests
    def test_CASE_get_related_fields_SHOULD_return_fields(self):
        result = FakeModelA.get_related_fields()
        self.assertEqual(result, FakeModelA._meta.related_fields)

    def test_CASE_get_related_fields_SHOULD_return_fields(self):
        result = FakeModelA.get_related_fields()
        self.assertEqual(result, FakeModelA._meta.related_fields)

    # get_field() tests
    def test_CASE_get_field_by_name_WITH_valid_field_SHOULD_return_field(self):
        result = FakeModelA.get_field("uid")
        self.assertEqual(result, FakeModelA._meta.fields[0])

    def test_CASE_get_field_by_name_WITH_valid_related_field_SHOULD_return_field(
        self,
    ):
        result = FakeModelB.get_field("related_field")
        self.assertEqual(result, FakeModelB._meta.related_fields[0])

    def test_CASE_get_field_by_name_WITH_invalid_field_SHOULD_raise(self):
        with self.assertRaises(exceptions.FieldNotFound):
            FakeModelA.get_field("nothing")

    # get_all_fields() tests
    def test_CASE_get_all_fields_SHOULD_return_all_fields(self):
        result = FakeModelB.get_all_fields()

        expected = []
        expected.extend(FakeModelB.get_fields())
        expected.extend(FakeModelB.get_related_fields())

        self.assertEqual(result, expected)

    # __eq__ tests
    def test_CASE_equal_SHOULD_return_bool(self):
        model_a_0 = FakeModelA(uid=5)
        model_a_1 = FakeModelA(uid=5)

        self.assertTrue(model_a_0 == model_a_1)

        model_a_2 = FakeModelA(uid=7)

        self.assertFalse(model_a_0 == model_a_2)

        model_b_0 = FakeModelB(uid=5)

        self.assertFalse(model_a_0 == model_b_0)

    # save() tests
    def test_CASE_save_WITH_unchanged_values_SHOULD_not_save(self):
        model = FakeModelB(uid=1, name="foo")

        result = model.save()
        self.assertFalse(result)
        self.assertFalse(FakeModelB.objects.update_was_called)

        result = model.save(name="foo")
        self.assertFalse(result)
        self.assertFalse(FakeModelB.objects.update_was_called)

    def test_CASE_save_WITH_changed_values_SHOULD_save(self):
        model = FakeModelB(uid=1, name="foo")

        result = model.save()
        self.assertFalse(result)
        self.assertFalse(FakeModelB.objects.update_was_called)

        model.name = "bar"

        result = model.save()
        self.assertTrue(result)
        self.assertTrue(FakeModelB.objects.update_was_called)

        result = model.save(name="baz")
        self.assertTrue(result)
        self.assertTrue(FakeModelB.objects.update_was_called)

    def test_CASE_save_WITH_changed_values_ON_bad_fields_SHOULD_not_save(self):
        model = FakeModelB(uid=1, name="foo")

        result = model.save(whatever="bar")
        self.assertFalse(result)
        self.assertFalse(FakeModelB.objects.update_was_called)
        self.assertFalse(FakeModelB.objects.insert_was_called)

    def test_CASE_save_WITH_changed_values_ON_new_object_SHOULD_not_create(
        self,
    ):
        model = FakeModelB(name="foo")  # uid set to 0

        result = model.save()
        self.assertTrue(result)
        self.assertFalse(FakeModelB.objects.update_was_called)
        self.assertTrue(FakeModelB.objects.insert_was_called)

    def test_CASE_save_WITH_bad_values_for_field_ON_existed_object_SHOULD_raise(
        self,
    ):
        model = FakeModelB(uid=1, name="foo")

        with self.assertRaises(exceptions.FieldBadValue):
            model.save(name=1)

    def test_CASE_save_WITH_bad_values_for_field_ON_unexisted_object_SHOULD_raise(
        self,
    ):
        model = FakeModelB(name="foo")  # uid set to 0

        with self.assertRaises(exceptions.FieldBadValue):
            model.save(name=1)

    # delete() tests
    def test_CASE_delete_SHOULD_delete(self):
        # TODO
        with self.assertRaises(NotImplementedError):
            model = FakeModelA(uid=5)
            model.delete()

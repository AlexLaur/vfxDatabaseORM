import unittest

from vfxDatabaseORM.core import models, exceptions
from vfxDatabaseORM.core.models.fields import RelatedField
from vfxDatabaseORM.core.interfaces import IManager

class FakeBadRelatedField(RelatedField):
    is_many_to_many = False
    is_one_to_many = False
    is_one_to_one = False


class FakeManager(IManager):
    get_was_called = False
    all_was_called = False
    filters_was_called = False

    should_return_one_value = False
    should_return_nothing = False

    def __init__(self, model_class):
        super(FakeManager, self).__init__(model_class)

    def get(self, uid):
        self.get_was_called = True
        return self.model_class(uid=1)

    def all(self):
        self.all_was_called = True
        return [self.model_class(uid=i) for i in range(2)]

    def filters(self, **kwargs):
        self.filters_was_called = True
        if self.should_return_one_value:
            return [self.model_class(uid=i) for i in range(1)]
        if self.should_return_nothing:
            return []
        return [self.model_class(uid=i) for i in range(2)]

    def create(self, isntance):
        return True

    def update(self, isntance):
        return True

    def delete(self):
        return True


class FakeModel1(models.Model):
    manager_class = FakeManager

    uid = models.IntegerField("id", read_only=True, default=0)
    code = models.StringField("code")

    link = models.OneToManyField(
        "link_a", to="FakeModel2", related_db_name="link_b"
    )
    many = models.ManyToManyField(
        "many_a", to="FakeModel2", related_db_name="many_b"
    )

    broken_o2o = models.OneToOneField(
        "broken_o2o_a", to="FakeModel2", related_db_name="broken_o2o_b"
    )
    broken_o2m = models.OneToOneField(
        "broken_o2m_a", to="FakeModel2", related_db_name="broken_o2m_b"
    )
    broken_m2m = models.ManyToManyField(
        "broken_m2m_a", to="FakeModel2", related_db_name="broken_m2m_b"
    )

    bad_field = FakeBadRelatedField(
        "bad_link_a", to="FakeModel2", related_db_name="bad_link_b"
    )


class FakeModel2(models.Model):
    manager_class = FakeManager

    uid = models.IntegerField("id", read_only=True, default=0)
    name = models.StringField("name")

    link = models.OneToOneField(
        "link_b", to="FakeModel1", related_db_name="link_a"
    )
    many = models.ManyToManyField(
        "many_b", to="FakeModel1", related_db_name="many_a"
    )
    custom_link = models.OneToOneField(
        "bad_link_b", to="FakeModel1", related_db_name="bad_link_a"
    )


class TestAttributeDescriptor(unittest.TestCase):
    def tearDown(self):
        FakeManager.all_was_called = False
        FakeManager.get_was_called = False
        FakeManager.filters_was_called = False
        FakeManager.should_return_one_value = False
        FakeManager.should_return_nothing = False

    # __set__
    def test_CASE_set_on_class_init_WITH_valid_data_SHOULD_set(self):
        fake_model = FakeModel1(uid=5)

        self.assertEqual(fake_model._changed, [])
        self.assertEqual(fake_model.uid, 5)

    def test_CASE_set_on_class_init_WITH_invalid_data_SHOULD_raise(self):
        with self.assertRaises(exceptions.FieldBadValue):
            FakeModel1(code=5)  # Should be a string not an int

    def test_CASE_set_on_instantiated_class_WITH_data_SHOULD_set(self):
        fake_model = FakeModel1(uid=5, code="foo")

        self.assertEqual(fake_model.code, "foo")
        self.assertEqual(len(fake_model._changed), 0)

        fake_model.code = "bar"

        self.assertEqual(fake_model.code, "bar")
        self.assertEqual(len(fake_model._changed), 1)

    def test_CASE_set_on_instantiated_class_WITH_same_data_SHOULD_not_set(self):
        fake_model = FakeModel1(uid=5, code="foo")

        # TODO

        # self.assertEqual(fake_model.code, "foo")
        # self.assertEqual(len(fake_model._changed), 0)

        # fake_model.code = "foo"

        # self.assertEqual(fake_model.code, "foo")
        # self.assertEqual(len(fake_model._changed), 0)

    def test_CASE_set_on_instantiated_class_WITH_read_only_field_SHOULD_raise(
        self,
    ):
        fake_model = FakeModel1(uid=5)
        with self.assertRaises(exceptions.ReadOnlyField):
            fake_model.uid = 10

    def test_CASE_set_on_instantiated_class_WITH_invalid_data_SHOULD_raise(
        self,
    ):
        fake_model = FakeModel1(uid=5, code="foo")
        with self.assertRaises(exceptions.FieldBadValue):
            fake_model.code = 10

    # __get__
    def test_CASE_get_on_class_SHOULD_raise(self):
        # Get on the object instead of an instance
        with self.assertRaises(exceptions.ModelNotInstantiated):
            FakeModel1.code

    def test_CASE_get_on_instantiated_class_ON_non_related_fields_SHOULD_return_value(
        self,
    ):
        fake_model = FakeModel1(uid=5, code="foo")

        self.assertEqual(fake_model.uid, 5)
        self.assertEqual(fake_model.code, "foo")

    def test_CASE_get_on_related_field_m2m_SHOULD_return_values(self):
        fake_model = FakeModel1(uid=5, code="foo")

        result = fake_model.many

        expected = [FakeModel2(uid=i) for i in range(2)]

        self.assertEqual(result, expected)

    def test_CASE_get_on_bad_related_field_m2m_SHOULD_raise(self):
        fake_model = FakeModel1(uid=5, code="foo")

        with self.assertRaises(exceptions.FieldRelatedError):
            fake_model.broken_m2m

    def test_CASE_get_on_bad_related_field_o2o_SHOULD_raise(self):
        fake_model = FakeModel1(uid=5, code="foo")

        with self.assertRaises(exceptions.FieldRelatedError):
            fake_model.broken_o2o

    def test_CASE_get_on_related_field_o2o_WITH_multiple_values_SHOULD_raise(
        self,
    ):
        fake_model = FakeModel2(uid=5, code="foo")

        with self.assertRaises(exceptions.FieldRelatedError):
            fake_model.link

    def test_CASE_get_on_related_field_o2o_SHOULD_return_value(self):
        FakeManager.should_return_one_value = True

        fake_model = FakeModel2(uid=5, code="foo")

        result = fake_model.link

        expected = FakeModel1(uid=0)

        self.assertEqual(result, expected)

    def test_CASE_get_on_related_field_o2o_WITH_empty_result_SHOULD_return_None(
        self,
    ):
        FakeManager.should_return_nothing = True

        fake_model = FakeModel2(uid=5, code="foo")

        result = fake_model.link

        self.assertIsNone(result)

    def test_CASE_get_on_related_field_o2m_SHOULD_return_values(self):
        fake_model = FakeModel1(uid=5, code="foo")

        result = fake_model.link

        expected = [FakeModel2(uid=i) for i in range(2)]

        self.assertEqual(result, expected)

    def test_CASE_get_on_bad_related_field_o2m_SHOULD_raise(self):
        fake_model = FakeModel1(uid=5, code="foo")

        with self.assertRaises(exceptions.FieldRelatedError):
            fake_model.broken_o2m

    def test_CASE_get_on_bad_related_field_SHOULD_raise(self):
        # This case should never happen

        fake_model = FakeModel1(uid=5, code="foo")

        with self.assertRaises(exceptions.FieldBadType):
            fake_model.bad_field

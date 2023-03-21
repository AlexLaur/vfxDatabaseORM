import datetime
import unittest

from vfxDatabaseORM.core.models.fields import (
    Field,
    RelatedField,
    IntegerField,
    StringField,
    FloatField,
    BooleanField,
    ListField,
    DateTimeField,
    DateField,
    OneToOneField,
    ManyToManyField,
    OneToManyField,
)


class TestField(unittest.TestCase):
    def test_CASE_attributes_SHOULD_return_attributes(self):
        field = Field(
            db_name="foo", description="test", default="bar", read_only=True
        )

        self.assertEqual(field.db_name, "foo")
        self.assertEqual(field.description, "test")
        self.assertEqual(field.default, "bar")
        self.assertEqual(field.read_only, True)
        self.assertFalse(field.is_related)

    def test_CASE_check_value_SHOULD_return_true(self):
        field = Field(
            db_name="foo", description="test", default="bar", read_only=True
        )

        self.assertTrue(field.check_value(1))
        self.assertTrue(field.check_value("foo"))
        self.assertTrue(field.check_value(None))

    def test_CASE_compute_lookup_WITH_no_lookup_SHOULD_return_computed_lookup(
        self,
    ):
        field = Field(
            db_name="foo", description="test", default="bar", read_only=True
        )

    def test_CASE_compute_lookup_WITH_lookup_SHOULD_return_computed_lookup(
        self,
    ):
        field = Field(
            db_name="foo", description="test", default="bar", read_only=True
        )

    def test_CASE_compute_lookup_WITH_related_lookup_SHOULD_return_computed_lookup(
        self,
    ):
        field = Field(
            db_name="foo", description="test", default="bar", read_only=True
        )

    def test_CASE_compute_lookup_WITH_invalid_lookup_SHOULD_raise(self):
        field = Field(
            db_name="foo", description="test", default="bar", read_only=True
        )


class TestRelatedField(unittest.TestCase):
    def test_CASE_attributes_SHOULD_return_attributes(self):
        field = RelatedField(
            db_name="foo",
            to="Bar",
            related_db_name="baz",
            description="test",
            default="bar",
            read_only=False,
        )

        self.assertEqual(field.db_name, "foo")
        self.assertEqual(field.to, "Bar")
        self.assertEqual(field.related_db_name, "baz")
        self.assertEqual(field.description, "test")
        self.assertEqual(field.default, "bar")
        self.assertEqual(field.read_only, False)
        self.assertTrue(field.is_related)

    def test_CASE_check_value_SHOULD_return_true(self):
        field = RelatedField(
            db_name="foo",
            to="Bar",
            related_db_name="baz",
            description="test",
            default="bar",
            read_only=True,
        )

        self.assertTrue(field.check_value(1))
        self.assertTrue(field.check_value("foo"))
        self.assertTrue(field.check_value(None))


class TestIntegerField(unittest.TestCase):
    def test_CASE_check_value_WITH_valid_data_SHOULD_return_true(self):
        field = IntegerField("uid")
        self.assertTrue(field.check_value(1))

    def test_CASE_check_value_WITH_invalid_data_SHOULD_return_false(self):
        field = IntegerField("uid")

        self.assertFalse(field.check_value("1"))
        self.assertFalse(field.check_value(None))


class TestStringField(unittest.TestCase):
    def test_CASE_attributes_SHOULD_return_attributes(self):
        field = StringField("name", max_width=255)

        self.assertEqual(field.max_width, 255)

    def test_CASE_check_value_WITH_valid_data_SHOULD_return_true(self):
        field = StringField("name")
        self.assertTrue(field.check_value("foo"))

    def test_CASE_check_value_WITH_invalid_data_SHOULD_return_false(self):
        field = StringField("uid", max_width=10)

        self.assertFalse(field.check_value(1))
        self.assertFalse(field.check_value(None))
        self.assertFalse(field.check_value("abcdefghijkl"))  # > 10 chars


class TestFloatField(unittest.TestCase):
    def test_CASE_check_value_WITH_valid_data_SHOULD_return_true(self):
        field = FloatField("range")
        self.assertTrue(field.check_value(1.0))

    def test_CASE_check_value_WITH_invalid_data_SHOULD_return_false(self):
        field = FloatField("range")

        self.assertFalse(field.check_value(1))
        self.assertFalse(field.check_value(None))
        self.assertFalse(field.check_value("1.0"))  # > 10 chars


class TestBooleanField(unittest.TestCase):
    def test_CASE_check_value_WITH_valid_data_SHOULD_return_true(self):
        field = BooleanField("is_valid")
        self.assertTrue(field.check_value(True))
        self.assertTrue(field.check_value(False))

    def test_CASE_check_value_WITH_invalid_data_SHOULD_return_false(self):
        field = BooleanField("is_valid")

        self.assertFalse(field.check_value("True"))
        self.assertFalse(field.check_value(None))
        self.assertFalse(field.check_value(0))
        self.assertFalse(field.check_value(10))


class TestListField(unittest.TestCase):
    def test_CASE_check_value_WITH_valid_data_SHOULD_return_true(self):
        field = ListField("values")
        self.assertTrue(field.check_value([]))
        self.assertTrue(field.check_value((1, 0)))

    def test_CASE_check_value_WITH_invalid_data_SHOULD_return_false(self):
        field = ListField("values")

        self.assertFalse(field.check_value("True"))
        self.assertFalse(field.check_value(None))
        self.assertFalse(field.check_value(0))
        self.assertFalse(field.check_value({}))


class TestDateTimeField(unittest.TestCase):
    def test_CASE_check_value_WITH_valid_data_SHOULD_return_true(self):
        field = DateTimeField("created_at")
        self.assertTrue(field.check_value(datetime.datetime.now()))

    def test_CASE_check_value_WITH_invalid_data_SHOULD_return_false(self):
        field = DateTimeField("created_at")

        self.assertFalse(field.check_value("2012-04-23T18:25:43.511Z"))
        self.assertFalse(field.check_value(None))
        self.assertFalse(field.check_value(0))
        self.assertFalse(field.check_value(datetime.date.today()))


class TestDateField(unittest.TestCase):
    def test_CASE_check_value_WITH_valid_data_SHOULD_return_true(self):
        field = DateField("created_at")
        self.assertTrue(field.check_value(datetime.date.today()))

    def test_CASE_check_value_WITH_invalid_data_SHOULD_return_false(self):
        field = DateField("created_at")

        self.assertFalse(field.check_value("2012-04-23"))
        self.assertFalse(field.check_value(None))
        self.assertFalse(field.check_value(0))


class TestOneToOneField(unittest.TestCase):
    def test_CASE_attributes_SHOULD_return_attributes(self):
        field = OneToOneField("link", to="Bar", related_db_name="foo")

        self.assertTrue(field.is_one_to_one)
        self.assertFalse(field.is_one_to_many)
        self.assertFalse(field.is_many_to_many)


class TestManyToManyField(unittest.TestCase):
    def test_CASE_attributes_SHOULD_return_attributes(self):
        field = ManyToManyField("link", to="Bar", related_db_name="foo")

        self.assertTrue(field.is_many_to_many)
        self.assertFalse(field.is_one_to_many)
        self.assertFalse(field.is_one_to_one)


class TestOneToManyField(unittest.TestCase):
    def test_CASE_attributes_SHOULD_return_attributes(self):
        field = OneToManyField("link", to="Bar", related_db_name="foo")

        self.assertTrue(field.is_one_to_many)
        self.assertFalse(field.is_many_to_many)
        self.assertFalse(field.is_one_to_one)

import unittest

from vfxDatabaseORM.core.models.fields import Field, RelatedField
from vfxDatabaseORM.core.models.options import Options


class TestOptions(unittest.TestCase):

    def test_CASE_attributes_SHOULD_return_attributes(self):

        field = Field("foo")
        related_field = RelatedField("bar", to="Bar", related_db_name="baz")

        options = Options()

        options.add_field(field)
        options.add_related_field(related_field)

        self.assertIsInstance(options.fields, list)
        self.assertIsInstance(options.related_fields, list)
        self.assertEqual(options.fields, [field])
        self.assertEqual(options.related_fields, [related_field])

    def test_CASE_add_fields(self):

        field = Field("foo")

        options = Options()

        self.assertEqual(len(options.fields), 0)
        self.assertEqual(len(options.related_fields), 0)

        options.add_field(field)

        self.assertEqual(len(options.fields), 1)
        self.assertEqual(len(options.related_fields), 0)

    def test_CASE_add_related_fields(self):

        field = RelatedField("bar", to="Bar", related_db_name="baz")

        options = Options()

        self.assertEqual(len(options.fields), 0)
        self.assertEqual(len(options.related_fields), 0)

        options.add_related_field(field)

        self.assertEqual(len(options.fields), 0)
        self.assertEqual(len(options.related_fields), 1)
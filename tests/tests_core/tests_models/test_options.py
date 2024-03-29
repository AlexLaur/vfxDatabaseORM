# -*- coding: utf-8 -*-
#
# - test_options.py -
#
# Copyright (c) 2022-2023 Alexandre Laurette
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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

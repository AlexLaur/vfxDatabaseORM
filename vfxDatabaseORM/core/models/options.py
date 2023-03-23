# -*- coding: utf-8 -*-
#
# - options.py -
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


class Options(object):
    """A class which contains informations of a model like its fields..."""

    def __init__(self):
        self._fields = []
        self._related_fields = []

    @property
    def fields(self):
        """Returns the list of basic fields associated with the model

        :return: The list of basic fields
        :rtype: list
        """
        return self._fields

    @property
    def related_fields(self):
        """Returns the list of related fields associated with the model

        :return: The list of related fields
        :rtype: list
        """
        return self._related_fields

    def add_field(self, field):
        """Registers a new field

        :param field: The field to register
        :type field: vfxDatabaseORM.src.domain.model.fields.Field
        """
        self._fields.append(field)

    def add_related_field(self, field):
        """Registers a new related field

        :param field: The related field to register
        :type field: vfxDatabaseORM.src.domain.model.fields.Field
        """
        self._related_fields.append(field)

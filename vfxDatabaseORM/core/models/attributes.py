# -*- coding: utf-8 -*-
#
# - attributes.py -
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

from vfxDatabaseORM.core import exceptions
from vfxDatabaseORM.core.models import constants


class AttributeDescriptor(object):
    """Simple descriptor to control fields in models."""

    def __init__(self, field):
        """Constructor for AttributeDescriptor

        :param field: The associated field for this descriptor
        :type field: vfxDatabaseORM.core.models.fields.Field
        """
        self._field = field
        self._attribute_name = "_{field_name}".format(field_name=field.name)

    def __get__(self, instance, owner):
        if not instance:
            raise exceptions.ModelNotInstantiated(
                "Attributes can only be retrieved on an instance of a Model "
                "and not directly on the Model class itself."
            )

        if not self._field.is_related:
            # It is not a related field, simply return the value.
            return getattr(instance, self._attribute_name)

        related_model = instance._graph.get_node_model(self._field.to)
        related_db_name = self._field.related_db_name
        related_model_fields = related_model.get_related_fields()

        related_field = None
        for field in related_model_fields:
            if field.db_name == related_db_name:
                related_field = field
                break

        if not related_field:
            raise exceptions.FieldRelatedError(
                "The corresponding {field_class_name} for '{field}' "
                "should also be defined "
                "in the related model '{related_model}'.".format(
                    field_class_name=self._field.__class__.__name__,
                    field=self._field,
                    related_model=related_model,
                )
            )

        kwargs = {}
        key = "{}{}{}{}{}".format(
            related_field.name,
            constants.LOOKUP_TOKEN,
            constants.UID_KEY,
            constants.LOOKUP_TOKEN,
            constants.LOOKUPS.EQUAL,
        )
        kwargs[key] = instance.uid

        result = related_model.objects.filters(**kwargs)

        if self._field.is_one_to_many:
            return result

        elif self._field.is_many_to_many:
            return result

        elif self._field.is_one_to_one:
            if not result:
                return None

            if len(result) > 1:
                raise exceptions.FieldRelatedError(
                    "More than one result has been found for '{field}'. "
                    "If more than one result should be returned, "
                    "use a OneToMany field instead.".format(field=self._field)
                )
            return result[0]

        else:
            # Should never happen here
            raise exceptions.FieldBadType(
                "Unknown related field. "
                "Only ManyToManyField, OneToOneField and OneToManyField "
                "are configured here."
            )

    def __set__(self, instance, value):
        if not instance._initialized:
            if not self._field.check_value(value):
                raise exceptions.FieldBadValue(
                    "The given value '{value}' is not valid "
                    "for this kind of field '{field}'.".format(
                        value=value, field=self._field
                    )
                )
            setattr(instance, self._attribute_name, value)
            return

        # We are outside of the __init__ in the instance
        if self._field.read_only:
            raise exceptions.ReadOnlyField(
                "The field '{name}' is a read only field. "
                "It cannot be updated.".format(name=self._field.name)
            )

        # TODO Cannot update related field for this moment
        if self._field.is_related:
            return

        # Check the value before storing it
        if not self._field.check_value(value):
            raise exceptions.FieldBadValue(
                "The given value '{value}' is not valid "
                "for this kind of field '{field}'.".format(
                    value=value, field=self._field
                )
            )

        if getattr(instance, self._field.name) == value:
            # It is the same value, no change to perform
            return

        # The field has been changed, mark it as changed.
        if self._field not in instance._changed:
            instance._changed.append(self._field)

        setattr(instance, self._attribute_name, value)

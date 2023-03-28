# -*- coding: utf-8 -*-
#
# - fields.py -
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

import datetime

from collections import namedtuple

import six

from vfxDatabaseORM.core import exceptions
from vfxDatabaseORM.core.models.constants import LOOKUPS, LOOKUP_TOKEN


class ComputedLookup(
    namedtuple(
        "ComputedLookup", ["field_name", "related_field_name", "lookup"]
    )
):
    pass


class BaseField(object):
    LOOKUP_TOKEN = LOOKUP_TOKEN

    LOOKUPS = [LOOKUPS.EQUAL]

    is_related = False

    def __init__(
        self, db_name, description=None, default=None, read_only=False
    ):
        """Constructor for fields

        :param db_name: The name of this field in the database
        :type db_name: str
        :param description: The description of this field, defaults to None
        :type description: str, optional
        :param default: The default value for this field, defaults to None
        :type default: any, optional
        :param read_only: Is a read only field ?, defaults to False
        :type read_only: bool, optional
        """

        self._name = None
        self._db_name = db_name
        self._description = description
        self._default = default
        self._read_only = read_only

    @property
    def db_name(self):
        """The name of the field in the database

        :return: The name of the field in the database
        :rtype: str
        """
        return self._db_name

    @property
    def name(self):
        """The name of the field in the associated model

        :return: The name of the field in the model
        :rtype: str
        """
        return self._name

    @property
    def description(self):
        """A description of this field

        :return: A description
        :rtype: str
        """
        return self._description

    @property
    def default(self):
        """The default value to apply on this field

        :return: The default value
        :rtype: _type_
        """
        return self._default

    @property
    def read_only(self):
        """Is the field is in read only mode ?

        :return: True if the field is read only, False otherwise.
        :rtype: bool
        """
        return self._read_only

    def compute_lookup(self, arg_with_filter):
        """Compute the argument in order to extract the lookup

        >>> compute_lookup(uid__lt)
        >>> ComputedLookup.field_name # uid
        >>> ComputedLookup.related_field_name # None
        >>> ComputedLookup.lookup # lt

        >>> compute_lookup(name__startswith)
        >>> ComputedLookup.field_name # name
        >>> ComputedLookup.related_field_name # None
        >>> ComputedLookup.lookup # startswith

        >>> compute_lookup(uid) # default imprementation is the equality
        >>> ComputedLookup.field_name # uid
        >>> ComputedLookup.related_field_name # None
        >>> ComputedLookup.lookup # is

        >>> compute_lookup(project__uid__lt) # default imprementation is the equality
        >>> ComputedLookup.field_name # project
        >>> ComputedLookup.related_field_name # uid
        >>> ComputedLookup.lookup # lt

        :param arg_with_filter: The argument with the lookup
        :type arg_with_filter: str
        :raises exceptions.InvalidLookUp: Raised if the lookup is not defined
        for this field.
        :return: The computed lookup
        :rtype: ComputedLookup
        """
        args = arg_with_filter.split(self.LOOKUP_TOKEN)
        field_name = None
        related_field_name = None
        lookup = None

        if len(args) == 3:
            # related field
            field_name, related_field_name, lookup = args
        elif len(args) == 2:
            # classic field with lookup
            field_name, lookup = args
        elif len(args) == 1:
            # classic field without lookup
            field_name = args[0]
        else:
            # More than three level, it is not supported yet
            raise exceptions.InvalidLookUp("Only first deph lookup works.")

        if field_name != self.name:
            # This field is seems not be the right field
            return ComputedLookup(None, None, None)

        if related_field_name and not self.is_related:
            # Reltated lookup on a field which is not related
            raise exceptions.InvalidLookUp(
                "You can't build a filter for related field with a field "
                "which is not a related field."
            )

        if lookup is None:
            # No lookup defined here, it is an equal by default
            return ComputedLookup(
                field_name, related_field_name, LOOKUPS.EQUAL
            )

        if lookup not in self.LOOKUPS:
            raise exceptions.InvalidLookUp(
                "The lookup '{lookup}' is not valid. "
                "Valid lookup are: {lookups}.".format(
                    lookup=lookup, lookups=self.LOOKUPS
                )
            )

        return ComputedLookup(field_name, related_field_name, lookup)

    def check_value(self, value):
        """Check the value for this field

        :param value: The value to check
        :type value: any
        :return: True if the value is conform for this field, False otherwise.
        :rtype: bool
        """
        return True

    def __repr__(self):
        return "<{cls_name} '{name}'>".format(
            cls_name=self.__class__.__name__, name=self.name
        )


class Field(BaseField):
    """A Simple field"""

    LOOKUPS = [
        LOOKUPS.EQUAL,
        LOOKUPS.NOT_EQUAL,
        LOOKUPS.LESS_THAN,
        LOOKUPS.GREATER_THAN,
        LOOKUPS.CONTAINS,
        LOOKUPS.IN,
        LOOKUPS.NOT_IN,
        LOOKUPS.STARTS_WITH,
        LOOKUPS.ENDS_WITH,
    ]

    is_related = False


class RelatedField(BaseField):
    LOOKUPS = [LOOKUPS.EQUAL, LOOKUPS.NOT_EQUAL, LOOKUPS.IN, LOOKUPS.NOT_IN]

    is_many_to_many = False
    is_one_to_many = False
    is_one_to_one = False

    is_related = True

    def __init__(self, db_name, to, related_db_name, *args, **kwargs):
        """Constructor for related fields

        :param db_name: The name of this field in the database
        :type db_name: str
        :param to: The name of the related Model
        :type to: str
        :param related_db_name: The name of the related field in the database
        :type related_db_name: str
        """
        self._to = to
        self._related_db_name = related_db_name

        super(RelatedField, self).__init__(db_name, *args, **kwargs)

    @property
    def to(self):
        """The destination object for this related field.

        :return: The name of the destination Model
        :rtype: str
        """
        return self._to

    @property
    def related_db_name(self):
        """The name of the related field in the database.

        :return: The name in the database of the related field
        :rtype: str
        """
        return self._related_db_name


# ##########################################


class IntegerField(Field):
    """A Field which implements an Integer"""

    LOOKUPS = [
        LOOKUPS.EQUAL,
        LOOKUPS.NOT_EQUAL,
        LOOKUPS.LESS_THAN,
        LOOKUPS.GREATER_THAN,
    ]

    def check_value(self, value):
        if value == self.default:
            return True
        if not isinstance(value, int):
            return False
        return super(IntegerField, self).check_value(value)


class StringField(Field):
    """A Field which implements a String"""

    LOOKUPS = [
        LOOKUPS.EQUAL,
        LOOKUPS.NOT_EQUAL,
        LOOKUPS.CONTAINS,
        LOOKUPS.IN,
        LOOKUPS.NOT_IN,
        LOOKUPS.STARTS_WITH,
        LOOKUPS.ENDS_WITH,
    ]

    def __init__(self, db_name, max_width=None, *args, **kwargs):
        """Construtor for StringField

        :param db_name: The name of this field in the database
        :type db_name: str
        :param max_width: The max width for this field, defaults to None
        :type max_width: int, optional
        """
        self._max_width = max_width

        super(StringField, self).__init__(db_name, *args, **kwargs)

    @property
    def max_width(self):
        """Get the max width allowed for the value of this field

        :return: The max width
        :rtype: int
        """
        return self._max_width

    def check_value(self, value):
        if value == self.default:
            return True
        if not isinstance(value, six.string_types):
            return False
        if self._max_width:
            if len(value) > self._max_width:
                return False
        return super(StringField, self).check_value(value)


class FloatField(Field):
    """A Field which implements a Float"""

    LOOKUPS = [
        LOOKUPS.EQUAL,
        LOOKUPS.NOT_EQUAL,
        LOOKUPS.LESS_THAN,
        LOOKUPS.LESS_THAN_OR_EQUAL,
        LOOKUPS.GREATER_THAN,
        LOOKUPS.GREATER_THAN_OR_EQUAL,
    ]

    def check_value(self, value):
        if value == self.default:
            return True
        if not isinstance(value, float):
            return False
        return super(FloatField, self).check_value(value)


class BooleanField(Field):
    """A Field which implements a Boolean"""

    LOOKUPS = [LOOKUPS.EQUAL, LOOKUPS.NOT_EQUAL]

    def __init__(self, db_name, default=False, **kwargs):
        """Constructor for BooleanField

        :param db_name: The name of this field in the database
        :type db_name: str
        :param default: The default value, defaults to False
        :type default: bool, optional
        """
        super(BooleanField, self).__init__(db_name, default=default, **kwargs)

    def check_value(self, value):
        if not isinstance(value, bool):
            return False
        if value == self.default:
            return True
        return super(BooleanField, self).check_value(value)


class ListField(Field):
    """A Field which implements a List"""

    LOOKUPS = [LOOKUPS.EQUAL, LOOKUPS.NOT_EQUAL, LOOKUPS.IN, LOOKUPS.NOT_IN]

    def check_value(self, value):
        if value == self.default:
            return True
        if not isinstance(value, (list, tuple)):
            return False
        return super(ListField, self).check_value(value)


class DateTimeField(Field):
    """A Field which implements a datetime.datetime"""

    LOOKUPS = [
        LOOKUPS.EQUAL,
        LOOKUPS.NOT_EQUAL,
        LOOKUPS.GREATER_THAN,
        LOOKUPS.LESS_THAN,
    ]

    def __init__(self, db_name, *args, **kwargs):
        """Constructor for DateTimeField

        :param db_name: The name of this field in the database
        :type db_name: str
        """
        kwargs.pop("default", None)
        default = datetime.datetime.now()
        super(DateTimeField, self).__init__(
            db_name, default=default, *args, **kwargs
        )

    def check_value(self, value):
        if value == self.default:
            return True
        if not isinstance(value, datetime.datetime):
            return False
        return super(DateTimeField, self).check_value(value)


class DateField(Field):
    """A Field which implements a datetime.date"""

    LOOKUPS = [
        LOOKUPS.EQUAL,
        LOOKUPS.NOT_EQUAL,
        LOOKUPS.GREATER_THAN,
        LOOKUPS.LESS_THAN,
    ]

    def __init__(self, db_name, *args, **kwargs):
        """Constructor for DateField

        :param db_name: The name of this field in the database
        :type db_name: str
        """
        kwargs.pop("default", None)
        default = datetime.date.today()
        super(DateField, self).__init__(
            db_name, default=default, *args, **kwargs
        )

    def check_value(self, value):
        if value == self.default:
            return True
        if not isinstance(value, datetime.date):
            return False
        return super(DateField, self).check_value(value)


class OneToOneField(RelatedField):
    """A Field which implements a One to One relation."""
    is_one_to_one = True


class ManyToManyField(RelatedField):
    """A Field which implements a Many to Many relation."""
    is_many_to_many = True


class OneToManyField(RelatedField):
    """A Field which implements a One to Many relation."""
    is_one_to_many = True

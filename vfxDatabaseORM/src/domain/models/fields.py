import six
import importlib

from vfxDatabaseORM.src.domain import exceptions
from vfxDatabaseORM.src.domain.models import constants


class BaseField(object):

    EQUAL_LOOKUP = "is"
    LOOKUPS = [EQUAL_LOOKUP]

    LOOKUP_TOKEN = constants.LOOKUP_TOKEN

    def __init__(
        self, db_name, description=None, default=None, read_only=False
    ):
        """Constructor for fields

        :param db_name: The name of this field in the database
        :type db_name: str
        :param description: The description of this field, defaults to None
        :type description: str, optional
        :param default: The default value for this field, defaults to None
        :type default: _type_, optional
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
        >>> lt
        >>> compute_lookup(name__startswith)
        >>> startswith
        >>> compute_lookup(uid) # default imprementation is the equality
        >>> is

        :param arg_with_filter: The argument with the lookup
        :type arg_with_filter: str
        :raises exceptions.InvalidLookUp: Raised if the lookup is not defined
        for this field.
        :return: The extracted lookup
        :rtype: str
        """
        arg_name, _, lookup = arg_with_filter.partition(self.LOOKUP_TOKEN)
        if arg_name != self.name:
            # This field is not the right field
            return None
        if not lookup:
            # No lookup defined here, it is an equal by default
            return self.EQUAL_LOOKUP
        if lookup not in self.LOOKUPS:
            raise exceptions.InvalidLookUp(
                "The lookup '{lookup}' is not valid. "
                "Valid lookup are: {lookups}.".format(
                    lookup=lookup, lookups=self.LOOKUPS
                )
            )
        return lookup

    def check_value(self, value):
        """Check the value for this field

        :param value: The value to check
        :return: True if the value is conform for this field, False otherwise.
        :rtype: bool
        """
        return True

    def __repr__(self):
        return "<{cls_name} '{name}'>".format(
            cls_name=self.__class__.__name__,
            name=self.name,
        )


class Field(BaseField):
    """A Simple field"""

    LOOKUPS = [
        BaseField.EQUAL_LOOKUP,
        "isnot",
        "lt",
        "gt",
        "contains",
        "in",
        "startswith",
        "endswith",
    ]

    RELATED = False


class IntegerField(Field):
    """A Field which implements an Integer"""

    LOOKUPS = [
        BaseField.EQUAL_LOOKUP,
        "isnot",
        "lt",
        "gt",
    ]

    def check_value(self, value):
        if not isinstance(value, int):
            return False
        return super(IntegerField, self).check_value(value)


class StringField(Field):
    """A Field which implements a String"""

    LOOKUPS = [
        BaseField.EQUAL_LOOKUP,
        "isnot",
        "contains",
        "in",
        "startswith",
        "endswith",
    ]

    def __init__(self, db_name, max_width=None, *args, **kwargs):

        self._max_width = max_width

        super(StringField, self).__init__(db_name, *args, **kwargs)

    def check_value(self, value):
        if not isinstance(value, six.string_types):
            return False
        if self._max_width:
            if len(value) > self._max_width:
                return False
        return super(StringField, self).check_value(value)


class DecimalField(Field):
    """A Field which implements a Float"""

    LOOKUPS = [
        BaseField.EQUAL_LOOKUP,
        "isnot",
        "lt",
        "gt",
    ]

    def check_value(self, value):
        if not isinstance(value, float):
            return False
        return super(DecimalField, self).check_value(value)


class BooleanField(Field):
    """A Field which implements a Boolean"""

    LOOKUPS = [
        BaseField.EQUAL_LOOKUP,
        "isnot",
    ]

    def check_value(self, value):
        if not isinstance(value, bool):
            return False
        return super(BooleanField, self).check_value(value)


class DateTimeField(Field):
    """A Field which implements a DateTime"""

    pass


class ChoiceField(Field):
    """A Field which implements a List"""

    LOOKUPS = [
        BaseField.EQUAL_LOOKUP,
        "isnot",
        "in",
    ]

    def check_value(self, value):
        if not isinstance(value, list):
            return False
        return super(ChoiceField, self).check_value(value)


###
class RelatedField(BaseField):

    LOOKUPS = [BaseField.EQUAL_LOOKUP]

    is_many_to_many = False
    is_one_to_many = False
    is_one_to_one = False

    def __init__(self, db_name, to, reverse_db_name, *args, **kwargs):

        self._reverse_db_name = reverse_db_name
        self._to = to

        super(RelatedField, self).__init__(db_name, *args, **kwargs)

    @property
    def to(self):
        return self.lazy_import(self._to)

    @property
    def reverse_db_name(self):
        return self._reverse_db_name

    @staticmethod
    def lazy_import(path):
        module_name, _, class_name = path.rpartition(".")
        module = importlib.import_module(module_name)
        my_class = getattr(module, class_name)
        return my_class


class ManyToManyField(RelatedField):
    LOOKUPS = ["in", "is"]

    is_many_to_many = True


class OneToManyField(RelatedField):

    is_one_to_many = True


class OneToOneField(RelatedField):

    is_one_to_one = True

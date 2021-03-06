import six

from vfxDatabaseORM.src.domain import exceptions
from vfxDatabaseORM.src.domain.models import constants
from vfxDatabaseORM.src.domain.models.fields import (
    Field,
    RelatedField,
    IntegerField,
)
from vfxDatabaseORM.src.domain.models.options import Options
from vfxDatabaseORM.src.domain.models.attributes import AttributeDescriptor

from vfxDatabaseORM.src.domain.ports import AbstractManager


class BaseModel(type):
    """Metaclass for all models"""

    manager_class = AbstractManager
    uid_key = constants.UID_KEY

    def __new__(cls, name, bases, attrs, **kwargs):

        # Also insure initialization is only performed for subclasses of Model
        # (excluding Model class itself)
        parents = [b for b in bases if isinstance(b, BaseModel)]
        if not parents:
            return super(BaseModel, cls).__new__(cls, name, bases, attrs)

        # Inject uid field if it doesn't exist
        if cls.uid_key not in attrs:
            for base in bases:
                uid_field = getattr(base, cls.uid_key, None)
                if not uid_field:
                    continue
                attrs[cls.uid_key] = uid_field

        # Finnaly, check if we have an uid field.
        if cls.uid_key not in attrs:
            raise exceptions.FieldNotFound(
                "The field '{field_name}' doesn't exists. "
                "You should inherit from Model class "
                "or implement the field in your Model.".format(
                    field_name=cls.uid_key
                )
            )

        # Hard work start here, create the class
        new_attrs = attrs.copy()

        options = Options()

        for attr_name, attr_value in attrs.items():

            if not isinstance(attr_value, (Field, RelatedField)):
                continue

            # Remove the attribute from new_attrs
            # A private attribute and a linked descriptor will be created
            new_attrs.pop(attr_name)

            field = attr_value

            # Insert the attribute name as the name of the field
            field._name = attr_name

            # Collect fields objects
            if isinstance(attr_value, Field):
                # Create private attribute
                new_attrs["_{}".format(attr_name)] = field.default

                # Create and set descriptors for basic fields
                attr_descriptor = AttributeDescriptor(field=field)
                new_attrs[attr_name] = attr_descriptor

                # Register field in options
                options.add_field(field)

            if isinstance(attr_value, RelatedField):
                options.add_related_field(field)

        new_attrs["_meta"] = options
        new_attrs["_initialized"] = False
        new_attrs["_changed"] = []

        return super(BaseModel, cls).__new__(cls, name, bases, new_attrs)

    @property
    def objects(cls):
        """Return the manager to communicate with the database.

        :return: The manager
        :rtype: BaseManager
        """
        return cls._get_manager()

    def _get_manager(cls):
        """Get the manager of the model.

        :return: The instance of the manager
        :rtype: BaseManager
        """
        return cls.manager_class(model_class=cls)


@six.add_metaclass(BaseModel)
class Model(object):

    entity_name = ""

    # Default field to identify an entity in a database
    uid = IntegerField("id", read_only=True, default=0)

    def __init__(self, **kwargs):
        """Constructor of the Model.
        Each given attribute is set of the corresponding field.
        """
        # Initialize fields in the model
        fields = self.get_fields()
        field_names = [field.name for field in fields]

        # Fill descriptors for basic fields
        for arg_name, arg_value in kwargs.items():
            if arg_name not in field_names:
                continue
            setattr(self, arg_name, arg_value)

        self._initialized = True

    def save(self, **kwargs):
        """Save changes on this model instance into the database"""

        if not self._changed and not kwargs:
            # Nothing has change, nothing to update
            return

        # No uid, create the entity on the database
        if not self.uid:
            # Need to create the entity
            # self.__class__.objects.insert({})
            return

        # 1. Loop through kwargs and update Model properties
        fields = self.get_fields()
        field_names = [field.name for field in fields]

        for key, value in kwargs.items():
            if key not in field_names:
                # An unknow attribute has been given here...
                continue
            setattr(self, key, value)

        # 2. Collect all updated fields
        raw_new_data = {}

        for field in self._changed:
            raw_new_data[field.db_name] = getattr(self, field.name)

        # 3. Update the model on the database
        self.__class__.objects.update(self.uid, raw_new_data)

        self._changed = []

    def delete(self):
        """Delete this Model instance from the database.

        :raises NotImplementedError: _description_
        """
        raise NotImplementedError()

    @classmethod
    def get_fields(cls):
        """Get the list of all basic fields in this Model.

        :return: List of fields
        :rtype: list
        """
        return cls._meta.fields

    @classmethod
    def get_related_fields(cls):
        """Get the list of all related fields in this Model.

        :return: List of fields
        :rtype: list
        """
        return cls._meta.related_fields

    @classmethod
    def get_field(cls, field_name):
        """Get the field object corresponding to the given field name. The
        field name correspond to the attribute name of the Model.

        For example, you have define a field in the model like this:

        >>> uid = Field("id")

        Then, you may call get_field() like this:

        >>> Model.get_field("uid")
        >>> <Field 'id'>

        :param field_name: The name of the field to retrieve
        :type field_name: str
        :raises exceptions.FieldNotFound: Raised if there is no field
        corresponding to the field_name
        :return: The field object
        :rtype: Field
        """
        for field in cls._meta.fields:
            if field.name == field_name:
                return field
        for field in cls._meta.related_fields:
            if field.name == field_name:
                return field
        raise exceptions.FieldNotFound(
            "Field '{name}' isn't setted on the Model.".format(name=field_name)
        )

    def __repr__(self):
        return "<{cls_name} type={entity_type}>".format(
            cls_name=self.__class__.__name__, entity_type=self.entity_name
        )

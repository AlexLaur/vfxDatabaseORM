import six

from vfxDatabaseORM.core import exceptions
from vfxDatabaseORM.core.models import constants
from vfxDatabaseORM.core.models.graph import Graph
from vfxDatabaseORM.core.models.options import Options
from vfxDatabaseORM.core.models.attributes import AttributeDescriptor
from vfxDatabaseORM.core.models.fields import Field, RelatedField, IntegerField
from vfxDatabaseORM.core.interfaces import IManager


class BaseModel(type):
    """Metaclass for all models"""

    manager_class = IManager
    uid_key = constants.UID_KEY

    _graph = None  # Singleton Graph

    def __new__(cls, name, bases, attrs, **kwargs):
        # Initialize the graph for all futures entities and links
        if not cls._graph:
            cls._graph = Graph()

        # Also insure initialization is only performed for subclasses of Model
        # (excluding Model class itself)
        parents = [b for b in bases if isinstance(b, BaseModel)]
        if not parents:
            return super(BaseModel, cls).__new__(cls, name, bases, attrs)

        # Do small checks
        manager_class = attrs.get("manager_class", None)
        if not manager_class:
            raise exceptions.ManagerNotDefined(
                "No Manager defined. "
                "Add a manager to the model through the attribute "
                "'manager_class'."
            )

        # Add the a new node to the graph
        cls._graph.add_node(name)

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

                # Register field in options
                options.add_field(field)

            if isinstance(attr_value, RelatedField):
                # Register field in options
                options.add_related_field(field)
                # Connect nodes together, If the field.to node is not created
                # it will be created.
                cls._graph.connect_nodes(name, field.to, field.name)

            # Create and set descriptors for basic fields
            attr_descriptor = AttributeDescriptor(field=field)
            new_attrs[attr_name] = attr_descriptor

        new_attrs["_meta"] = options
        new_attrs["_initialized"] = False
        new_attrs["_changed"] = []
        new_attrs["_graph"] = cls._graph

        new_class = super(BaseModel, cls).__new__(cls, name, bases, new_attrs)

        # Class created, register some informations in the corresponding node
        new_class._graph.add_attribute_to_node(
            node_name=name, attribute_name="model", attribute_value=new_class
        )
        new_class._graph.add_attribute_to_node(
            node_name=name,
            attribute_name="attributes",
            attribute_value=[f.name for f in options.fields],
        )
        new_class._graph.add_attribute_to_node(
            node_name=name,
            attribute_name="related_attributes",
            attribute_value=[f.name for f in options.related_fields],
        )

        return new_class

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
        fields = self.get_fields()
        field_names = [field.name for field in fields]

        # Fill descriptors for basic fields
        for arg_name, arg_value in kwargs.items():
            if arg_name not in field_names:
                continue
            setattr(self, arg_name, arg_value)

        self._initialized = True

    def save(self, **kwargs):
        if not self._changed and not kwargs:
            # Nothing has changed, nothing to update
            return

        # No uid, create the entity on the database
        if not self.uid:
            # TODO and what happen if we supercharge uid field with default to -1 ?

            # Need to create the entity
            self.__class__.objects.create(self)
            # Reset changed fields
            self._changed = []
            return

        # 1. Loop through kwargs and update Model properties
        fields = self.get_fields()
        field_names = [field.name for field in fields]

        for key, value in kwargs.items():
            if key not in field_names:
                # An unknow attribute has been given here...
                continue
            setattr(self, key, value)

        # 2. Update the model on the database
        self.__class__.objects.update(self)

        # Reset changed fields
        self._changed = []

    def delete(self):
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
    def get_all_fields(cls):
        """Get all fields (classic and related) of the Model.

        :return: List of all fields
        :rtype: list
        """
        fields = []
        fields.extend(cls._meta.fields)
        fields.extend(cls._meta.related_fields)
        return fields

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
            "This Model doesn't have a Field named '{name}'.".format(
                name=field_name
            )
        )

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.uid == other.uid

    def __repr__(self):
        return "<{cls_name} uid={entity_id}>".format(
            cls_name=self.__class__.__name__,
            entity_id=self.uid,
        )

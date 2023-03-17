import six

from vfxDatabaseORM.core import exceptions
from vfxDatabaseORM.core.models import constants
from vfxDatabaseORM.core.models.fields import IntegerField
from vfxDatabaseORM.core.interfaces import IManager


class BaseModel(type):
    """Metaclass for all models"""

    manager_class = IManager
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
        pass
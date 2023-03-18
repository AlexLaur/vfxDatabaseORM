from vfxDatabaseORM.core import exceptions


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

        if self._field._related:
            model_name = instance.__class__.__name__

            if self._field.is_one_to_many:
                return instance._graph.get_node_model(self._field.to).objects.all() # TODO should be filtered by id of the instance 
            
            elif self._field.is_one_to_one:
                return instance._graph.get_node_model(self._field.to).objects.get(-1) # TODO should be filtered by id of the instance 

            elif self._field.is_many_to_many:
                return instance._graph.get_node_model(self._field.to).objects.all() # TODO what here ?

            else:
                # TODO should never hapen here
                pass

        # It is not a related field, simply return the value.
        return getattr(instance, self._attribute_name)

    def __set__(self, instance, value):
        if not instance._initialized:
            setattr(instance, self._attribute_name, value)
            return

        # We are outside of the __init__ in the instance
        if self._field.read_only:
            raise exceptions.ReadOnlyField(
                "The field '{name}' is a read only field. "
                "It cannot be updated.".format(name=self._field.name)
            )

        # TODO Cannot update related field for this moment
        if self._field._related:
            return

        # Check the value before storing it
        if not self._field.check_value(value):
            raise exceptions.FieldBadType()

        # The field has been changed, mark it as changed.
        if self._field not in instance._changed:
            instance._changed.append(self._field)

        setattr(instance, self._attribute_name, value)

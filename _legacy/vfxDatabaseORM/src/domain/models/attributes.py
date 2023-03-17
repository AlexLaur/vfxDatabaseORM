from vfxDatabaseORM.src.domain import exceptions


class AttributeDescriptor(object):
    """Simple descriptor to control non related fields in models."""

    def __init__(self, field):
        """Constructor for AttributeDescriptor

        :param field: The associated field for this descriptor
        :type field: vfxDatabaseORM.src.domain.models.fields.Field
        """
        self._field = field
        self._attribute_name = "_{field_name}".format(field_name=field.name)

    def __get__(self, instance, owner):
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

        if not self._field.check_value(value):
            raise exceptions.FieldBadType()

        if self._field not in instance._changed:
            instance._changed.append(self._field)

        setattr(instance, self._attribute_name, value)


# class RelatedAttributeDescriptor(object):
#     def __init__(self, field):

#         self._field = field
#         self._value = None

#     def __get__(self, instance, owner):

#         linked_model = self._field.to

#         kwargs = {}
#         kwargs["{}__in".format(self._field.reverse_db_name)] = instance.uid

#         result = linked_model.objects.filters(**kwargs)

#         return result

#     def all(self):
#         pass

#     def clear(self):
#         pass

#     def add(self, what):
#         pass

#     def set(self, what):
#         pass

#     def remove(self, what):
#         pass

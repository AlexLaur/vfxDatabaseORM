from vfxDatabaseORM.core import exceptions
from vfxDatabaseORM.core.models.constants import LOOKUP_TOKEN, LOOKUPS


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

        # TODO refacto this long part
        if self._field.is_related:
            related_model = instance._graph.get_node_model(self._field.to)

            if self._field.is_one_to_many or self._field.is_many_to_many:
                related_db_name = self._field.related_db_name
                related_model_fields = related_model.get_related_fields()

                related_field = None
                for field in related_model_fields:
                    if field.db_name == related_db_name:
                        related_field = field
                        break

                if not related_field:
                    raise exceptions.FieldRelatedError(
                        "The corresponding {} for {} "
                        "should also be defined "
                        "in the related model {}.".format(
                            self._field.__class__.__name__,
                            self._field,
                            related_model,
                        )
                    )

                filters = {}
                key = "{}{}{}{}{}".format(
                    related_field.name,
                    LOOKUP_TOKEN,
                    "uid",
                    LOOKUP_TOKEN,
                    LOOKUPS.EQUAL,
                )
                filters[key] = instance.uid

                return related_model.objects.filters(**filters)

            elif self._field.is_one_to_one:
                related_db_name = self._field.related_db_name
                related_model_fields = related_model.get_related_fields()

                related_field = None
                for field in related_model_fields:
                    if field.db_name == related_db_name:
                        related_field = field
                        break

                if not related_field:
                    raise exceptions.FieldRelatedError(
                        "The corresponding OneToOne field for {} "
                        "should also be defined "
                        "in the related model {}.".format(
                            self._field, related_model
                        )
                    )

                # TODO refacto this part wich is not really good
                # And find a way for hard coded "uid"
                filters = {}
                key = "{}{}{}{}{}".format(
                    related_field.name,
                    LOOKUP_TOKEN,
                    "uid",
                    LOOKUP_TOKEN,
                    LOOKUPS.EQUAL,
                )
                filters[key] = instance.uid

                result = related_model.objects.filters(**filters)
                if not result:
                    return None

                if len(result) > 1:
                    raise exceptions.FieldRelatedError(
                        "More than one result has been found for the "
                        "OneToOne field '{}'. "
                        "If more than one result should be returned, "
                        "use a OneToMany field instead.".format(self._field)
                    )
                return result[0]

            else:
                # Should never happen here
                raise exceptions.FieldBadType(
                    "Unknown related field. "
                    "Only ManyToManyField, OneToOneField and OneToManyField "
                    "are configured here."
                )

        # It is not a related field, simply return the value.
        return getattr(instance, self._attribute_name)

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

        # The field has been changed, mark it as changed.
        if self._field not in instance._changed:
            instance._changed.append(self._field)

        setattr(instance, self._attribute_name, value)

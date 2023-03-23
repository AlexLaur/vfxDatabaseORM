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

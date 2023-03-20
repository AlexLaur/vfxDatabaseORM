import shotgun_api3

from vfxDatabaseORM.core.interfaces import IManager
from vfxDatabaseORM.core.factories import ModelFactory
from vfxDatabaseORM.core.models.constants import LOOKUPS


class ShotgridManager(IManager):

    HOST = ""
    SCRIPT_NAME = ""
    SCRIPT_KEY = ""
    HTTP_PROXY = ""

    _SG_CLIENT = None
    _LOOKUPS_MAPPING = {
        LOOKUPS.EQUAL: "is",
        LOOKUPS.NOT_EQUAL: "is_not",
        LOOKUPS.LESS_THAN: "less_than",
        LOOKUPS.GREATER_THAN: "greater_than",
        LOOKUPS.CONTAINS: "contains",
        LOOKUPS.IN: "in",
        LOOKUPS.STARTS_WITH: "starts_with",
        LOOKUPS.ENDS_WITH: "ends_with",
    }

    def __init__(self, model_class):

        super(ShotgridManager, self).__init__(model_class)

        if not self._SG_CLIENT:
            self._SG_CLIENT = shotgun_api3.Shotgun(
                self.HOST,
                script_name=self.SCRIPT_NAME,
                api_key=self.SCRIPT_KEY,
                http_proxy=self.HTTP_PROXY,
            )

    def all(self):
        """Get all entities in the database

        :return: All entites in the database
        :rtype: list
        """
        field_names = [f.db_name for f in self.model_class.get_fields()]

        query_entities = self._SG_CLIENT.find(self.model_class.entity_name, [], field_names)

        result = []
        for entity in query_entities:
            model_instance = ModelFactory.build(
                model_class=self.model_class, raw_values=entity
            )
            result.append(model_instance)

        return result

    def get(self, uid):
        """Get an entity from its ID.

        :param uid: The uid of the entity
        :type uid: The uid of the entity
        :return: The entity in the database
        :rtype: model_class instance
        """
        field_names = [f.db_name for f in self.model_class.get_fields()]
        uid_field = self.model_class.get_field(self.model_class.uid_key)

        query_entity = self._SG_CLIENT.find_one(
            self.model_class.entity_name,
            [[uid_field.db_name, "is", uid]],
            field_names,
        )

        # TODO raise or return None if nothing found ?

        model_instance = ModelFactory.build(
            model_class=self.model_class, raw_values=query_entity
        )

        return model_instance

    def filters(self, **kwargs):
        """Get entities in the database filtered by given kwargs

        :return: All entites in the database which correspond
        to the given filter
        :rtype: list
        """
        if not kwargs:
            # No filters supplied, let's return like the all() method.
            return self.all()

        model_fields = self.model_class.get_fields()

        filters = []
        field_names = [f.db_name for f in model_fields]

        for arg_name, arg_value in kwargs.items():
            for field in model_fields:
                lookup = field.compute_lookup(arg_name)
                if not lookup:
                    continue

                sg_lookup = self._LOOKUPS_MAPPING.get(lookup, None)
                if not sg_lookup:
                    # TODO Raise here ?
                    continue

                filters.append([field.db_name, sg_lookup, arg_value])

        query_entities = self._SG_CLIENT.find(
            self.model_class.entity_name, filters, field_names
        )

        result = []
        for entity in query_entities:
            model_instance = ModelFactory.build(self.model_class, entity)
            result.append(model_instance)

        return result

    def update(self, uid, new_data):
        print(uid, new_data)
        # self._SG_CLIENT.update(self.model_class.entity_name, uid, new_data)
        raise NotImplementedError()

    def create(self, data):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

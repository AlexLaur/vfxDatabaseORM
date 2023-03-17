import shotgun_api3

from vfxDatabaseORM.src.domain.ports import AbstractManager
from vfxDatabaseORM.src.domain.factories import ModelFactory


class ShotgunManagerAdapter(AbstractManager):

    HOST = ""
    SCRIPT_NAME = ""
    SCRIPT_KEY = ""
    HTTP_PROXY = ""

    _SG = None

    LOOKUPS = {
        "is": "is",
        "isnot": "is_not",
        "lt": "less_than",
        "gt": "greater_than",
        "contains": "contains",
        "in": "in",
        "startswith": "starts_with",
        "endswith": "ends_with",
    }

    def __init__(self, model_class):

        super(ShotgunManagerAdapter, self).__init__(model_class)

        if not self._SG:
            # Init shotgun
            self._SG = shotgun_api3.Shotgun(
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
        entities = self._SG.find(self.model_class.entity_name, [], field_names)

        result = []
        for entity in entities:
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

        entity = self._SG.find_one(
            self.model_class.entity_name,
            [[uid_field.db_name, "is", uid]],
            field_names,
        )
        model_instance = ModelFactory.build(
            model_class=self.model_class, raw_values=entity
        )
        return model_instance

    def filters(self, **kwargs):
        result = []
        if not kwargs:
            return result

        filters = []
        field_names = [f.db_name for f in self.model_class.get_fields()]

        for arg_name, arg_value in kwargs.items():
            for field in self.model_class.get_fields():
                lookup = field.compute_lookup(arg_name)
                if not lookup:
                    continue
                filters.append(
                    [field.db_name, self.LOOKUPS.get(lookup), arg_value]
                )

            # TEMP
            # for field in self.model_class._meta.related_fields:
            #     lookup = field.compute_lookup(arg_name)
            #     if not lookup:
            #         continue
            #     filters.append(
            #             [field.db_name, self.LOOKUPS.get(lookup), [{"type": field.to.entity_name, "id": arg_value}]]
            #         )
            # END TEMP

        entities = self._SG.find(
            self.model_class.entity_name, filters, field_names
        )

        for entity in entities:
            model_instance = ModelFactory.build(self.model_class, entity)
            print(model_instance)
            result.append(model_instance)

        return result

    def update(self, uid, new_data):

        print(uid, new_data)
        # self._SG.update(self.model_class.entity_name, uid, new_data)

    def create(self, data):
        pass

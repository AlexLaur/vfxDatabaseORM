# -*- coding: utf-8 -*-
#
# - shotgridManager.py -
#
# Copyright (c) 2022-2023 Alexandre Laurette
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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

        query_entities = self._SG_CLIENT.find(
            self.model_class.entity_name, [], field_names
        )

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

        if not query_entity:
            # No entity found, return None
            return None

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

        all_fields = self.model_class.get_all_fields()

        field_names = [f.db_name for f in self.model_class.get_fields()]
        filters = []

        for arg_name, arg_value in kwargs.items():
            for field in all_fields:
                computed_lookup = field.compute_lookup(arg_name)
                if not computed_lookup.lookup:
                    continue

                sg_lookup = self._LOOKUPS_MAPPING.get(
                    computed_lookup.lookup, None
                )
                if not sg_lookup:
                    # TODO No corresponding lookup found, Raise here ?
                    continue

                if not field.is_related:
                    # It is a classic field
                    filters.append([field.db_name, sg_lookup, arg_value])
                    continue

                # It is a related field
                related_model = self.model_class._graph.get_node_model(
                    field.to
                )  # TODO ugly private member access
                related_field = related_model.get_field(
                    computed_lookup.related_field_name
                )
                filters.append(
                    [
                        "{}.{}.{}".format(
                            field.db_name,
                            related_model.entity_name,
                            related_field.db_name,
                        ),
                        computed_lookup.lookup,
                        arg_value,
                    ]
                )

        # print(self.model_class.entity_name, filters, field_names)

        query_entities = self._SG_CLIENT.find(
            self.model_class.entity_name, filters, field_names
        )

        result = []
        for entity in query_entities:
            model_instance = ModelFactory.build(self.model_class, entity)
            result.append(model_instance)

        return result

    def update(self, instance):
        """Update the given instance into ShotGrid

        :param instance: The instance to update
        :type instance: vfxDatabaseORM.core.models.Model
        """
        new_data = {
            field.db_name: getattr(instance, field.name)
            for field in instance._changed
        }
        if not new_data:
            return

        self._SG_CLIENT.update(
            self.model_class.entity_name, instance.uid, new_data
        )

    def create(self, **kwargs):
        """From given arguments, create an entity in the database and return
        the instance.

        :return: The created entity
        :rtype: vfxDatabaseORM.core.models.Model
        """
        instance = self.model_class(**kwargs)
        new_instance = self.insert(instance)
        return new_instance

    def insert(self, instance):
        """Insert the entity on Shotgrid

        :param instance: The instance to create
        :type instance: vfxDatabaseORM.core.models.Model
        :return: A new instance
        :rtype: vfxDatabaseORM.core.models.Model
        """
        fields = self.model_class.get_fields()
        non_read_only_fields = [
            field for field in fields if not field.read_only
        ]

        new_data = {
            field.db_name: getattr(instance, field.name)
            for field in non_read_only_fields
        }
        if not new_data:
            return instance

        field_names = [f.db_name for f in self.model_class.get_fields()]

        query_data = self._SG_CLIENT.create(
            self.model_class.entity_name, new_data, field_names
        )

        new_instance = ModelFactory.build(self.model_class, query_data)

        return new_instance

    def delete(self, instance):
        """Delete the entity on Shotgrid

        :param instance: The instance to delete
        :type instance: vfxDatabaseORM.core.models.Model
        :return: True if done, False otherwise
        :rtype: bool
        """
        self._SG_CLIENT.delete(self.model_class.entity_name, instance.uid)
        return True

# -*- coding: utf-8 -*-
#
# - manager.py -
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

import abc

ABC = abc.ABCMeta("ABC", (object,), {})


class IManager(ABC):
    """Interface for all managers."""

    def __init__(self, model_class):
        self.model_class = model_class

    @abc.abstractmethod
    def get(self, uid):
        """Get object in the database for the given uid.

        :param uid: The id of the object in the database
        :type uid: int
        """
        pass

    @abc.abstractmethod
    def all(self):
        """Get all objects in the database."""
        pass

    @abc.abstractmethod
    def filters(self, **kwargs):
        """Filters objects in the database."""
        pass

    @abc.abstractmethod
    def create(self, **kwargs):
        """Create the object in the database from the given arguments."""
        pass

    @abc.abstractmethod
    def insert(self, instance):
        """Insert the object in the database. It is like the create() method
        but it takes an instance instead of arguments.

        :param instance: The instance to insert in the database.
        :type instance: vfxDatabaseORM.core.models.Model
        """
        pass

    @abc.abstractmethod
    def update(self, instance):
        """Update the object in the database.

        :param instance: The instance to update in the database.
        :type instance: vfxDatabaseORM.core.models.Model
        """
        pass

    @abc.abstractmethod
    def delete(self, instance):
        """Delete the object from the database."""
        pass

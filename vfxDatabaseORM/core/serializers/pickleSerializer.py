# -*- coding: utf-8 -*-
#
# - jsonSerializer.py -
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

import pickle

from vfxDatabaseORM.core.interfaces import ISerializer


class PickleSerializer(ISerializer):
    def serialize(self, instance):
        """Serialize the given instance in the pickle format

        :param instance: The instance to serialize
        :type instance: vfxDatabaseORM.core.models.Model
        :return: The serialized model
        :rtype: str
        """
        data = {}
        for field in self.model_class.get_fields():
            data[field.name] = getattr(instance, field.name)
        return pickle.dumps(data)

    def deserialize(self, data):
        """Deserialize the data and create a new Model instance

        :param data: The data (in pickle format)
        :type data: str
        :return: A new instance
        :rtype: vfxDatabaseORM.core.models.Model
        """
        unpickled_data = pickle.loads(data)
        return self.model_class(**unpickled_data)

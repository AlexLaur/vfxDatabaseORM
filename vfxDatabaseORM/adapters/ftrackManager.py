# -*- coding: utf-8 -*-
#
# - ftrackManager.py -
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

import ftrack_api

from vfxDatabaseORM.core.interfaces import IManager
from vfxDatabaseORM.core.factories import ModelFactory


class FTrackManager(IManager):
    HOST = ""
    API_NAME = ""
    API_KEY = ""

    _SESSION = None

    def __init__(self, model_class):
        super(FTrackManager, self).__init__(model_class)

        if not self._SESSION:
            self._SESSION = ftrack_api.Session(
                server_url=self.HOST,
                api_key=self.API_KEY,
                api_user=self.API_NAME,
            )

    def get(self, uid):
        raise NotImplementedError()

    def all(self):
        raise NotImplementedError()

    def filters(self, **kwargs):
        raise NotImplementedError()

    def create(self, **kwargs):
        raise NotImplementedError()

    def insert(self, instance):
        raise NotImplementedError()

    def update(self, instance):
        raise NotImplementedError()

    def delete(self, instance):
        raise NotImplementedError()

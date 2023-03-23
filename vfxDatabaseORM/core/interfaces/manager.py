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
    def __init__(self, model_class):
        self.model_class = model_class

    @abc.abstractmethod
    def get(self, uid):
        pass

    @abc.abstractmethod
    def all(self):
        pass

    @abc.abstractmethod
    def filters(self, **kwargs):
        pass

    @abc.abstractmethod
    def create(self, **kwargs):
        pass

    @abc.abstractmethod
    def insert(self, instance):
        pass

    @abc.abstractmethod
    def update(self, instance):
        pass

    @abc.abstractmethod
    def delete(self):
        pass

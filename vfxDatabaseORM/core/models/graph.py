# -*- coding: utf-8 -*-
#
# - graph.py -
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

import networkx as nx

from vfxDatabaseORM.core import exceptions


class Graph(object):
    _graph = None

    def __init__(self):
        if not self._graph:
            self._graph = nx.Graph()

    @property
    def nodes(self):
        return list(self._graph.nodes(data=True))

    @property
    def edges(self):
        return list(self._graph.edges(data=True))

    def add_node(self, node_name):
        self._graph.add_node(
            node_name, model=None, attributes=[], related_attributes=[]
        )

    def get_node_model(self, node_name):
        if node_name not in self._graph.nodes:
            raise exceptions.ModelNotRegistered(
                "The model '{node_name}' cannot be found. "
                "Have you defined it ?".format(node_name=node_name)
            )
        return self._graph.nodes(data=True)[node_name].get("model")

    def add_attribute_to_node(
        self, node_name, attribute_name, attribute_value
    ):
        self._graph.nodes[node_name][attribute_name] = attribute_value

    def connect_nodes(self, node_name_a, node_name_b, on_attr):
        self._graph.add_edge(
            node_name_a, node_name_b, origin=node_name_a, on_attr=on_attr
        )

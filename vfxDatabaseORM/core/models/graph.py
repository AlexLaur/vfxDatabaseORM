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
        """Get all nodes (with data) of the graph.

        :return: All nodes in the graph
        :rtype: list
        """
        return list(self._graph.nodes(data=True))

    @property
    def edges(self):
        """Get all edges (with data) of the graph.

        :return: All edges in the graph
        :rtype: list
        """
        return list(self._graph.edges(data=True))

    def add_node(self, node_name):
        """Add a node to the graph

        :param node_name: The name of the node
        :type node_name: str
        """
        self._graph.add_node(
            node_name, model=None, attributes=[], related_attributes=[]
        )

    def get_node_model(self, node_name):
        """Get the Model Class linked to the node.

        :param node_name: The name of the node
        :type node_name: str
        :raises exceptions.ModelNotRegistered: Raised if no Model has been
        registered for this node.
        :return: The class corresponding to this node
        :rtype: vfxDatabaseORM.core.models.Model
        """
        if node_name not in self._graph.nodes:
            raise exceptions.ModelNotRegistered(
                "The model '{node_name}' cannot be found. "
                "Have you defined it ?".format(node_name=node_name)
            )
        return self._graph.nodes(data=True)[node_name].get("model")

    def add_attribute_to_node(
        self, node_name, attribute_name, attribute_value
    ):
        """Add an attribute to the node.

        :param node_name: The name of the node
        :type node_name: str
        :param attribute_name: The name of the attribute to add
        :type attribute_name: str
        :param attribute_value: The value of the attribute
        :type attribute_value: any
        """
        self._graph.nodes[node_name][attribute_name] = attribute_value

    def connect_nodes(self, node_name_a, node_name_b, on_attr):
        """Connect two nodes together

        :param node_name_a: The name of the first node
        :type node_name_a: str
        :param node_name_b: The name of the second node
        :type node_name_b: str
        :param on_attr: Tag the attribute on which the connection is made
        :type on_attr: str
        """
        self._graph.add_edge(
            node_name_a, node_name_b, origin=node_name_a, on_attr=on_attr
        )

# -*- coding: utf-8 -*-
#
# - test_graph.py -
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

import unittest

from vfxDatabaseORM.core.models.graph import Graph


FakeModel = type("FakeModel", (object,), {})


class TestGraph(unittest.TestCase):
    def test_CASE_graph_init_SHOULD_be_singleton(self):
        graph_0 = Graph()
        graph_1 = Graph()

        # self.assertEqual(graph_0._graph, graph_1._graph) # TODO doesn't work !

    def test_CASE_add_node_SHOULD_graph_contains_nodes(self):
        graph = Graph()

        self.assertEqual(graph.nodes, [])

        graph.add_node("A")

        self.assertEqual(
            graph.nodes,
            [
                (
                    "A",
                    {
                        "attributes": [],
                        "model": None,
                        "related_attributes": [],
                    },
                )
            ],
        )

    def test_CASE_add_attribute_to_node_SHOULD_add_attribute(self):
        graph = Graph()
        graph.add_node("A")

        self.assertEqual(
            graph.nodes,
            [
                (
                    "A",
                    {
                        "attributes": [],
                        "model": None,
                        "related_attributes": [],
                    },
                )
            ],
        )

        graph.add_attribute_to_node("A", "model", FakeModel)

        self.assertEqual(
            graph.nodes,
            [
                (
                    "A",
                    {
                        "attributes": [],
                        "model": FakeModel,
                        "related_attributes": [],
                    },
                )
            ],
        )

    def test_CASE_get_node_model_SHOULD_return_class(self):
        graph = Graph()
        graph.add_node("A")
        graph.add_attribute_to_node("A", "model", FakeModel)

        model_class = graph.get_node_model("A")

        self.assertEqual(model_class, FakeModel)

    def test_CASE_connect_nodes_WITH_existing_nodes(self):
        graph = Graph()

        self.assertEqual(graph.nodes, [])
        self.assertEqual(graph.edges, [])

        graph.add_node("A")
        graph.add_node("B")

        self.assertEqual(len(graph.nodes), 2)
        self.assertEqual(len(graph.edges), 0)

        graph.connect_nodes("A", "B", on_attr="foo")

        self.assertEqual(len(graph.edges), 1)
        self.assertEqual(
            graph.edges, [("A", "B", {"on_attr": "foo", "origin": "A"})]
        )

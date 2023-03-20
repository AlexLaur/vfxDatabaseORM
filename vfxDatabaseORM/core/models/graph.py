import networkx as nx

from vfxDatabaseORM.core import exceptions


class Graph(object):

    _graph = None

    def __init__(self):
        if not self._graph:
            self._graph = nx.Graph()

    def add_node(self, node_name):
        self._graph.add_node(node_name, model=None)

    def get_node_model(self, node_name):
        if node_name not in self._graph.nodes:
            raise exceptions.ModelNotRegistered(
                "The model '{node_name}' cannot be found. "
                "Have you defined it ?".format(node_name=node_name)
            )
        return self._graph.nodes(data=True)[node_name].get("model")

    def add_attribute_to_node(self, node_name, attribute_name, attribute_value):
        self._graph.nodes[node_name][attribute_name] = attribute_value

    def connect_nodes(self, node_name_a, node_name_b, on_attr):
        self._graph.add_edge(node_name_a, node_name_b, origin=node_name_a, on_attr=on_attr)
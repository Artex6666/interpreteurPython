# -*- coding: utf-8 -*-

import uuid
import graphviz as gv

def print_tree_graph(t):
    graph = gv.Digraph(format='pdf')
    graph.attr('node', shape='circle')
    add_node(graph, t)
    graph.render(filename='../img/graph.gv') #Pour Sauvegarder
    graph.view() #Pour afficher

def add_node(graph, node):
    my_id = uuid.uuid4()

    if not hasattr(node, "children"):
        graph.node(str(my_id), label=str(node))
        return my_id

    label = node.name

    if hasattr(node, "value"):
        label += f"({node.value})"

    if hasattr(node, "operator"):
        label += f"({node.operator})"

    if hasattr(node, "func_name"):
        label += f"({node.func_name})"


    if hasattr(node, "number"):
        label += f"({node.number})"

    graph.node(str(my_id), label=label)

    for child in node.children:
        graph.edge(str(my_id), str(add_node(graph, child)), arrowsize='0')

    return my_id
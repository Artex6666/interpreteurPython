# -*- coding: utf-8 -*-

import uuid
import graphviz as gv

def print_tree_graph(t):
    graph = gv.Digraph(format='pdf')
    graph.attr('node', shape='circle')
    add_node(graph, t)
    graph.render(filename='../../img/graph.gv') #Pour Sauvegarder
    graph.view() #Pour afficher

def add_node(graph, t):
    my_id = uuid.uuid4()

    if not hasattr(t, "children"):
        graph.node(str(my_id), label=str(t))
        return my_id

    label = t.name

    if hasattr(t, "value"):
        label += f"({t.value})"

    if hasattr(t, "operator"):
        label += f"({t.operator})"

    if hasattr(t, "func_name"):
        label += f"({t.func_name})"


    if hasattr(t,"number"):
        label += f"({t.number})"

    graph.node(str(my_id), label=label)

    for child in t.children:
        graph.edge(str(my_id), str(add_node(graph, child)), arrowsize='0')

    return my_id
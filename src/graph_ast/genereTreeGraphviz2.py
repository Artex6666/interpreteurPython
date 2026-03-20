# -*- coding: utf-8 -*-

import uuid
import graphviz as gv

def printTreeGraph(t):
    graph = gv.Digraph(format='pdf')
    graph.attr('node', shape='circle')
    addNode(graph, t)
    graph.render(filename='../../img/graph.gv') #Pour Sauvegarder
    graph.view() #Pour afficher

def addNode(graph, t):
    myId = uuid.uuid4()

    if not hasattr(t, "children"):
        graph.node(str(myId), label=str(t))
        return myId

    label = t.name

    if hasattr(t, "value"):
        label += f"({t.value})"

    if hasattr(t, "operator"):
        label += f"({t.operator})"

    if hasattr(t, "func_name"):
        label += f"({t.func_name})"


    if hasattr(t,"number"):
        label += f"({t.number})"

    graph.node(str(myId), label=label)

    for child in t.children:
        graph.edge(str(myId), str(addNode(graph, child)), arrowsize='0')

    return myId 
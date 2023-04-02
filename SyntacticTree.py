# -*-coding:utf-8 -*-
"""
@File    :   SyntacticTree.py
@Date    :   2023/04/01
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase que permite la construccion del arbol sintactico a partir de la expresion postfix.
"""

# -*-coding:utf-8 -*-
"""
@File    :   SyntacticTree.py
@Date    :   2023/04/01
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase que permite la construccion del arbol sintactico a partir de la expresion postfix.
"""

from graphviz import Digraph
from Node import Node


class SyntacticTree:
    def __init__(self, title):
        self.root = None
        self.title = title

    def tree_construction(self, postfix):
        stack = []
        for symbol in postfix:
            if str(symbol) not in "|*.+?":
                if type(symbol) == int:
                    symbol = str(symbol)
                node = Node(symbol)
                stack.append(node)
            elif symbol == "|":
                node = Node(symbol)
                node.right = stack.pop()
                node.left = stack.pop()
                stack.append(node)
            elif symbol == ".":
                node = Node(symbol)
                node.right = stack.pop()
                node.left = stack.pop()
                stack.append(node)
            elif symbol == "*":
                node = Node(symbol)
                node.left = stack.pop()
                stack.append(node)
            elif symbol == "+":
                node = Node(symbol)
                node.left = stack.pop()
                stack.append(node)
            elif symbol == "?":
                node = Node(symbol)
                node.left = stack.pop()
                stack.append(node)
        self.root = stack.pop()

    # Lectura Left Most
    def left_most(self):
        if self.root is None:
            return []
        stack = [self.root]
        result = []
        while len(stack) > 0:
            node = stack.pop(0)
            result.append(node.data)
            if node.left is not None:
                stack.insert(0, node.left)
            if node.right is not None:
                stack.insert(0, node.right)
        return list(reversed(result))

    def generate_dot(self, node, graph):
        if node is not None:
            graph.node(str(id(node)), node.data)
            if node.left is not None:
                graph.edge(str(id(node)), str(id(node.left)))
                self.generate_dot(node.left, graph)
            if node.right is not None:
                graph.edge(str(id(node)), str(id(node.right)))
                # Esto es una operacion recursiva
                self.generate_dot(node.right, graph)

    def visualize_tree(self, node=None):
        
        description = ("Syntactic Tree of " + self.title)
        graph = Digraph(comment=description)
        graph.attr(
            labelloc="t",
            label=description
        )
        final_node = self.root
        self.generate_dot(final_node, graph)
        graph.render("SyntacticTree_of_" + self.title, format="png", view=True)

# -*-coding:utf-8 -*-
'''
@File    :   Node.py
@Date    :   2023/04/01
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase Node que implemeta la estructura de nodos para construir el arbol sintactico.
'''

class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
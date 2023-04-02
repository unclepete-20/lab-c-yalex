# -*-coding:utf-8 -*-
'''
@File    :   main.py
@Date    :   2023/04/01
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Main donde se ejecuta toda la logica implementada.
'''

import time
from Postfix import Postfix
import pyfiglet
from Yalex import Yalex
from SyntacticTree import SyntacticTree



header = pyfiglet.figlet_format("Y A L E X")
print(header)

yalex = "./yalex/slr-1.yal"

start_time = time.time()

regex = Yalex(yalex).read_yalex()

post = Postfix(regex)
postfix = post.shunting_yard()
print("\npostfix: ", postfix)


tree = SyntacticTree(yalex)
tree.tree_construction(postfix)
tree.visualize_tree()

result = tree.left_most()

time.sleep(1)
end_time = time.time()

total_time = end_time - start_time

print("\n===========================================================================================")

print(f"\nLa construccion del arbol sintactico tuvo un tiempo de ejecucion de {total_time} segundos\n")

print("===========================================================================================\n")
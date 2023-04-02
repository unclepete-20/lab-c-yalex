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
from Errors import Errors
from Yalex import Yalex
from SyntacticTree import SyntacticTree



header = pyfiglet.figlet_format("Y A L E X")
print(header)

yalex = "./yalex/slr-1.yal"

regex = Yalex(yalex).read_yalex()

post = Postfix(regex)
postfix = post.shunting_yard()
print("\npostfix: ", postfix)

# -*-coding:utf-8 -*-
'''
@File    :   main.py
@Date    :   2023/02/26
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Main donde se ejecuta toda la logica implementada.
'''

import time
from Postfix import Postfix
from Thompson import Thompson
from Errors import Errors
from Subset import SubsetDFA
from Direct import DirectDFA
import pyfiglet

# Regex de prueba

# r = 'a(b*|c+)b|baa'
# r = 'ab*a(b+)'
r = 'b*ab?'

# test = 'acb'
# test = 'abbab'
test = 'bbbbab'

header = pyfiglet.figlet_format("L E X E R")
print(header)

# Se verifican errores, si los hay
Errors(r)

# Se convierte la expresion regular a formato postfix
expression = Postfix(r).postfixExpression

# Se realiza la construccion de un AFN

print("===========================================================================================")
start_time = time.time()
afn = Thompson(expression).nfa
time.sleep(1)
end_time = time.time()

total_time = end_time - start_time

print(f"\nLa construccion de AFN tuvo un tiempo de ejecucion de {total_time} segundos\n")
    
print("===========================================================================================")

# Se realiza la construccion de un AFD por medio de subconjuntos
start_time = time.time()
subset_dfa = SubsetDFA(expression, afn).subset_dfa
time.sleep(1)
end_time = time.time()

total_time = end_time - start_time

print(f"\nLa construccion de AFD por Subconjuntos tuvo un tiempo de ejecucion de {total_time} segundos\n")

simulate_subset = subset_dfa.simulate(test)

if (simulate_subset == True):
    print(f"\nLa cadena {test} SI pertence a L(r) de la expresion regular {r} en AFD por Subconjuntos\n")
else:
    print(f"\nLa cadena {test} NO pertence a L(r  de la expresion regular {r} en AFD por Subconjuntos\n")

print("===========================================================================================")

# Se realiza la construccion Directa de AFD
start_time = time.time()
directa_dfa = DirectDFA(expression).direct_dfa
time.sleep(1)
end_time = time.time()

total_time = end_time - start_time

print(f"\nLa construccion de AFD Directo tuvo un tiempo de ejecucion de {total_time} segundos\n")

simulate_direct = directa_dfa.simulate(test)

if (simulate_direct == True):
    print(f"\nLa cadena {test} SI pertence a L(r) de la expresion regular {r} en AFD Directo\n")
else:
    print(f"\nLa cadena {test} NO pertence a L(r  de la expresion regular {r} en AFD Directo\n")

print("===========================================================================================")
    
minimized = SubsetDFA(expression, afn).minimized_dfa
simulate_minimized = subset_dfa.simulate(test)

if (simulate_minimized == True):
    print(f"\nLa cadena {test} SI pertence a L(r) de la expresion regular {r} en AFD Minimizado\n")
else:
    print(f"\nLa cadena {test} NO pertence a L(r  de la expresion regular {r} en AFD Minimizado\n")

print("===========================================================================================")


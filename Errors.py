# -*-coding:utf-8 -*-
"""
@File    :   Errors.py
@Date    :   2023/03/10
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase para verificar errores en las expresiones regulares.
"""

import sys


class Errors(object):
    def __init__(self, regex):
        self.regex = regex
        self.valid_operators = ["+", "?", "*", ".", "|"]

        # Se verifican instantaneamente los errores
        self.valid = self.check_errors()

    # Se definen casos en los que se debe verificar si existen errores o no
    def check_errors(self):

        # Se verifica que la expresion regular no este vacia
        if self.regex == "":
            sys.exit("Error: expresion regular vacia.")

        # Se verifica que no hayan or's al final de la expresion regular
        if self.regex.endswith("|"):
            sys.exit("Error: expresion regular invalida")

        # Se cuentan los paréntesis derechos e izquierdos.
        l_parenthesis = self.regex.count("(")
        r_parenthesis = self.regex.count(")")

        # Se verifica que la cantidad de parentesis sea la misma de ambos lados
        if l_parenthesis != r_parenthesis or r_parenthesis != l_parenthesis:
            sys.exit("Error: expresion regular invalida")

        # Se verifica que no hayan operadores al inicio de la expresion regular
        for operator in self.valid_operators:
            if self.regex == operator or self.regex.startswith(operator):
                sys.exit("Error: expresion regular invalida")

        # Se separa la expresion regular para realizar un analisis mas riguroso.
        regex_list = list(self.regex)

        # Ahora se recorre dicha expresion.
        for i in reversed(range(1, len(regex_list))):
            if (regex_list[i] in self.valid_operators) and (regex_list[i - 1] == "|"):

                sys.exit(f"Error: expresion regular invalida")

        # Si todo cumple correctamente, se imprime este mensaje
        print(
            f"\nLa expresion regular {self.regex} es correcta... Procediendo con las construcciones respectivas\n"
        )

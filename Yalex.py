# -*-coding:utf-8 -*-
"""
@File    :   Yalex.py
@Date    :   2023/04/01
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase que permite la lectura e interpretacion de los archivos Yalex.
"""


class Yalex(object):
    def __init__(self, yalex):
        self.yal = yalex

    def read_yalex(self):

        # Aqui se guardaran todas las funciones let
        functions = []
        clean_functions = []

        # Aqui se guardaran los regex
        regex = []
        clean_regex_expression = []

        # Se almacenan palabras reservadas encontradas en la gramatica del yalex
        reserved_word = ""

        # Se hace lectura del archivo Yalex
        with open(self.yal, "r") as yal:
            lines = yal.readlines()

        active_elements = False

        # Se obtienen los elementos de la expresion
        for line in lines:
            # Se extraen los tokens de la gramatica para trabajarlos
            if active_elements:
                temporary_reserved_word = ""
                for x in line:
                    if x != " ":
                        if x != "\n":
                            if x != "'":
                                temporary_reserved_word += x
                            if x == "|":
                                regex.append(temporary_reserved_word)
                                temporary_reserved_word = ""
                        else:
                            regex.append(temporary_reserved_word)
            # Se obtienen todas sus functions
            if line.startswith("let"):
                functions.append(line[4:-1])
            # Se activan los tokens para continuar con el proceso
            if line.startswith("rule"):
                active_elements = True

        # realizar limpieza de los datos de regex
        for x in range(len(regex)):
            temporary_reserved_word = ""
            for l in regex[x]:
                temporary_reserved_word += l
                if "{" in temporary_reserved_word:
                    temporary_reserved_word = temporary_reserved_word[:-1]
                    break
                if "(*" in temporary_reserved_word:
                    temporary_reserved_word = temporary_reserved_word[:-2]
                    break
            regex[x] = temporary_reserved_word

        for x in regex:
            if len(x) != 0:
                if x.count('"') == 2:
                    x = x[1:-1]
                clean_regex_expression.append(x)

        # limpieza de los datos de functions
        for f in functions:
            deletable_array = []
            temp_expression = []
            nombre, definition = f.split("=")
            nombre = nombre.strip()
            definition = definition.strip()
            temp_expression.append(nombre)
            reserved_word = ""
            # Se hace una revision de la definition
            if definition[0] == "[":
                definition = definition[1:-1]
                for x in definition:
                    reserved_word += x
                    if reserved_word[0] == '"' or reserved_word[0] == "'":
                        if reserved_word.count("'") == 2:
                            reserved_word = reserved_word[1:-1]

                            if len(reserved_word) == 2:
                                if reserved_word == "\s":
                                    reserved_word = bytes(" ", "utf-8").decode(
                                        "unicode_escape"
                                    )
                                else:
                                    reserved_word = bytes(
                                        reserved_word, "utf-8"
                                    ).decode("unicode_escape")
                                deletable_array.append(ord(reserved_word))

                            else:
                                if reserved_word == " ":
                                    reserved_word = bytes(" ", "utf-8").decode(
                                        "unicode_escape"
                                    )
                                    deletable_array.append(ord(reserved_word))
                                else:
                                    deletable_array.append(ord(reserved_word))
                            reserved_word = ""
                        if reserved_word.count('"') == 2:
                            # si tiene \ o no tiene dependiendo de este se trabajara conforme a ello
                            reserved_word = reserved_word[1:-1]
                            temporary_reserved_word = ""

                            if chr(92) in reserved_word:
                                for y in reserved_word:
                                    temporary_reserved_word += y
                                    if temporary_reserved_word.count(chr(92)) == 2:
                                        if temporary_reserved_word[:-1] == "\s":
                                            temp_reserved_word = " "
                                        else:
                                            temp_reserved_word = (
                                                temporary_reserved_word[:-1]
                                            )
                                        reserved_word = bytes(
                                            temp_reserved_word, "utf-8"
                                        ).decode("unicode_escape")
                                        deletable_array.append(ord(reserved_word))
                                        temporary_reserved_word = (
                                            temporary_reserved_word[2:]
                                        )
                                if len(temporary_reserved_word) != 0:
                                    if temporary_reserved_word == "\s":
                                        temp_reserved_word = " "
                                    else:
                                        temp_reserved_word = temporary_reserved_word
                                    reserved_word = bytes(
                                        temp_reserved_word, "utf-8"
                                    ).decode("unicode_escape")
                                    deletable_array.append(ord(reserved_word))
                            else:
                                reserved_word = list(reserved_word)
                                for w in range(len(reserved_word)):
                                    reserved_word[w] = ord(reserved_word[w])
                                deletable_array.extend(reserved_word)

                    else:
                        deletable_array.append(reserved_word)
                        reserved_word = ""

            else:
                tokens = []
                token_actual = ""

                for char in definition:

                    if "]" in token_actual:
                        word = ""
                        array = []
                        array.append("(")

                        token_actual = token_actual[1:-1]

                        for tok in token_actual:
                            word += tok
                            if word.count("'") == 2:
                                word = ord(word[1:-1])
                                array.append(word)
                                array.append("|")
                                word = ""
                        array[len(array) - 1] = ")"
                        tokens.extend(array)
                        token_actual = ""

                    if token_actual.count("'") == 2:
                        if "[" not in token_actual:
                            token_actual = token_actual[1:-1]
                            tokens.append(token_actual)
                            token_actual = ""

                    if char in ("(", ")", "*", "?", "+", "|", "."):
                        if "'" not in token_actual:
                            if token_actual:
                                if len(token_actual) == 1:
                                    token_actual = ord(token_actual)
                                tokens.append(token_actual)
                                token_actual = ""
                            tokens.append(char)
                        else:
                            token_actual += char
                    else:
                        token_actual += char

                if token_actual:
                    tokens.append(token_actual)

                deletable_array.extend(tokens)

            temp_expression.append(deletable_array)
            clean_functions.append(temp_expression)

        # Se agrega la concatenacion a las funciones de la gramatica
        for x in range(len(clean_functions)):
            isFunc = True

            # Se revisa si la expresion en cuestion es un entero (int)
            for c in ["+", "*", "(", ")", "?", "|"]:
                if c in clean_functions[x][1]:
                    isFunc = False

            if isFunc == False:
                # Se revisa si la expresion posee el token .

                # Se comienza con el proceso de concatenacion
                temp_expression = []
                for y in clean_functions[x][1]:
                    temp_expression.append(y)
                    temp_expression.append(".")
                # Se elimina cualquier concatenacion no deseada
                for z in range(len(temp_expression)):
                    if temp_expression[z] == "(":
                        if temp_expression[z + 1] == ".":
                            temp_expression[z + 1] = ""
                    if temp_expression[z] == ")":
                        if temp_expression[z - 1] == ".":
                            temp_expression[z - 1] = ""
                    if temp_expression[z] == "*":
                        if temp_expression[z - 1] == ".":
                            temp_expression[z - 1] = ""
                    if temp_expression[z] == "|":
                        if temp_expression[z - 1] == ".":
                            temp_expression[z - 1] = ""
                        if temp_expression[z + 1] == ".":
                            temp_expression[z + 1] = ""
                    if temp_expression[z] == "+":
                        if temp_expression[z - 1] == ".":
                            temp_expression[z - 1] = ""
                    if temp_expression[z] == "?":
                        if temp_expression[z - 1] == ".":
                            temp_expression[z - 1] = ""
                temp_expression = [
                    element for element in temp_expression if element != ""
                ]

                clean_functions[x][1] = temp_expression[:-1]

            else:
                # Se revisa la expresion para ver si posee el token -
                ascii_array = []
                newString_Array = []
                if "-" in clean_functions[x][1]:
                    for z in range(len(clean_functions[x][1])):
                        if clean_functions[x][1][z] == "-":
                            for i in range(
                                clean_functions[x][1][z - 1],
                                clean_functions[x][1][z + 1] + 1,
                            ):
                                ascii_array.append(i)
                    # convertir el ascii en string otra vez, en este caso lo dejo como ascii
                    for i in ascii_array:
                        newString_Array.append(i)
                    # reemplazarlo en su respectiva posicion
                    clean_functions[x][1] = newString_Array

                # Se añaden los | en cada uno
                newString_Array = []
                for y in clean_functions[x][1]:
                    newString_Array.append(y)
                    newString_Array.append("|")

                newString_Array = newString_Array[:-1]
                clean_functions[x][1] = newString_Array

        # Se agregan los parentesis () al final y inicial
        for func in clean_functions:
            func[1] = ["("] + func[1] + [")"]

        functionNames = [x[0] for x in clean_functions] + ["|"]
        clean_regex_expression = [
            ord(x) if len(x) == 1 and x not in functionNames else x
            for x in clean_regex_expression
        ]

        # Se agregan los #
        temporalNewRegex = []
        for x in clean_regex_expression:
            if x != "|":
                temporalNewRegex.append("(")
                temporalNewRegex.append(x)
                temporalNewRegex.append(".")
                temporalNewRegex.append("#" + str(x))
                temporalNewRegex.append(")")
            else:
                temporalNewRegex.append(x)

        clean_regex_expression = temporalNewRegex

        def replace_regex(regex, functions):
            final_regex = []
            for r in regex:
                if r in functions:
                    final_regex.extend(replace_regex(functions[r], functions))
                else:
                    final_regex.append(r)
            return final_regex

        final_regex = replace_regex(clean_regex_expression, dict(clean_functions))

        return final_regex

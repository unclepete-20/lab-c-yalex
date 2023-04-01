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

        # lista donde se guardarán todas las functions "let"
        functions = []

        # lista donde se guardarán todas las functions en un formato mas limpio
        clean_functions = []

        # aqui se guardaran las expresiones regulares
        regex = []
        clean_regex = []

        # para guardar las palabras y ver que se hara con ello segun la funcion que tengan
        word = ""

        # leer el archivo
        with open(self.yal, "r") as yal:
            lines = yal.readlines()

        active_elements = False

        # obtener los elementos
        for line in lines:
            # obtener los tokens
            if active_elements:
                temporary_word = ""
                for x in line:
                    if x != " ":
                        if x != "\n":
                            if x != "'":
                                temporary_word += x
                            if x == "|":
                                regex.append(temporary_word)
                                temporary_word = ""
                        else:
                            regex.append(temporary_word)
            # obtener todas sus functions
            if line.startswith("let"):
                functions.append(line[4:-1])
            # activar lo de tokens
            if line.startswith("rule"):
                active_elements = True

        # realizar limpieza de los datos de regex
        for i in range(len(regex)):
            index_bracket = regex[i].find("{")
            index_comment = regex[i].find("(*")
            if index_bracket != -1 and (
                index_bracket < index_comment or index_comment == -1
            ):
                regex[i] = regex[i][:index_bracket]
            elif index_comment != -1 and (
                index_comment < index_bracket or index_bracket == -1
            ):
                regex[i] = regex[i][:index_comment]

        clean_regex = [
            x[1:-1] if len(x) != 0 and x.count('"') == 2 else x for x in regex
        ]

        # limpieza de los datos de functions

        for f in functions:

            del_array = []

            temp_array = []

            nombre, definicion = f.split("=")

            nombre = nombre.strip()

            definicion = definicion.strip()

            temp_array.append(nombre)

            if definicion[0] == "[":
                definicion = definicion[1:-1]
                word = ""
                for x in definicion:
                    word += x
                    if word[0] in ("'", '"'):
                        if word.count(word[0]) == 2:
                            word = word[1:-1]
                            del_array.append(
                                ord(word)
                                if len(word) == 1
                                else bytes(word, "utf-8").decode("unicode_escape")
                            )
                            word = ""
                    else:
                        del_array.append(word)
                        word = ""
            else:
                tokens = []
                token_actual = ""
                for caracter in definicion:
                    if "]" in token_actual:
                        palabra = ""
                        array = ["("]
                        token_actual = token_actual[1:-1]
                        for tok in token_actual:
                            palabra += tok
                            if palabra.count("'") == 2:
                                palabra = ord(palabra[1:-1])
                                array.extend([palabra, "|"])
                                palabra = ""
                        array[-1] = ")"
                        tokens.extend(array)
                        token_actual = ""
                    if token_actual.count("'") == 2:
                        if "[" not in token_actual:
                            token_actual = token_actual[1:-1]
                            tokens.append(token_actual)
                            token_actual = ""
                    if caracter in ("(", ")", "*", "?", "+", "|", "."):
                        if "'" not in token_actual:
                            if token_actual:
                                tokens.append(
                                    ord(token_actual[0])
                                    if len(token_actual) == 1
                                    else token_actual
                                )
                                token_actual = ""
                            tokens.append(caracter)
                        else:
                            token_actual += caracter
                    else:
                        token_actual += caracter
                if token_actual:
                    tokens.append(token_actual)
                del_array.extend(tokens)

            temp_array.append(del_array)
            clean_functions.append(temp_array)

        # Se le agrega la concatenacion a las funciones
        for x in range(len(clean_functions)):
            isFunc = True

            # Se revisa si posee un entero dentro de la gramatica
            for c in ["+", "*", "(", ")", "?", "|"]:
                if c in clean_functions[x][1]:
                    isFunc = False

            if isFunc == False:

                # Se comienza con el proceso de concatenacion
                temp_array = []
                for y in clean_functions[x][1]:
                    temp_array.append(y)
                    temp_array.append(".")
                # A continuacion se elimina cualquier concatenacion innecesaria.
                for z in range(len(temp_array)):
                    if temp_array[z] == "(":
                        if temp_array[z + 1] == ".":
                            temp_array[z + 1] = ""
                    if temp_array[z] == ")":
                        if temp_array[z - 1] == ".":
                            temp_array[z - 1] = ""
                    if temp_array[z] == "*":
                        if temp_array[z - 1] == ".":
                            temp_array[z - 1] = ""
                    if temp_array[z] == "|":
                        if temp_array[z - 1] == ".":
                            temp_array[z - 1] = ""
                        if temp_array[z + 1] == ".":
                            temp_array[z + 1] = ""
                    if temp_array[z] == "+":
                        if temp_array[z - 1] == ".":
                            temp_array[z - 1] = ""
                    if temp_array[z] == "?":
                        if temp_array[z - 1] == ".":
                            temp_array[z - 1] = ""
                temp_array = [element for element in temp_array if element != ""]

                clean_functions[x][1] = temp_array[:-1]

            else:
                # Se revisa para ver si posee el simbolo -
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
                    for i in ascii_array:
                        newString_Array.append(i)
                    # reemplazarlo en su respectiva posicion
                    clean_functions[x][1] = newString_Array

                # añadir los | en cada uno
                newString_Array = []
                for y in clean_functions[x][1]:
                    newString_Array.append(y)
                    newString_Array.append("|")

                newString_Array = newString_Array[:-1]
                clean_functions[x][1] = newString_Array

        for func in clean_functions:
            func[1] = ["("] + func[1] + [")"]

        # convertilos en ascii solo aquellos que no forman parte de alguna funcion
        functionNames = []
        # obtener los nombres de las functions
        for x in clean_functions:
            functionNames.append(x[0])
        functionNames.append("|")
        for x in range(len(clean_regex)):
            if clean_regex[x] not in functionNames:
                if len(clean_regex[x]) == 1:
                    clean_regex[x] = ord(clean_regex[x])

        # agregar los #
        temporalNewRegex = []
        for x in clean_regex:
            if x != "|":
                temporalNewRegex.append("(")
                temporalNewRegex.append(x)
                temporalNewRegex.append(".")
                temporalNewRegex.append("#" + str(x))
                temporalNewRegex.append(")")
            else:
                temporalNewRegex.append(x)

        clean_regex = temporalNewRegex

        # comenzar a reemplazar la regex
        final_regex = []
        for reg in clean_regex:
            found = False
            # si la regex found en las functions
            for func in clean_functions:
                if reg == func[0]:
                    found = True
                    # este sera en el que tendra todos los cambios y por el cual se cambiara
                    regex_temp = []
                    regex_temp.extend(func[1])
                    # seguir revisando si en el regex temporal si dentro de el aun found valores que pertenecen a las funcioens hasta que ya ninguno no tenga mas
                    length = 0
                    while length != len(regex_temp):

                        length = len(regex_temp)
                        i = 0
                        regex_test = []
                        while i < len(regex_temp):
                            n_found = False
                            for x in clean_functions:
                                if regex_temp[i] == x[0]:
                                    n_found = True
                                    regex_test.extend(x[1])
                                    regex_test.extend(regex_temp[i + 1 :])
                                    regex_temp = regex_test
                                    i = len(regex_temp)
                                    regex_test = []
                                    break

                            if n_found == False:
                                regex_test.append(regex_temp[i])
                                i += 1

                    final_regex.extend(regex_temp)
            # si la regex no found en las functions solo agregarlo
            if found == False:
                final_regex.append(reg)

        return final_regex

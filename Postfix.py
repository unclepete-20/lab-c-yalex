# -*-coding:utf-8 -*-
"""
@File    :   Postfix.py
@Date    :   2023/04/01
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Implementacion de caracteristicas de un Regex y funcionalidad Postfix.
"""

class Postfix(object):
    PIPE = '|'
    STAR = '*'
    PLUS = '+'
    QUESTION = '?'
    CONCAT = '•'
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    OPERATORS = {PIPE: 1, CONCAT: 2, QUESTION: 3, STAR: 3, PLUS: 3}

    def __init__(self, regex):
        self.regex = regex
        self.stack = []
        self.output = []

    def shunting_yard(self):
        for token in self.regex:
            if token in self.OPERATORS:
                while self.stack and self.stack[-1] != self.LEFT_PAREN and self.OPERATORS[token] <= self.OPERATORS.get(self.stack[-1], 0):
                    self.output.append(self.stack.pop())
                self.stack.append(token)
            elif token == self.LEFT_PAREN:
                self.stack.append(token)
            elif token == self.RIGHT_PAREN:
                while self.stack and self.stack[-1] != self.LEFT_PAREN:
                    self.output.append(self.stack.pop())
                if self.stack and self.stack[-1] == self.LEFT_PAREN:
                    self.stack.pop()
            else:
                self.output.append(token)

        while self.stack:
            self.output.append(self.stack.pop())

        return self.output
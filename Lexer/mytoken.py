from enum import Enum
import string

class Tokens(Enum):
    #types
    INT = 'INT'
    BOOL = 'BOOL'
    #arithmetics
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    IDIV = '//'
    MOD = '%'
    #logical
    OR = '||'
    AND = '&&'
    NOT = '!'
    EQUEL = '='
    NEQUEL = '!='
    LESS = '<'
    LESSE = '<='
    GREATER = '>'
    GREATERE = '>='
    #brackets
    LPAREN = '('
    RPAREN = ')'
    LBRCE = '{'
    RBRCE = '}'
    #other
    DIGITS = '0123456789'
    LETTERS = string.ascii_letters

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
    
    def __repr__(self):
        if self.value:
            return f"{self.type}: '{self.value}'"
        return f"{self.type}"
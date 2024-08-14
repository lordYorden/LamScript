from enum import Enum
import string

class Tokens:
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
    EQUEL = '=='
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
    #boolean 
    TRUE = 'true'
    FALSE = 'false'
    #other
    DIGITS = '0123456789'
    LETTERS = string.ascii_letters
    ASSIGN = '='
    EOF = 'EOF'
    WHITESPACE = ' \t'

class Token:
    def __init__(self, type, value=None, pos_start=None, pos_end=None):
        self.type = type
        self.value = value
        
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        
        if pos_end:
            self.pos_end = pos_end.copy()
    
    def __repr__(self):
        if self.value:
            return f"{self.type}: '{self.value}'"
        return f"{self.type}"
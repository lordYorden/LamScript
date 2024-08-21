from enum import Enum
import string

class Tokens:
    """Class that contains all the tokens that the lexer can understand."""
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
    BOOLEANS = [TRUE,FALSE]
    #other
    DIGITS = '0123456789'
    LETTERS = string.ascii_letters
    LETTERS_DIGITS = LETTERS + DIGITS
    ASSIGN = '='
    EOF = 'EOF'
    WHILE = 'while'
    DEF = 'def'
    LITE = 'lite'
    KEYWORD = 'KEYWORD'
    IDENTIFIER = 'IDENTIFIER'
    RETURN = 'return'
    BREAK = 'break'
    CONTINUE = 'continue'
    KEYWORDS = [WHILE, DEF, LITE, RETURN, BREAK, CONTINUE]
    COMMA = ','
    NEWLINE = 'NEWLINE'

class Token:
    def __init__(self, type, value=None, pos_start=None, pos_end=None):
        """Initializes the Token class.

        Args:
            type (character): The type of token.
            value (int, None): The value of the token. Defaults to None.
            pos_start (position, None): The start posithion of the object. Defaults to None.
            pos_end (position, None):The end posithion of the object. Defaults to None.
        """
        self.type = type
        self.value = value
        
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        
        if pos_end:
            self.pos_end = pos_end.copy()
            
    def matches(self, type_, value):
        """Check if the token matches the given type and value.

        Args:
            type_ (character): The type of the token.
            value (int): The value of the token.

        Returns:
            boolean: True if the token matches the given type and value, False otherwise.
        """
        return self.type == type_ and self.value == value
    
    def __repr__(self):
        """Return the string representation of the token.

        Returns:
            string: the string representation of the token.
        """
        if self.value:
            return f"{self.type}: '{self.value}'"
        return f"{self.type}"
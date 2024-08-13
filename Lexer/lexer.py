from Lexer.mytoken import Token, Tokens
from Lexer.myerror import Position, IllegalCharacterError

# Token = token.Token
# Tokens = token.Tokens
# Position = myerror.Position
# IllegalCharacterError = myerror.IllegalCharacterError
DIGITS = '0123456789'

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance()
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None
    
    def make_tokens(self):
        tokens = []
        
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            # elif self.current_char in Tokens.LETTERS:
            #     tokens.append(self.make_word())
            elif self.current_char == '+':
                tokens.append(Token(Tokens.ADD))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(Tokens.SUB))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(Tokens.MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(self.make_whole_div())
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(Tokens.MOD))
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token(self.make_equel(Tokens.EQUEL,Tokens.ASSIGN)))
                self.advance()
            elif self.current_char == '!':
                tokens.append(Token(self.make_equel(Tokens.NEQUEL,Tokens.NOT)))
                self.advance()
            elif self.current_char == '<':
                tokens.append(Token(self.make_equel(Tokens.LESSE,Tokens.LESS)))
                self.advance()
            elif self.current_char == '>':
                tokens.append(Token(self.make_equel(Tokens.GREATERE,Tokens.GREATER)))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(Tokens.LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(Tokens.RPAREN))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(Tokens.LBRCE))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(Tokens.RBRCE))
                self.advance()
            else:
                start_pos = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharacterError(start_pos, self.pos, "'" + char + "'")
                       
        return tokens,None
    
    def make_number(self):
        num_str = ''
        
        while self.current_char != None and self.current_char in DIGITS:
            num_str += self.current_char
            self.advance()
            
        return Token(Tokens.INT, int(num_str))
    
    def make_whole_div(self):
        self.advance()
        if self.current_char == '/':
            return Token(Tokens.IDIV)
        return Token(Tokens.DIV)
    
    def make_equel(self, equel_token,alternative_token):
        self.advance()
        if self.current_char == '=':
            return Token(equel_token)
        return Token(alternative_token)
    

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    return tokens, error
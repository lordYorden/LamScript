from Lexer.mytoken import Token, Tokens
from Lexer.myerror import Position, IllegalCharacterError

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
            elif self.current_char in Tokens.DIGITS.value:
                tokens.append(self.make_number())
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
            # elif self.current_char == 't':
            #     tokens.append(self.make_boolean())
            #     self.advance()
            # elif self.current_char == 'f':
            #     tokens.append(self.make_boolean())
            #     self.advance()
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
                       
        tokens.append(Token(Tokens.EOF))               
        return tokens,None
    
    def make_number(self):
        num_str = ''
        
        while self.current_char != None and self.current_char in Tokens.DIGITS.value:
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
    
    #possible implementation of boolean
    def make_boolean(self):
        bool_str = ''
        
        if self.current_char == 't':
            for i in range(4):
                bool_str += self.current_char
                self.advance()
                if self.current_char == None or self.current_char not in Tokens.TRUE.value:
                    break
            if bool_str == 'true':
                return Token(Tokens.BOOL, True)

        elif self.current_char == 'f':
            for i in range(5):
                bool_str += self.current_char
                self.advance()
                if self.current_char == None or self.current_char not in Tokens.FALSE.value:
                    break
            if bool_str == 'false':
                return Token(Tokens.BOOL, False)
        return None

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    return tokens, error
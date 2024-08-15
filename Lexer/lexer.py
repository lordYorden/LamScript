from Lexer.mytoken import Token, Tokens
from Lexer.myerror import Position, IllegalCharacterError, ExpectedCharError

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
        
    def backtrack(self):
        self.pos.backtrack()
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None
    
    def make_tokens(self):
        tokens = []
        
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in Tokens.DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(Tokens.ADD, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(Tokens.SUB, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(Tokens.MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(self.make_whole_div())
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(Tokens.MOD, pos_start=self.pos))
                self.advance()
            elif self.current_char == '=':
                tokens.append(self.make_equel(Tokens.EQUEL,Tokens.ASSIGN))
                self.advance()
            elif self.current_char == '!':
                tokens.append(self.make_equel(Tokens.NEQUEL,Tokens.NOT))
                self.advance()
            elif self.current_char == '<':
                tokens.append(self.make_equel(Tokens.LESSE,Tokens.LESS))
                self.advance()
            elif self.current_char == '>':
                tokens.append(self.make_equel(Tokens.GREATERE,Tokens.GREATER))
                self.advance()
            elif self.current_char == 't' or self.current_char == 'f':
                tok, error = self.make_boolean()
                if error:
                    return [], error
                tokens.append(tok)
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(Tokens.LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(Tokens.RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '|':
                tok, error = self.make_or()
                if error:
                    return [], error
                tokens.append(tok)
                self.advance()
            elif self.current_char == '&':
                tok, error = self.make_and()
                if error:
                    return [], error
                tokens.append(tok)
                self.advance()
            # elif self.current_char == '{':
            #     tokens.append(Token(Tokens.LBRCE))
            #     self.advance()
            # elif self.current_char == '}':
            #     tokens.append(Token(Tokens.RBRCE))
            #     self.advance()
            else:
                start_pos = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharacterError(start_pos, self.pos, "'" + char + "'")
                       
        tokens.append(Token(Tokens.EOF, pos_start=self.pos))               
        return tokens,None
    
    def make_number(self):
        num_str = ''
        pos_start = self.pos.copy()
        
        while self.current_char != None and self.current_char in Tokens.DIGITS:
            num_str += self.current_char
            self.advance()
            
        return Token(Tokens.INT, int(num_str), pos_start=pos_start, pos_end=self.pos)
    
    def make_whole_div(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '/':
            return Token(Tokens.IDIV, pos_start=pos_start, pos_end=self.pos)
        self.backtrack()
        return Token(Tokens.DIV, pos_start=pos_start)
    
    def make_or(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '|':
            return Token(Tokens.OR, pos_start=pos_start), None
        else:
            return None, ExpectedCharError(pos_start, self.pos, "'|'")
    
    def make_and(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '&':
            return Token(Tokens.AND, pos_start=pos_start), None
        else:
            return None, ExpectedCharError(pos_start, self.pos, "'&'")
    
    def make_equel(self, equel_token,alternative_token):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            return Token(equel_token, pos_start=pos_start)
        self.backtrack()
        return Token(alternative_token, pos_start=pos_start)
    
    #possible implementation of boolean
    def make_boolean(self):
        bool_str = ''
        pos_start = self.pos.copy()
        
        if self.current_char == 't':
            for i in range(4):
                bool_str += self.current_char
                self.advance()
                if self.current_char == None or self.current_char not in Tokens.TRUE:
                    break
            if bool_str == 'true':
                self.backtrack()
                return Token(Tokens.BOOL, True, pos_start=pos_start, pos_end=self.pos), None

        elif self.current_char == 'f':
            for i in range(5):
                bool_str += self.current_char
                self.advance()
                if self.current_char == None or self.current_char not in Tokens.FALSE:
                    break
            if bool_str == 'false':
                self.backtrack()
                return Token(Tokens.BOOL, False, pos_start=pos_start, pos_end=self.pos), None
             
        return None, IllegalCharacterError(pos_start, self.pos, "'" + bool_str + "'")
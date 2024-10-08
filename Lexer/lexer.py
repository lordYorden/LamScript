from Lexer.Tokens import Token, Tokens
from Error.Error import Position, IllegalCharacterError, ExpectedCharError

class Lexer:
    def __init__(self, fn, text):
        """The lexer class is responsible for converting the input text 
           into tokens that the parser can understand.

        Args:
            fn (string): name of the file
            text (string): file text
        """
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        """Move the position of the current character by one character"""
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None
        
    def backtrack(self):
        """Move the position of the current character back by one character"""
        self.pos.backtrack()
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None
    
    def make_tokens(self):
        """Convert the input text into tokens that the parser can understand.

        Returns:
            token, None: list of tokens and no error
        """
        tokens = []
        
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in ';\n':
                tokens.append(Token(Tokens.NEWLINE, pos_start=self.pos))
                self.advance()
            elif self.current_char == '#':
                self.ignore_comments()
            elif self.current_char in Tokens.DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in Tokens.LETTERS:
                tok = self.make_keyword_bool_identifier()
                tokens.append(tok)
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
            elif self.current_char == ',':
                tokens.append(Token(Tokens.COMMA, pos_start=self.pos))
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
            elif self.current_char == '{':
                tokens.append(Token(Tokens.LBRCE, pos_start=self.pos))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(Tokens.RBRCE, pos_start=self.pos))
                self.advance()
            else:
                start_pos = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharacterError(start_pos, self.pos, "'" + char + "'")
                       
        tokens.append(Token(Tokens.EOF, pos_start=self.pos))               
        return tokens,None
    
    def make_number(self):
        """Convert the input text into a number token.

        Returns:
            token: number token with the value of the number
        """
        num_str = ''
        pos_start = self.pos.copy()
        
        while self.current_char != None and self.current_char in Tokens.DIGITS:
            num_str += self.current_char
            self.advance()
            
        return Token(Tokens.INT, int(num_str), pos_start=pos_start, pos_end=self.pos)
    
    def make_whole_div(self):
        """check if the current character is a division token.

        Returns:
            token: division token 
        """
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '/':
            return Token(Tokens.IDIV, pos_start=pos_start, pos_end=self.pos)
        self.backtrack()
        return Token(Tokens.DIV, pos_start=pos_start)
    
    def make_or(self):
        """check if the current character is a or token.

        Returns:
            token: or token 
        """
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '|':
            return Token(Tokens.OR, pos_start=pos_start), None
        else:
            return None, ExpectedCharError(pos_start, self.pos, "'|'")
    
    def make_and(self):
        """check if the current character is a and token.

        Returns:
            token: and token
        """
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '&':
            return Token(Tokens.AND, pos_start=pos_start), None
        else:
            return None, ExpectedCharError(pos_start, self.pos, "'&'")
    
    def make_equel(self, equel_token,alternative_token):
        """check if the current character is a equel token.

        Args:
            equel_token (character): the equel token
            alternative_token (character): the alternative token

        Returns:
            token: equel token or alternative token
        """
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            return Token(equel_token, pos_start=pos_start)
        self.backtrack()
        return Token(alternative_token, pos_start=pos_start)
    
    def make_keyword_bool_identifier(self):
        """Convert the input text into a keyword, boolean or identifier token.

        Returns:
            token: keyword, boolean or identifier token
        """
        key_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in Tokens.LETTERS_DIGITS + '_':
            key_str += self.current_char
            self.advance()
            
        key_str = key_str.lower()
        if key_str in Tokens.KEYWORDS:
            tok_type = Tokens.KEYWORD
            return Token(tok_type, key_str, pos_start, self.pos)
        elif key_str in Tokens.BOOLEANS:
            tok_type = Tokens.BOOL
            if key_str == 'true':
                return Token(tok_type, True, pos_start, self.pos)
            elif key_str == 'false':
                return Token(tok_type, False, pos_start, self.pos)

        return Token(Tokens.IDENTIFIER, key_str, pos_start, self.pos)
    
    def ignore_comments(self):
        """Ignore comments in the input text."""
        self.advance()
        while self.current_char != '\n':
            self.advance()
        self.advance()
        
    
    #deprecated
    def make_boolean(self):
        """check if the current character is a boolean token.

        Returns:
            token: boolean token or None and an error
        """
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
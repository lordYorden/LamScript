from Parser.node import NumberNode, BinOpNode, UnaryOpNode, BooleanNode, whileNode ,SymbolAcsessNode , FuncDefNode , FuncCallNode
from Lexer.Tokens import Tokens, Token
from Error.Error import InvalidSyntaxError
from Parser.ParseResult import ParseResult

class Parser:
    parenthesis = (Tokens.LPAREN, Tokens.RPAREN)
    math_low_order_ops = (Tokens.ADD, Tokens.SUB)
    math_high_order_ops = (Tokens.MUL, Tokens.DIV, Tokens.IDIV, Tokens.MOD)
    bool_low_order_ops = (Tokens.OR, Tokens.AND)
    equel_ops = (Tokens.EQUEL, Tokens.NEQUEL)
    comparisson_ops = (Tokens.LESS, Tokens.LESSE, Tokens.GREATER, Tokens.GREATERE, Tokens.EQUEL, Tokens.NEQUEL)
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()
        
    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token
    
    def parse(self):
        res = self.bool_expr()
        if not res.error and self.current_token.type != Tokens.EOF:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, "Unkonwn operation for type"))
        return res
    
    def bool_expr(self):
        return self.bin_op(self.bool_term, self.bool_low_order_ops)
    
    def bool_term(self):
        return self.bin_op(self.bool_factor, self.equel_ops)
    
    def bool_factor(self):
        res = ParseResult()
        tok = self.current_token
        
        if tok.type == Tokens.BOOL:
            res.register_advancement()
            self.advance()
            return res.success(BooleanNode(tok))
        elif tok.type == Tokens.NOT:
            res.register_advancement()
            self.advance()
            factor = res.register(self.bool_factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        else:
            comp = res.register(self.comparisson_expr())
            if res.error: return res
            return res.success(comp)
    
    def comparisson_expr(self): 
        return self.bin_op(self.math_expr, self.comparisson_ops)
    
    def math_expr(self):
        return self.bin_op(self.math_term, self.math_low_order_ops)
    
    def math_term(self):
        return self.bin_op(self.math_factor, self.math_high_order_ops)
    
    def math_factor(self):
        res = ParseResult()
        tok = self.current_token
        if tok.type in self.math_low_order_ops:
            res.register_advancement()
            self.advance()
            factor = res.register(self.math_factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        else:
            call = res.register(self.call())
            if res.error: return res
            return res.success(call)
       
    def identifer(self):
        res = ParseResult()
        tok = self.current_token
        if tok.type == Tokens.IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(SymbolAcsessNode(tok))
        return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected 'IDENTIFIER'")) 
        
    def atom(self):
        res = ParseResult()
        tok = self.current_token
        if tok.type == Tokens.INT:
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))
        elif tok.type == Tokens.IDENTIFIER:
            id = res.register(self.identifer())
            if res.error: return res
            return res.success(id)
        elif tok.type == Tokens.LPAREN:
            return self.parentized_expr()
        elif tok.matches(Tokens.KEYWORD, Tokens.WHILE):
            #res.register_advancement()
            expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(expr)
        elif tok.matches(Tokens.KEYWORD, Tokens.DEF) or tok.matches(Tokens.KEYWORD, Tokens.LITE):
            expr = res.register(self.function_def())
            if res.error: return res
            return res.success(expr)
            
        return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected '(, int, or while, def or lite'"))
    
    def parentized_expr(self):
        res = ParseResult()
        tok = self.current_token
        res.register_advancement()
        self.advance()
        expr = res.register(self.bool_expr())
        if res.error: return res
        
        if self.current_token.type == Tokens.RPAREN:
            res.register_advancement()
            self.advance()
            return res.success(expr)
        else:
            return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected ')'"))
         
    def while_expr(self):
        res = ParseResult()
        tok = self.current_token
            
        res.register_advancement() 
        self.advance()
        if self.current_token.type == Tokens.LPAREN:
            condition = res.register(self.parentized_expr())
            if res.error: return res
        
        if self.current_token.type == Tokens.LBRCE:
            tok = self.current_token
            res.register_advancement()
            self.advance()

            body_nodes = []
            if self.current_token.type == Tokens.NEWLINE:
                res.register_advancement()
                self.advance()
                body_nodes =  res.register(self.staments())
                if res.error: return res
            else:
                expr = res.register(self.bool_expr())
                if res.error: return res
                body_nodes.append(expr)
            
            if self.current_token.type == Tokens.RBRCE:
                res.register_advancement()
                self.advance()
                return res.success(whileNode(condition, body_nodes))
            else:
                return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected '}'"))
        else:
            return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected '{'"))
    
    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res
        
        while self.current_token.type in ops:
            op_tok = self.current_token
            res.register_advancement()
            self.advance()
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)
        return res.success(left)
    
    def parameters(self):
        res = ParseResult()
        # res.register_advancement()
        # self.advance()
        more_then_one = False
        parameters = []
        
        id = res.register(self.identifer())
        if res.error: return res
        parameters.append(id)
        
        if self.current_token.type == Tokens.COMMA:
            more_then_one = True
            res.register_advancement()
            self.advance()
            
        while more_then_one:
            id = res.register(self.identifer())
            if res.error: return res
            parameters.append(id)
            
            if self.current_token.type != Tokens.COMMA:
                more_then_one = False
            else:
                res.register_advancement()
                self.advance()
                
        return res.success(parameters)
            
    def arguments(self):
        res = ParseResult()
        # res.register_advancement()
        # self.advance()
        more_then_one = False
        arguments = []
        
        arg = res.register(self.bool_expr())
        if res.error: return res
        arguments.append(arg)
        
        if self.current_token.type == Tokens.COMMA:
            more_then_one = True
            res.register_advancement()
            self.advance()
            
        while more_then_one:
            arg = res.register(self.bool_expr())
            if res.error: return res
            arguments.append(arg)
            
            if self.current_token.type != Tokens.COMMA:
                more_then_one = False
            else:
                res.register_advancement()
                self.advance()
                
        return res.success(arguments)
  

    def function_def(self):
        res = ParseResult()
        tok = self.current_token
        if tok.matches(Tokens.KEYWORD , Tokens.DEF):
            res.register_advancement()
            self.advance()
            id = res.register(self.identifer())
            if res.error: return res
            if self.current_token.type == Tokens.LPAREN:
                tok = self.current_token
                res.register_advancement()
                self.advance()

                params = []
                if  self.current_token.type == Tokens.IDENTIFIER:
                    params = res.register(self.parameters())
                    if res.error: return res

                if self.current_token.type == Tokens.RPAREN:
                    self.advance()
                    res.register_advancement()

                    if self.current_token.type == Tokens.LBRCE:
                        tok = self.current_token
                        res.register_advancement()
                        self.advance()
                       
                        body_nodes = []
                        if self.current_token.type == Tokens.NEWLINE:
                            res.register_advancement()
                            self.advance()
                            body_nodes =  res.register(self.staments())
                            if res.error: return res
                        else:
                            expr = res.register(self.bool_expr())
                            if res.error: return res
                            body_nodes.append(expr)

                        if self.current_token.type == Tokens.RBRCE:
                            res.register_advancement()
                            self.advance()
                            return res.success(FuncDefNode(id, params, body_nodes))
                        else:
                            return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected '}'"))
                    else:
                        return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected '{'"))
                else:
                    return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected ')'"))
            else:
                return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected '('"))

        elif tok.matches(Tokens.KEYWORD , Tokens.LITE): 
            res.register_advancement()
            self.advance()
            if self.current_token.type == Tokens.LPAREN:
                tok = self.current_token
                res.register_advancement()
                self.advance()
                params = None
                if  self.current_token.type == Tokens.IDENTIFIER:
                    params = res.register(self.parameters())
                    if res.error: return res
                    if self.current_token.type == Tokens.RPAREN:
                        self.advance()
                        res.register_advancement()

                        body = res.register(self.bool_expr())
                        if res.error: return res
                        return res.success(FuncDefNode(None, params, body))
                    else:
                        return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected ')'"))  
            else:
                return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected '('"))
        else:
            return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected 'def' or 'lite'"))
                    
    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error: return res
        if self.current_token.type == Tokens.LPAREN:
            self.advance()
            res.register_advancement()
            if self.current_token.type == Tokens.RPAREN:
                self.advance()
                res.register_advancement()
                return res.success(FuncCallNode(atom, []))
            else:
                tok = self.current_token
                # res.register_advancement()
                # self.advance()
                arg = res.register(self.arguments())
                if res.error:return res
                if self.current_token.type == Tokens.RPAREN:
                    self.advance()
                    res.register_advancement()
                    return res.success(FuncCallNode(atom, arg))
                else:
                    return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected ')'"))
        return res.success(atom)
            
    def staments(self):
        res = ParseResult()
        staments = []
        pos_start = self.current_token.pos_start.copy()
        
        while self.current_token.type == Tokens.NEWLINE:
            res.register_advancement()
            self.advance()
            
        stament = res.register(self.bool_expr())
        if res.error: return res
        staments.append(stament)
        
        while self.current_token.type == Tokens.NEWLINE:
            res.register_advancement()
            self.advance()
            
            if self.current_token.type == Tokens.RBRCE:
                break
            
            stament = res.register(self.bool_expr())
            if res.error: return res
            staments.append(stament)
            
        return res.success(staments)



# class ParseResult:
    
#     def __init__(self):
#         self.error = None
#         self.node = None
#         self.advance_count = 0
    
#     def register(self, res):
#         self.advance_count += res.advance_count
#         if res.error: self.error = res.error
#         return res.node
    
#     def register_advancement(self):
#         self.advance_count += 1
#         return self
    
#     def success(self, node):
#         self.node = node
#         return self
    
#     def failure(self, error):
#         if not self.error or self.advance_count == 0:
#             self.error = error
#         return self
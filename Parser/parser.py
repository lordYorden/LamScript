from Parser.node import NumberNode, BinOpNode, UnaryOpNode, BooleanNode
from Lexer.mytoken import Tokens, Token
from Lexer.myerror import InvalidSyntaxError

class Parser:
    parenthesis = (Tokens.LPAREN, Tokens.RPAREN)
    math_low_order_ops = (Tokens.ADD, Tokens.SUB)
    math_high_order_ops = (Tokens.MUL, Tokens.DIV, Tokens.IDIV, Tokens.MOD)
    bool_low_order_pos = (Tokens.OR, Tokens.AND, Tokens.EQUEL, Tokens.NEQUEL)
    bool_high_order_ops = (Tokens.LESS, Tokens.LESSE, Tokens.GREATER, Tokens.GREATERE)
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()
        
    def parse(self):
        res = self.bool_expr()
        if not res.error and self.current_token.type != Tokens.EOF:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, "Expected '+', '-', '*', '/', '//' or '%'"))
        return res
    
    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token
    
    def math_factor(self):
        res = ParseResult()
        tok = self.current_token
        if tok.type in (Tokens.INT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        
        elif tok.type in self.math_low_order_ops:
            res.register(self.advance())
            factor = res.register(self.math_factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        
        elif tok.type == Tokens.LPAREN:
            res.register(self.advance())
            expr = res.register(self.math_expr())
            if res.error: return res
            if self.current_token.type == Tokens.RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected ')'"))
            
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int"))
        
    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res
        
        while self.current_token.type in ops:
            op_tok = self.current_token
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)
        return res.success(left)
        
    def math_term(self):
        return self.bin_op(self.math_factor, self.math_high_order_ops)

    def math_expr(self):
        return self.bin_op(self.math_term, self.math_low_order_ops)
    
    def bool_term(self):
        res = ParseResult()
        factor = res.register(self.bool_factor())
        if res.error: 
            return self.bin_op(self.math_expr, self.bool_high_order_ops)
        return res.success(factor)
        
    def bool_factor(self):
        res = ParseResult()
        tok = self.current_token
        
        if tok.type == Tokens.BOOL:
            res.register(self.advance())
            return res.success(BooleanNode(tok))
        elif tok.type == Tokens.NOT:
            res.register(self.advance())
            factor = res.register(self.bool_factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        elif tok.type == Tokens.LPAREN:
            res.register(self.advance())
            expr = res.register(self.bool_expr())
            if res.error: return res
            if self.current_token.type == Tokens.RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected ')'"))
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected bool or !"))
    
    def bool_expr(self):
        return self.bin_op(self.bool_term, self.bool_low_order_pos)
    
class ParseResult:
    
    
    def __init__(self):
        self.error = None
        self.node = None
    
    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
        return res
    
    def success(self, node):
        self.node = node
        return self
    
    def failure(self, error):
        self.error = error
        return self
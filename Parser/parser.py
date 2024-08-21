from Parser.node import NumberNode, BinOpNode, UnaryOpNode, BooleanNode, whileNode ,SymbolAcsessNode , FuncDefNode , FuncCallNode, ReturnNode, ContinueNode, BreakNode
from Lexer.Tokens import Tokens, Token
from Error.Error import InvalidSyntaxError
from Parser.ParseResult import ParseResult

class Parser:
    #define the order of operations
    parenthesis = (Tokens.LPAREN, Tokens.RPAREN)
    math_low_order_ops = (Tokens.ADD, Tokens.SUB)
    math_high_order_ops = (Tokens.MUL, Tokens.DIV, Tokens.IDIV, Tokens.MOD)
    bool_low_order_ops = (Tokens.OR, Tokens.AND)
    equel_ops = (Tokens.EQUEL, Tokens.NEQUEL)
    comparisson_ops = (Tokens.LESS, Tokens.LESSE, Tokens.GREATER, Tokens.GREATERE, Tokens.EQUEL, Tokens.NEQUEL)
    
    def __init__(self, tokens):
        """The parser class that follows the languege grammar.
        Layed out in grammer.txt

        Args:
            tokens (Token[]): The lexer tokens to parse.
        """
        self.tokens = tokens
        self.token_index = -1
        self.advance()
        self.isInsideLoop = False
        
    def advance(self):
        """Move the current token to the next token.

        Returns:
            Token: the next token.
        """
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token
    
    def parse(self):
        """Parse the tokens and return the Abstract Syntax Tree.

        Returns:
            ParseResult: the result of the parsing.
        """
        res = self.statements(False)
        if not res.error and self.current_token.type != Tokens.EOF:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, "Unkonwn operation for type"))
        return res
    
    def bool_expr(self):
        """Parse the boolean expression.

        Returns:
            ParseResult: the boolean expression syntax tree.
        """
        return self.bin_op(self.bool_term, self.bool_low_order_ops)
    
    def bool_term(self):
        """Parse the boolean term.

        Returns:
            ParseResult: the boolean term syntax tree.
        """
        return self.bin_op(self.bool_factor, self.equel_ops)
    
    def bool_factor(self):
        """Parse the boolean factor.

        Returns:
            ParseResult: the boolean factor syntax tree.
        """
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
        """Parse the comparisson expression.

        Returns:
            ParseResult: the comparisson expression syntax tree.
        """
        return self.bin_op(self.math_expr, self.comparisson_ops)
    
    def math_expr(self):
        """Parse the math expression.

        Returns:
            ParseResult: The math expression syntax tree.
        """
        return self.bin_op(self.math_term, self.math_low_order_ops)
    
    def math_term(self):
        """Parse the math term.

        Returns:
            ParseResult: The math term syntax tree.
        """
        return self.bin_op(self.math_factor, self.math_high_order_ops)
    
    def math_factor(self):
        """Parse the math factor.

        Returns:
            ParseResult: The math factor syntax tree.
        """
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
        """Parse the identifer expression.

        Returns:
            ParseResult: The identifer node (SymbolAcsessNode)
        """
        res = ParseResult()
        tok = self.current_token
        if tok.type == Tokens.IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(SymbolAcsessNode(tok))
        return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected 'IDENTIFIER'")) 
        
    def atom(self):
        """Parse the atom expression.

        Returns:
            ParseResult: the atom expression node (NumberNode, SymbolAcsessNode, or parentized expression)
        """
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
        """Parse the parentized expression.

        Returns:
            ParseResult: The parentized expression syntax tree.
        """
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
        """Parse the while expression.

        Returns:
            ParseResult: the while expression syntax tree.
        """
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
            self.isInsideLoop = True

            body_nodes = []
            if self.current_token.type == Tokens.NEWLINE:
                res.register_advancement()
                self.advance()
                body_nodes =  res.register(self.statements(False))
                if res.error: return res
            else:
                expr = res.register(self.statement(False))
                if res.error: return res
                body_nodes.append(expr)
            
            if self.current_token.type == Tokens.RBRCE:
                res.register_advancement()
                self.advance()
                self.isInsideLoop = False
                return res.success(whileNode(condition, body_nodes, self.current_token.pos_end))
            else:
                return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected '}'"))
        else:
            return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected '{'"))
    
    def bin_op(self, func, ops):
        """Parse the binary operation syntax.

        Args:
            func (method): the expression to parse.
            ops (Token[]): the operation tokens to parse.

        Returns:
            ParseResult: The binary operation syntax tree.
        """
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
        """Parse the function parameters.

        Returns:
            ParseResult: the function parameters (BaseNode[]).
        """
        res = ParseResult()
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
        """Parse the function arguments.

        Returns:
            ParseResult: the function arguments (BaseNode[]).
        """
        res = ParseResult()
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
        """Parse the function definition.

        Returns:
            ParseResult: the function definition syntax tree.
        """
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
                            body_nodes =  res.register(self.statements(True))
                            if res.error: return res
                        else:
                            expr = res.register(self.statement(True))
                            if res.error: return res
                            body_nodes.append(expr)

                        if self.current_token.type == Tokens.RBRCE:
                            res.register_advancement()
                            self.advance()
                            
                            return res.success(FuncDefNode(id, params, body_nodes, False, self.current_token.pos_end))
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
                #sets the identifier to none
                id = SymbolAcsessNode(Token(Tokens.IDENTIFIER, "none", tok.pos_start, tok.pos_end))
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

                        body = res.register(self.statement(False))
                        if res.error: return res

                        
                        return res.success(FuncDefNode(id, params, [body], True))
                    else:
                        return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected ')'"))  
            else:
                return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected '('"))
        else:
            return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected 'def' or 'lite'"))
                    
    def call(self):
        """Parse the function call.

        Returns:
           ParseResult: the function call syntax tree.
        """
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
                arg = res.register(self.arguments())
                if res.error:return res
                if self.current_token.type == Tokens.RPAREN:
                    self.advance()
                    res.register_advancement()
                    return res.success(FuncCallNode(atom, arg))
                else:
                    return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected ')'"))
        return res.success(atom)
            
    def statements(self, isInsideFunc):
        """Parse the multiple statements.

        Args:
            isInsideFunc (bool): check if the statement is inside a function.

        Returns:
            List: the list of statements (BaseNode[]).
        """
        res = ParseResult()
        statements = []
        pos_start = self.current_token.pos_start.copy()
        
        while self.current_token.type == Tokens.NEWLINE:
            res.register_advancement()
            self.advance()
            
        statement = res.register(self.statement(isInsideFunc))
        if res.error: return res
        statements.append(statement)
        
        while self.current_token.type == Tokens.NEWLINE:
            res.register_advancement()
            self.advance()
            
            while self.current_token.type == Tokens.NEWLINE:
                res.register_advancement()
                self.advance()
            
            if self.current_token.type == Tokens.RBRCE:
                break
            
            statement = res.register(self.statement(isInsideFunc))
            if res.error: return res
            statements.append(statement)
            
        while self.current_token.type == Tokens.NEWLINE:
                res.register_advancement()
                self.advance()
            
        return res.success(statements)

    def return_expr(self, isInsideFunc):
        """Parse the return expression syntax.

        Args:
            isInsideFunc (bool): check if the statement is inside a function.

        Returns:
            ParseResult: the return expression Node.
        """
        res = ParseResult()
        tok = self.current_token
        if tok.matches(Tokens.KEYWORD, Tokens.RETURN):
            res.register_advancement()
            self.advance()
            
            if self.current_token.type == Tokens.NEWLINE:
                if isInsideFunc:
                    return res.success(ReturnNode(None, tok.pos_start, tok.pos_end))
                else:
                    return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "return statement outside function"))
            else:
                expr = res.register(self.bool_expr())
                if res.error: return res
                
                if isInsideFunc:
                    return res.success(ReturnNode(expr, tok.pos_start, self.current_token.pos_end))
                else:
                    return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "return statement outside function"))
        else:
            return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected 'return'"))

    def continue_expr(self):
        """Parse the continue expression syntax.

        Returns:
            ParseResult: the continue expression Node.
        """
        res = ParseResult()
        tok = self.current_token
        if tok.matches(Tokens.KEYWORD, Tokens.CONTINUE):
            res.register_advancement()
            self.advance()
            if self.isInsideLoop:
                return res.success(ContinueNode(tok.pos_start, tok.pos_end))
            else:
                return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "continue statement outside loop"))
        else:
            return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected 'continue'"))

    def break_expr(self):
        """Parse the break expression syntax.

        Returns:
            ParseResult: the break expression Node.
        """
        res = ParseResult()
        tok = self.current_token
        if tok.matches(Tokens.KEYWORD, Tokens.BREAK):
            res.register_advancement()
            self.advance()
            
            if self.isInsideLoop:
                return res.success(BreakNode(tok.pos_start, tok.pos_end))
            else:
                return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "break statement outside loop"))
        else:
            return res.failure(InvalidSyntaxError(tok.pos_start, self.current_token.pos_end, "Expected 'Break'"))
         
    def statement(self, isInsideFunc):
        """Parse a statement syntax.

        Args:
            isInsideFunc (bool): check if the statement is inside a function.

        Returns:
            ParseResult: the statement syntax tree.
        """
        tok = self.current_token
        if tok.matches(Tokens.KEYWORD, Tokens.RETURN):
            return self.return_expr(isInsideFunc)
        elif tok.matches(Tokens.KEYWORD, Tokens.CONTINUE):
            return self.continue_expr()
        elif tok.matches(Tokens.KEYWORD, Tokens.BREAK):
            return self.break_expr()
        else:
            return self.bool_expr()
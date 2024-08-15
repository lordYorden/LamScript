from Lexer.mytoken import Tokens
class NumberNode:
    def __init__(self, token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end

    def __repr__(self):
        return f'{self.token}'
    
class BooleanNode:
    def __init__(self, token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end

    def __repr__(self):
        return f'{self.token}'
    
class BinOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node
        
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_token}, {self.right_node})'
    
class UnaryOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node
        
        self.pos_start = self.op_token.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f'({self.op_token}, {self.node})'
    
class whileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node
        
        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        return f'while ({self.condition_node}) {Tokens.LBRCE} {self.body_node} {Tokens.RBRCE}'
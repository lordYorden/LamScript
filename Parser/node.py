from Lexer.Tokens import Tokens
class NumberNode:
    def __init__(self, token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end
        
    def get_token(self):
        return self.token

    def __repr__(self):
        return f'{self.token}'
    
class BooleanNode:
    def __init__(self, token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end
        
    def get_token(self):
        return self.token

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
    def __init__(self, condition_node, body_nodes):
        self.condition_node = condition_node
        self.body_nodes = body_nodes
        
        self.pos_start = self.condition_node.pos_start
        
        if len(self.body_nodes) > 0:
            self.pos_start = self.body_nodes[0].pos_start
            self.pos_end = self.body_nodes[len(self.body_nodes) - 1].pos_end
        else:
            self.pos_end = self.condition_node.pos_end

    def __repr__(self):
        return f'while ({self.condition_node}) {Tokens.LBRCE} {self.body_node} {Tokens.RBRCE}'
    
class SymbolAcsessNode:
    def __init__(self, identifier_token):
        self.identifier_token = identifier_token
        self.pos_start = identifier_token.pos_start
        self.pos_end = identifier_token.pos_end
        
    def get_token(self):
        return self.identifier_token

    def __repr__(self):
        return f'{self.identifier_token}'
    
class FuncDefNode:
    def __init__(self, identifier_node, arg_nodes, body_node):
        self.identifier_token = identifier_node.identifier_token if identifier_node else None
        self.arg_nodes = arg_nodes
        self.body_node = body_node
        
        if self.identifier_token:
            self.pos_start = self.identifier_token.pos_start
        elif len(self.arg_nodes) > 0:
            self.pos_start = self.arg_nodes[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start
        
        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        return f'{self.identifier_token}({self.arg_nodes}) {Tokens.LBRCE} {self.body_node} {Tokens.RBRCE}'
    
class FuncCallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes
        
        self.pos_start = self.node_to_call.pos_start
        
        if len(self.arg_nodes) > 0:
            self.pos_start = self.arg_nodes[0].pos_start
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end

    def __repr__(self):
        return f'{self.node_to_call}({self.arg_nodes})'    
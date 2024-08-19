from Lexer.Tokens import Tokens

class BaseNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end
        
    def print_statement(self):
        self.statement_str = self.pos_start.extract_str(self.pos_end)
        return self.statement_str
class NumberNode(BaseNode):
    def __init__(self, token):
        super().__init__(token.pos_start, token.pos_end)
        self.token = token
        # self.pos_start = token.pos_start
        # self.pos_end = token.pos_end
        
    def get_token(self):
        return self.token

    def __repr__(self):
        return f'{self.token}'
    
class BooleanNode(BaseNode):
    def __init__(self, token):
        super().__init__(token.pos_start, token.pos_end)
        self.token = token
        # self.pos_start = token.pos_start
        # self.pos_end = token.pos_end
        
    def get_token(self):
        return self.token

    def __repr__(self):
        return f'{self.token}'
    
class BinOpNode(BaseNode):
    def __init__(self, left_node, op_token, right_node):
        super().__init__(left_node.pos_start, right_node.pos_end)
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node
        
        # self.pos_start = self.left_node.pos_start
        # self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_token}, {self.right_node})'
    
class UnaryOpNode(BaseNode):
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node
        
        # self.pos_start = self.op_token.pos_start
        # self.pos_end = self.node.pos_end

    def __repr__(self):
        return f'({self.op_token}, {self.node})'
    
class whileNode(BaseNode):
    def __init__(self, condition_node, body_nodes, pos_end=None):
        super().__init__(condition_node.pos_start, condition_node.pos_end)
        self.condition_node = condition_node
        self.body_nodes = body_nodes
        
        #self.pos_start = self.condition_node.pos_start
        
        if len(self.body_nodes) > 0:
            #self.pos_start = self.body_nodes[0].pos_start
            self.pos_end = self.body_nodes[len(self.body_nodes) - 1].pos_end
        else:
            self.pos_end = self.condition_node.pos_end
            
        if pos_end:
            self.pos_end = pos_end

    def __repr__(self):
        return f'while ({self.condition_node}) {Tokens.LBRCE} {self.body_nodes} {Tokens.RBRCE}'
    
class SymbolAcsessNode(BaseNode):
    def __init__(self, identifier_token):
        super().__init__(identifier_token.pos_start, identifier_token.pos_end)
        self.identifier_token = identifier_token
        # self.pos_start = identifier_token.pos_start
        # self.pos_end = identifier_token.pos_end
        
    def get_token(self):
        return self.identifier_token

    def __repr__(self):
        return f'{self.identifier_token}'
    
class FuncDefNode(BaseNode):
    def __init__(self, identifier_node, arg_nodes, body_nodes,auto_return, pos_end=None):
        super().__init__(identifier_node.pos_start, identifier_node.pos_end)
        self.identifier_token = identifier_node.identifier_token if identifier_node else None
        self.arg_nodes = arg_nodes
        self.body_nodes = body_nodes
        self.auto_return = auto_return
        
        # if self.identifier_token:
        #     self.pos_start = self.identifier_token.pos_start
        # elif len(self.arg_nodes) > 0:
        #     self.pos_start = self.arg_nodes[0].pos_start
        
        if len(self.body_nodes) > 0:
            #self.pos_start = self.body_nodes[0].pos_start
            self.pos_end = self.body_nodes[len(self.body_nodes) - 1].pos_end     
            
        if pos_end:
            self.pos_end = pos_end 

    def __repr__(self):
        return f'{self.identifier_token}({self.arg_nodes}) {Tokens.LBRCE} {self.body_nodes} {Tokens.RBRCE}'
    
class FuncCallNode(BaseNode):
    def __init__(self, node_to_call, arg_nodes):
        super().__init__(node_to_call.pos_start, node_to_call.pos_end)
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes
        
        self.pos_start = self.node_to_call.pos_start
        
        if len(self.arg_nodes) > 0:
            #self.pos_start = self.arg_nodes[0].pos_start
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end

    def __repr__(self):
        return f'{self.node_to_call}({self.arg_nodes})'    
    
class ReturnNode(BaseNode):
    def __init__(self, node_to_return, pos_start, pos_end):
        super().__init__(pos_start, pos_end)
        self.node_to_return = node_to_return
        # self.pos_start = pos_start
        # self.pos_end = pos_end

    def __repr__(self):
        return f'{self.node_to_return}'
    
class ContinueNode(BaseNode):
    def __init__(self, pos_start, pos_end):
        super().__init__(pos_start, pos_end)
        # self.pos_start = pos_start
        # self.pos_end = pos_end

    def __repr__(self):
        return f'continue'
    
class BreakNode(BaseNode):
    def __init__(self, pos_start, pos_end):
        super().__init__(pos_start, pos_end)
        # self.pos_start = pos_start
        # self.pos_end = pos_end

    def __repr__(self):
        return f'break'
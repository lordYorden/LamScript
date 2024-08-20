from Lexer.Tokens import Tokens

class BaseNode:
    def __init__(self, pos_start, pos_end):
        """The base node.

        Args:
            pos_start (position): The start position of the object.
            pos_end (position): The end position of the object.
        """
        self.pos_start = pos_start
        self.pos_end = pos_end
        
    def print_statement(self):
        """Print the statement of the object.

        Returns:
            string: the statement of the object.
        """
        self.statement_str = self.pos_start.extract_str(self.pos_end)
        return self.statement_str
class NumberNode(BaseNode):
    def __init__(self, token):
        """The number node.

        Args:
            token (token): The token of the number.
        """
        super().__init__(token.pos_start, token.pos_end)
        self.token = token
        # self.pos_start = token.pos_start
        # self.pos_end = token.pos_end
        
    def get_token(self):
        """Return the token of the number.

        Returns:
            token: the token.
        """
        return self.token

    def __repr__(self):
        """Return the string representation of the object.

        Returns:
            string: the string representation of the object.
        """
        return f'{self.token}'
    
class BooleanNode(BaseNode):
    def __init__(self, token):
        """The boolean node.

        Args:
            token (token): The token of the boolean.
        """
        super().__init__(token.pos_start, token.pos_end)
        self.token = token
        # self.pos_start = token.pos_start
        # self.pos_end = token.pos_end
        
    def get_token(self):
        """Return the token of the boolean.

        Returns:
            token: the token.
        """
        return self.token

    def __repr__(self):
        """Return the string representation of the object.

        Returns:
            string: the string representation of the object.
        """
        return f'{self.token}'
    
class BinOpNode(BaseNode):
    def __init__(self, left_node, op_token, right_node):
        """The binary operation node.

        Args:
            left_node (node): The left node of the operation.
            op_token (character): The token of the operation.
            right_node (node): The right node of the operation.
        """
        super().__init__(left_node.pos_start, right_node.pos_end)
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node
        
        # self.pos_start = self.left_node.pos_start
        # self.pos_end = self.right_node.pos_end

    def __repr__(self):
        """Return the string representation of the object.

        Returns:
            string: the string representation of the object.
        """
        return f'({self.left_node}, {self.op_token}, {self.right_node})'
    
class UnaryOpNode(BaseNode):
    def __init__(self, op_token, node):
        """The unary operation node.

        Args:
            op_token (token): The token of the operation.
            node (node): The node of the operation.
        """
        self.op_token = op_token
        self.node = node
        
        # self.pos_start = self.op_token.pos_start
        # self.pos_end = self.node.pos_end

    def __repr__(self):
        """Return the string representation of the object.

        Returns:
            string: the string representation of the object.
        """
        return f'({self.op_token}, {self.node})'
    
class whileNode(BaseNode):
    def __init__(self, condition_node, body_nodes, pos_end=None):
        """The while node.

        Args:
            condition_node (node): The condition node of the while loop.
            body_nodes (node): The body nodes of the while loop.
            pos_end (position, None): The end position of the object. Defaults to None.
        """
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
        """Return the string representation of the object.

        Returns:
            string: the string representation of the object.
        """
        return f'while ({self.condition_node}) {Tokens.LBRCE} {self.body_nodes} {Tokens.RBRCE}'
    
class SymbolAcsessNode(BaseNode):
    def __init__(self, identifier_token):
        """The symbol access node.

        Args:
            identifier_token (token): The token of the identifier.
        """
        super().__init__(identifier_token.pos_start, identifier_token.pos_end)
        self.identifier_token = identifier_token
        # self.pos_start = identifier_token.pos_start
        # self.pos_end = identifier_token.pos_end
        
    def get_token(self):
        """Return the token of the object.

        Returns:
            token: the token of the object.
        """
        return self.identifier_token

    def __repr__(self):
        """Return the string representation of the object.

        Returns:
            string: the string representation of the object.
        """
        return f'{self.identifier_token}'
    
class FuncDefNode(BaseNode):
    def __init__(self, identifier_node, arg_nodes, body_nodes,auto_return, pos_end=None):
        """The function definition node.

        Args:
            identifier_node (node): the identifier node of the function.
            arg_nodes (node): the argument nodes of the function.
            body_nodes (node): the body nodes of the function.
            auto_return (_type_): _description_
            pos_end (position, None): The end position of the object. Defaults to None.
        """
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
        """Return the string representation of the object.

        Returns:
            string: the string representation of the object.
        """
        return f'{self.identifier_token}({self.arg_nodes}) {Tokens.LBRCE} {self.body_nodes} {Tokens.RBRCE}'
    
class FuncCallNode(BaseNode):
    def __init__(self, node_to_call, arg_nodes):
        """The function call node.

        Args:
            node_to_call (node): the node to call.
            arg_nodes (node): the argument nodes.
        """
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
        """Return the string representation of the object.

        Returns:
            string: the string representation of the object.
        """
        return f'{self.node_to_call}({self.arg_nodes})'    
    
class ReturnNode(BaseNode):
    def __init__(self, node_to_return, pos_start, pos_end):
        super().__init__(pos_start, pos_end)
        self.node_to_return = node_to_return
        # self.pos_start = pos_start
        # self.pos_end = pos_end

    def __repr__(self):
        """Return the string representation of the object.

        Returns:
            string: the string return of the object.
        """
        return f'{self.node_to_return}'
    
class ContinueNode(BaseNode):
    def __init__(self, pos_start, pos_end):
        super().__init__(pos_start, pos_end)
        # self.pos_start = pos_start
        # self.pos_end = pos_end

    def __repr__(self):
        """Return the string representation of the object.

        Returns:
            string: the string continue of the object.
        """
        return f'continue'
    
class BreakNode(BaseNode):
    def __init__(self, pos_start, pos_end):
        """The break node.

        Args:
            pos_start (position): the start position of the object.
            pos_end (position): the end position of the object.
        """
        super().__init__(pos_start, pos_end)
        # self.pos_start = pos_start
        # self.pos_end = pos_end

    def __repr__(self):
        """Return the string representation of the object.

        Returns:
            string: the string break of the object.
        """
        return f'break'
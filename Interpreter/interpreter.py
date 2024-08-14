from Interpreter.Objects.Number import Number
from Interpreter.Objects.Boolean import Boolean
from Interpreter.Objects.Object import Object

class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        mehtod = getattr(self, method_name, self.no_visit_method)
        return mehtod(node)
    
    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    def visit_NumberNode(self, node):
        return Number(node.token.value).set_pos(node.pos_start, node.pos_end) ,None
    
    def visit_BooleanNode(self, node):
        return Boolean(node.token.value).set_pos(node.pos_start, node.pos_end), None
    
    def visit_BinOpNode(self, node):
        left, error = self.visit(node.left_node)
        if error: return None, error
        
        right, error = self.visit(node.right_node)
        if error: return None, error
        
        object, error = left.bin_op(node.op_token, right)
        if error: return None, error
        return object.set_pos(node.pos_start, node.pos_end), None
        
    def visit_UnaryOpNode(self, node):
        #find a fix for neg
        object, error = self.visit(node.node)
        object, error = object.unary_op(node.op_token)
        if error:
            return None, error
        return object.set_pos(node.pos_start, node.pos_end), None
        
        
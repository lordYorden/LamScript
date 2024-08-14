from Interpreter.Operations.Operation import UnaryOperation, BinaryOperation
import Interpreter.Objects.Boolean as Boolean
from Lexer.myerror import TypeError

class BooleanOperation(BinaryOperation):
    supported_types = (Boolean)
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
    
    def eval(self):
        #fix this
        return self.op_func(self.left, self.right), None
        if isinstance(self.left, self.supported_types) and isinstance(self.right, self.supported_types):
            return self.op_func(self.left, self.right), None
        return None, TypeError(self.left.pos_start, self.right.pos_end, f"Unsupported operand type(s) for {self.op_token}: '{self.left.__class__.__name__}' and '{self.right.__class__.__name__}'")
    
class UnaryBooleanOperation(UnaryOperation):
    def __init__(self, op_token, Object):
        super().__init__(op_token, Object)
        
    def eval(self):
        return self.op_func(self.left), None
    
class equels(BooleanOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.eq)
    
    def eq(self, left, right):
        return Boolean.Boolean(left.value == right.value).set_pos(left.pos_start, right.pos_end)
    
class not_equels(BooleanOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.neq)
    
    def neq(self, left, right):
        return Boolean.Boolean(left.value != right.value).set_pos(left.pos_start, right.pos_end)

class and_op(BooleanOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.and_)
    
    def and_(self, left, right):
        return Boolean.Boolean(left.value and right.value).set_pos(left.pos_start, right.pos_end)
    
class or_op(BooleanOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.or_)
    
    def or_(self, left, right):
        return Boolean.Boolean(left.value or right.value).set_pos(left.pos_start, right.pos_end)
    
class not_op(UnaryBooleanOperation):
    def __init__(self, op_token, Object):
        super().__init__(op_token, Object)
        self.set_op_func(self.not_)
    
    def not_(self, Object):
        return Boolean.Boolean(not Object.value).set_pos(Object.pos_start, Object.pos_end)
from Interpreter.Operations.Operation import UnaryOperation, BinaryOperation
import Interpreter.Objects.Boolean as Boolean
import Interpreter.Objects.Number as Number
from Lexer.myerror import TypeError

class BooleanOperation(BinaryOperation):
    supported_types = (Boolean, Number)
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
    
    def eval(self):
        #fix this
        return self.op_func(self.left, self.right), None
        if isinstance(self.left, self.supported_types) and isinstance(self.right, self.supported_types):
            return self.op_func(self.left, self.right), None
        return None, TypeError(self.left.pos_start, self.right.pos_end, f"Unsupported operand type(s) for {self.op_token}: '{self.left.__class__.__name__}' and '{self.right.__class__.__name__}'")
    
class equels(BinaryOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.eq)
    
    def eq(self, left, right):
        return Boolean(left.value == right.value).set_pos(left.pos_start, right.pos_end)
    
class not_equels(BinaryOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.neq)
    
    def neq(self, left, right):
        return Boolean(left.value != right.value).set_pos(left.pos_start, right.pos_end)

class and_op(BinaryOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.and_)
    
    def and_(self, left, right):
        return Boolean(left.value and right.value).set_pos(left.pos_start, right.pos_end)
    
class or_op(BinaryOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.or_)
    
    def or_(self, left, right):
        return Boolean(left.value or right.value).set_pos(left.pos_start, right.pos_end)
    
class not_op(UnaryOperation):
    def __init__(self, op_token, Object):
        super().__init__(op_token, Object)
        self.set_op_func(self.not_)
    
    def not_(self, Object):
        return Boolean(not Object.value).set_pos(Object.pos_start, Object.pos_end)
    
class greater(BinaryOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.gt)
    
    def gt(self, left, right):
        return  Boolean(left.value > right.value).set_pos(left.pos_start, right.pos_end)
    
class less(BinaryOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.lt)
    
    def lt(self, left, right):
        return  Boolean(left.value < right.value).set_pos(left.pos_start, right.pos_end)
    
class greater_eq(BinaryOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.gte)
    
    def gte(self, left, right):
        return  Boolean(left.value >= right.value).set_pos(left.pos_start, right.pos_end)
    
class less_eq(BinaryOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.lte)
    
    def lte(self, left, right):
        return  Boolean(left.value <= right.value).set_pos(left.pos_start, right.pos_end)
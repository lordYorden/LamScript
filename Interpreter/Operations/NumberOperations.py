from Interpreter.Operations.Operation import UnaryOperation, BinaryOperation
import Interpreter.Objects.Number as Number
import Interpreter.Objects.Boolean as Boolean
from Lexer.myerror import TypeError

class NumberOperation(BinaryOperation):
    supported_types = (Number)
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
    
    def eval(self):
        #fix this
        return self.op_func(self.left, self.right), None
        if isinstance(self.left, type(Number)) and isinstance(self.right,  type(Number)):
            return self.op_func(self.left, self.right), None
        return None, TypeError(self.left.pos_start, self.right.pos_end, f"Unsupported operand type(s) for {self.op_token}: '{self.left.__class__.__name__}' and '{self.right.__class__.__name__}'")

class UnaryNumberOperation(UnaryOperation):
    def __init__(self, op_token, Object):
        super().__init__(op_token, Object)
    
    def eval(self):
        return self.op_func(self.left), None

class add(NumberOperation): 
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.add)
    
    def add(self, left, right):
        return Number.Number(left.value + right.value).set_pos(left.pos_start, right.pos_end)
    
class sub(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.sub)
    
    def sub(self, left, right):
        return Number.Number(left.value - right.value).set_pos(left.pos_start, right.pos_end)
    
class mul(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.mul)
    
    def mul(self, left, right):
         return Number.Number(left.value * right.value).set_pos(left.pos_start, right.pos_end)
    
class div(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.div)
    
    def div(self, left, right):
         return Number.Number(left.value // right.value).set_pos(left.pos_start, right.pos_end)
    
class idiv(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.idiv)
    
    def idiv(self, left, right):
         return Number.Number(left.value // right.value).set_pos(left.pos_start, right.pos_end)
    
class mod(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.mod)
    
    def mod(self, left, right):
        return Number.Number(left.value % right.value).set_pos(left.pos_start, right.pos_end)

class neg(UnaryNumberOperation):
    def __init__(self, op_token, object):
        super().__init__(op_token, object)
        self.set_op_func(self.neg)
    
    def neg(self, object):
        return Number.Number(-object.value).set_pos(object.pos_start, object.pos_end)

class sign(UnaryNumberOperation):
    def __init__(self, op_token, object):
        super().__init__(op_token, object)
        self.set_op_func(self.sign)
    
    def sign(self, object):
        return Number.Number(object.value).set_pos(object.pos_start, object.pos_end)
    
class greater(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.gt)
    
    def gt(self, left, right):
        return Boolean(left.value > right.value).set_pos(left.pos_start, right.pos_end)
    
class less(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.lt)
    
    def lt(self, left, right):
        return Boolean.Boolean(left.value < right.value).set_pos(left.pos_start, right.pos_end)
    
class greater_eq(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.gte)
    
    def gte(self, left, right):
        return Boolean.Boolean(left.value >= right.value).set_pos(left.pos_start, right.pos_end)
    
class less_eq(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.lte)
    
    def lte(self, left, right):
        return Boolean.Boolean(left.value <= right.value).set_pos(left.pos_start, right.pos_end)
    
class equels(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.eq)
    
    def eq(self, left, right):
        return Boolean.Boolean(left.value == right.value).set_pos(left.pos_start, right.pos_end)
    
class not_equels(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.neq)
    
    def neq(self, left, right):
        return Boolean.Boolean(left.value != right.value).set_pos(left.pos_start, right.pos_end)
    
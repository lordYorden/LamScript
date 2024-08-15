from Interpreter.Operations.Operation import UnaryOperation, BinaryOperation
import Interpreter.Objects.Number as Number
import Interpreter.Objects.Boolean as Boolean
from Lexer.myerror import TypeError, RunTimeError

class NumberOperation(BinaryOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
    
    def eval(self):
        value, error = self.op_func(self.left, self.right)
        if error: return None, error
        return value, None

class UnaryNumberOperation(UnaryOperation):
    def __init__(self, op_token, Object):
        super().__init__(op_token, Object)
    
    def eval(self):
        value, error = self.op_func(self.left)
        if error: return None, error
        return value, None

class add(NumberOperation): 
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.add)
    
    def add(self, left, right):
        return Number.Number(left.value + right.value), None
    
class sub(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.sub)
    
    def sub(self, left, right):
        return Number.Number(left.value - right.value), None
    
class mul(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.mul)
    
    def mul(self, left, right):
         return Number.Number(left.value * right.value), None
    
#deprecated
class div(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.div)
    
    def div(self, left, right):
        if right.value == 0:
            return None, RunTimeError(right.pos_start, right.pos_end, "Division by zero" ,context=self.context)
        return Number.Number(left.value / right.value), None
    
class idiv(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.idiv)
    
    def idiv(self, left, right):
        if right.value == 0:
            return None, RunTimeError(right.pos_start, right.pos_end, "Division by zero" ,right.context)
        return Number.Number(left.value // right.value), None
    
class mod(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.mod)
    
    def mod(self, left, right):
        return Number.Number(left.value % right.value), None

class neg(UnaryNumberOperation):
    def __init__(self, op_token, object):
        super().__init__(op_token, object)
        self.set_op_func(self.neg)
    
    def neg(self, object):
        return Number.Number(-object.value), None

class sign(UnaryNumberOperation):
    def __init__(self, op_token, object):
        super().__init__(op_token, object)
        self.set_op_func(self.sign)
    
    def sign(self, object):
        return Number.Number(object.value), None
    
class greater(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.gt)
    
    def gt(self, left, right):
        return Boolean.Boolean(left.value > right.value), None
    
class less(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.lt)
    
    def lt(self, left, right):
        return Boolean.Boolean(left.value < right.value), None
    
class greater_eq(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.gte)
    
    def gte(self, left, right):
        return Boolean.Boolean(left.value >= right.value), None
    
class less_eq(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.lte)
    
    def lte(self, left, right):
        return Boolean.Boolean(left.value <= right.value), None
    
class equels(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.eq)
    
    def eq(self, left, right):
        return Boolean.Boolean(left.value == right.value), None
    
class not_equels(NumberOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.neq)
    
    def neq(self, left, right):
        return Boolean.Boolean(left.value != right.value), None
    
from Interpreter.Operations.Operation import UnaryOperation, BinaryOperation
import Interpreter.Objects.Boolean as Boolean
import Interpreter.Objects.Number as Number
from Error.RuntimeError import TypeError

class BooleanOperation(BinaryOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
    
    def eval(self):
        return self.op_func(self.left, self.right), None
    
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
        return Boolean.Boolean(left.value == right.value)
    
class not_equels(BooleanOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.neq)
    
    def neq(self, left, right):
        return Boolean.Boolean(left.value != right.value)

class and_op(BooleanOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.and_)
    
    def and_(self, left, right):
        return Boolean.Boolean(left.value and right.value)
    
class or_op(BooleanOperation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.or_)
    
    def or_(self, left, right):
        return Boolean.Boolean(left.value or right.value)
    
class not_op(UnaryBooleanOperation):
    def __init__(self, op_token, Object):
        super().__init__(op_token, Object)
        self.set_op_func(self.not_)
    
    def not_(self, Object):
        return Boolean.Boolean(not Object.value)
    
class add(BooleanOperation): 
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        self.set_op_func(self.add)
    
    def add(self, left, right):
        return Number.Number(left.value + right.value)
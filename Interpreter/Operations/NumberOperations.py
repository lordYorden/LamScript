from Interpreter.Operations.Operation import UnaryOperation, BinaryOperation
import Interpreter.Objects.Number as Number
import Interpreter.Objects.Boolean as Boolean
from Error.RuntimeError import TypeError, RunTimeError
from Interpreter.Objects.Object import Object

class NumberOperation(BinaryOperation):
    def __init__(self, op_token, left, right):
        """
        Initialize a NumberOperation object.

        Args:
            op_token (Token): The operator token.
            left (Object): The left operand.
            right (Object): The right operand.
        """
        super().__init__(op_token, left, right)
    
    def eval(self):
        """
        Evaluate the NumberOperation.

        Returns:
            value (Object): The result of the operation.
            error (Error): The error encountered during evaluation, if any.
        """
        value, error = super().eval()
        if error: return None, error
        value, error = self.op_func(self.left, self.right)
        if error: return None, error
        return value, None

class UnaryNumberOperation(UnaryOperation):
    def __init__(self, op_token, Object):
        """
        Initialize a UnaryNumberOperation object.

        Args:
            op_token (Token): The operator token.
            Object (Object): The operand.
        """
        super().__init__(op_token, Object)
    
    def eval(self):
        """
        Evaluate the UnaryNumberOperation.

        Returns:
            value (Object): The result of the operation.
            error (Error): The error encountered during evaluation, if any.
        """
        value, error = super().eval()
        if error: return None, error
        value, error = self.op_func(self.left)
        if error: return None, error
        return value, None

class add(NumberOperation): 
    def __init__(self, op_token, left, right):
        """
        Initialize an add object.

        Args:
            op_token (Token): The operator token.
            left (Object): The left operand.
            right (Object): The right operand.
        """
        super().__init__(op_token, left, right)
        self.set_op_func(self.add)
    
    def add(self, left, right):
        """
        Perform addition operation.

        Args:
            left (Object): The left operand.
            right (Object): The right operand.

        Returns:
            value (Object): The result of the addition operation.
            error (Error): The error encountered during evaluation, if any.
        """
        return Number.Number(left.value + right.value), None
    
class sub(NumberOperation):
    def __init__(self, op_token, left, right):
        """
        Initialize a sub object.

        Args:
            op_token (Token): The operator token.
            left (Object): The left operand.
            right (Object): The right operand.
        """
        super().__init__(op_token, left, right)
        self.set_op_func(self.sub)
    
    def sub(self, left, right):
        """
        Perform subtraction operation.

        Args:
            left (Object): The left operand.
            right (Object): The right operand.

        Returns:
            value (Object): The result of the subtraction operation.
            error (Error): The error encountered during evaluation, if any.
        """
        return Number.Number(left.value - right.value), None
    
class mul(NumberOperation):
    def __init__(self, op_token, left, right):
        """
        Initialize a mul object.

        Args:
            op_token (Token): The operator token.
            left (Object): The left operand.
            right (Object): The right operand.
        """
        super().__init__(op_token, left, right)
        self.set_op_func(self.mul)
    
    def mul(self, left, right):
        """
        Perform multiplication operation.

        Args:
            left (Object): The left operand.
            right (Object): The right operand.

        Returns:
            value (Object): The result of the multiplication operation.
            error (Error): The error encountered during evaluation, if any.
        """
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
        """
        Initialize an idiv object.

        Args:
            op_token (Token): The operator token.
            left (Object): The left operand.
            right (Object): The right operand.
        """
        super().__init__(op_token, left, right)
        self.set_op_func(self.idiv)
    
    def idiv(self, left, right):
        """
        Perform integer division operation. Handles division by zero.

        Args:
            left (Object): The left operand.
            right (Object): The right operand.

        Returns:
            value (Object): The result of the integer division operation.
            error (Error): The error encountered during evaluation, if any.
        """
        if right.value == 0:
            return None, RunTimeError(right.pos_start, right.pos_end, "Division by zero" ,right.context)
        return Number.Number(left.value // right.value), None
    
class mod(NumberOperation):
    def __init__(self, op_token, left, right):
        """
        Initialize a mod object.

        Args:
            op_token (Token): The operator token.
            left (Object): The left operand.
            right (Object): The right operand.
        """
        super().__init__(op_token, left, right)
        self.set_op_func(self.mod)
    
    def mod(self, left, right):
        """
        Perform modulo operation.

        Args:
            left (Object): The left operand.
            right (Object): The right operand.

        Returns:
            value (Object): The result of the modulo operation.
            error (Error): The error encountered during evaluation, if any.
        """
        return Number.Number(left.value % right.value), None

class neg(UnaryNumberOperation):
    def __init__(self, op_token, object):
        """
        Initialize a neg object.

        Args:
            op_token (Token): The operator token.
            object (Object): The operand.
        """
        super().__init__(op_token, object)
        self.set_op_func(self.neg)
    
    def neg(self, object):
        """
        Perform negation operation.

        Args:
            object (Object): The operand.

        Returns:
            value (Object): The result of the negation operation.
            error (Error): The error encountered during evaluation, if any.
        """
        return Number.Number(-object.value), None

class sign(UnaryNumberOperation):
    def __init__(self, op_token, object):
        """
        Initialize a sign object.

        Args:
            op_token (Token): The operator token.
            object (Object): The operand.
        """
        super().__init__(op_token, object)
        self.set_op_func(self.sign)
    
    def sign(self, object):
        """
        Perform sign operation.

        Args:
            object (Object): The operand.

        Returns:
            value (Object): The result of the sign operation.
            error (Error): The error encountered during evaluation, if any.
        """
        return Number.Number(object.value), None
    
class greater(NumberOperation):
    def __init__(self, op_token, left, right):
        """
        Initialize a greater object.

        Args:
            op_token (Token): The operator token.
            left (Object): The left operand.
            right (Object): The right operand.
        """
        super().__init__(op_token, left, right)
        self.set_op_func(self.gt)
    
    def gt(self, left, right):
        """
        Perform greater than operation.

        Args:
            left (Object): The left operand.
            right (Object): The right operand.

        Returns:
            value (Object): The result of the greater than operation.
            error (Error): The error encountered during evaluation, if any.
        """
        return Boolean.Boolean(left.value > right.value), None
    
class less(NumberOperation):
    def __init__(self, op_token, left, right):
        """
        Initialize a less object.

        Args:
            op_token (Token): The operator token.
            left (Object): The left operand.
            right (Object): The right operand.
        """
        super().__init__(op_token, left, right)
        self.set_op_func(self.lt)
    
    def lt(self, left, right):
        """
        Perform less than operation.

        Args:
            left (Object): The left operand.
            right (Object): The right operand.

        Returns:
            value (Object): The result of the less than operation.
            error (Error): The error encountered during evaluation, if any.
        """
        return Boolean.Boolean(left.value < right.value), None
    
class greater_eq(NumberOperation):
    def __init__(self, op_token, left, right):
        """
        Initialize a greater_eq object.

        Args:
            op_token (Token): The operator token.
            left (Object): The left operand.
            right (Object): The right operand.
        """
        super().__init__(op_token, left, right)
        self.set_op_func(self.gte)
    
    def gte(self, left, right):
        """
        Perform greater than or equal to operation.

        Args:
            left (Object): The left operand.
            right (Object): The right operand.

        Returns:
            value (Object): The result of the greater than or equal to operation.
            error (Error): The error encountered during evaluation, if any.
        """
        return Boolean.Boolean(left.value >= right.value), None
    
class less_eq(NumberOperation):
    def __init__(self, op_token, left, right):
        """
        Initialize a less_eq object.

        Args:
            op_token (Token): The operator token.
            left (Object): The left operand.
            right (Object): The right operand.
        """
        super().__init__(op_token, left, right)
        self.set_op_func(self.lte)
    
    def lte(self, left, right):
        """
        Perform less than or equal to operation.

        Args:
            left (Object): The left operand.
            right (Object): The right operand.

        Returns:
            value (Object): The result of the less than or equal to operation.
            error (Error): The error encountered during evaluation, if any.
        """
        return Boolean.Boolean(left.value <= right.value), None
    
class equels(NumberOperation):
    def __init__(self, op_token, left, right):
        """
        Initialize an equels object.

        Args:
            op_token (Token): The operator token.
            left (Object): The left operand.
            right (Object): The right operand.
        """
        super().__init__(op_token, left, right)
        self.set_op_func(self.eq)
    
    def eq(self, left, right):
        """
        Perform equality operation.

        Args:
            left (Object): The left operand.
            right (Object): The right operand.

        Returns:
            value (Object): The result of the equality operation.
            error (Error): The error encountered during evaluation, if any.
        """
        return Boolean.Boolean(left.value == right.value), None
    
class not_equels(NumberOperation):
    def __init__(self, op_token, left, right):
        """
        Initialize a not_equels object.

        Args:
            op_token (Token): The operator token.
            left (Object): The left operand.
            right (Object): The right operand.
        """
        super().__init__(op_token, left, right)
        self.set_op_func(self.neq)
    
    def neq(self, left, right):
        """
        Perform not equal to operation.

        Args:
            left (Object): The left operand.
            right (Object): The right operand.

        Returns:
            value (Object): The result of the not equal to operation.
            error (Error): The error encountered during evaluation, if any.
        """
        return Boolean.Boolean(left.value != right.value), None
    
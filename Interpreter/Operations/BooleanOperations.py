from Interpreter.Operations.Operation import UnaryOperation, BinaryOperation
import Interpreter.Objects.Boolean as Boolean
import Interpreter.Objects.Number as Number
from Error.RuntimeError import TypeError

class BooleanOperation(BinaryOperation):
    def __init__(self, op_token, left, right):
        """Initializes the Boolean Operation object

        Args:
            op_token (Token): the token of the operation
            left (Object): the left object of the operation
            right (Object): the right object of the operation
        """
        super().__init__(op_token, left, right)
    
    def eval(self):
        """Evaluates the operation

        Returns:
            Object: the result of the operation
        """
        value, error = super().eval()
        if error: return None, error
        return self.op_func(self.left, self.right), None
    
class UnaryBooleanOperation(UnaryOperation):
    def __init__(self, op_token, Object):
        """Initializes the Unary Boolean Operation object

        Args:
            op_token (Token): the token of the operation
            Object (Object): the object of the operation
        """
        super().__init__(op_token, Object)
        
    def eval(self):
        """Evaluates the operation

        Returns:
            Object: the result of the operation
        """
        value, error = super().eval()
        if error: return None, error
        return self.op_func(self.left), None
    
class equels(BooleanOperation):
    def __init__(self, op_token, left, right):
        """Initializes the equels Operation object

        Args:
            op_token (Token): the token of the operation
            left (Object): the left object of the operation
            right (Object): the right object of the operation
        """
        super().__init__(op_token, left, right)
        self.set_op_func(self.eq)
    
    def eq(self, left, right):
        """Checks if two objects are equal

        Args:
            left (Object): the left object of the operation
            right (Object): the right object of the operation

        Returns:
            Object: dose the two objects are equal
        """
        return Boolean.Boolean(left.value == right.value)
    
class not_equels(BooleanOperation):
    def __init__(self, op_token, left, right):
        """Initializes the NOT EQUALS Operation object

        Args:
            op_token (Token): the token of the operation
            left (Object): the left object of the operation
            right (Object): the right object of the operation
        """
        super().__init__(op_token, left, right)
        self.set_op_func(self.neq)
    
    def neq(self, left, right):
        """Checks if two objects are not equal

        Args:
            left (Object): the left object of the operation
            right (Object): the right object of the operation

        Returns:
            Object: dose the two objects are not equal
        """
        return Boolean.Boolean(left.value != right.value)

class and_op(BooleanOperation):
    def __init__(self, op_token, left, right):
        """Initializes the AND Operation object

        Args:
            op_token (Token): the token of the operation
            left (Object): the left object of the operation
            right (Object): the right object of the operation
        """
        super().__init__(op_token, left, right)
        self.set_op_func(self.and_)
    
    def and_(self, left, right):
        """AND Operation

        Args:
            left (Object): the left object of the operation
            right (Object): the right object of the operation

        Returns:
            Object: AND Operation of the two Boolean objects
        """
        return Boolean.Boolean(left.value and right.value)
    
class or_op(BooleanOperation):
    def __init__(self, op_token, left, right):
        """Initializes the OR Operation object

        Args:
            op_token (Token): the token of the operation
            left (Object): the left object of the operation
            right (Object): the right object of the operation
        """
        super().__init__(op_token, left, right)
        self.set_op_func(self.or_)
    
    def or_(self, left, right):
        """OR Operation

        Args:
            left (Object): the left object of the operation
            right (Object): the right object of the operation

        Returns:
            Object: OR Operation of the two Boolean objects
        """
        return Boolean.Boolean(left.value or right.value)
    
class not_op(UnaryBooleanOperation):
    def __init__(self, op_token, Object):
        """Initializes the NOT Operation object

        Args:
            op_token (Token): The token of the operation
            Object (Object): the object of the operation
        """
        super().__init__(op_token, Object)
        self.set_op_func(self.not_)
    
    def not_(self, Object):
        """NOT Operation

        Args:
            Object (Object): the object of the operation

        Returns:
            Object: NOT Operation of the Boolean object
        """
        return Boolean.Boolean(not Object.value)
    
class add(BooleanOperation): 
    def __init__(self, op_token, left, right):
        """Initializes the ADD Operation object

        Args:
            op_token (Token): the token of the operation
            left (Object): the left object of the operation
            right (Object): the right object of the operation
        """
        super().__init__(op_token, left, right)
        self.set_op_func(self.add)
    
    def add(self, left, right):
        """ADD Operation

        Args:
            left (Object): the left object of the operation
            right (Object): the right object of the operation

        Returns:
            Object: ADD Operation of the two Boolean objects
        """
        return Number.Number(left.value + right.value)
from Interpreter.Objects.Object import Object
from Error.RuntimeError import TypeError
class Operation:
    def __init__(self, op_token, left, right=None):
        """
        Initialize an Operation instance.
    
        Args:
            op_token (str): The token representing the operation.
            left (Any): The left operand of the operation.
            right (Any, optional): The right operand of the operation. Defaults to None.
        """
        self.left = left
        self.right = right
        self.op_token = op_token
        self.op_func = None
    
    def set_op_func(self, op_func):
        """
        Set the function to be used for the operation.
    
        Args:
            op_func (callable): The function that performs the operation.
        
        Returns:
            Operation: The current instance with the operation function set.
        """
        self.op_func = op_func
        return self
    
    def eval(self):
        """
        Evaluate the operation.
    
        Raises:
            NotImplementedError: If the operation is not implemented.
        """
        raise NotImplementedError(f"{self.op_token} Operation not implemented!")
    
    def __repr__(self):
        """
        Return a string representation of the operation.
    
        Returns:
            str: The string representation of the operation.
        """
        return f'{self.op}'
    
class UnaryOperation(Operation):

    def __init__(self, op_token, Object):
        """
        Initializes a UnaryOperation instance.

        Args:
            op_token: The token representing the operation.
            Object: The object on which the operation is performed.
        """
        super().__init__(op_token, Object)
        
    def eval(self):
        """
        Evaluates the unary operation.

        Returns:
            A tuple containing the result of the operation and an error if any.
        """
        if self.left == Object.none:
            return None, TypeError(self.right.pos_start, self.right.pos_end, f"Unsupported operand type(s) None", self.left.context)
        else:
            return self, None
        
class BinaryOperation(Operation):

    def __init__(self, op_token, left, right):
        """
        Initializes a BinaryOperation instance.

        Args:
            op_token: The token representing the operation.
            left: The left operand of the operation.
            right: The right operand of the operation.
        """
        super().__init__(op_token, left, right)
        
    def eval(self):
        """
        Evaluates the binary operation.

        Returns:
            A tuple containing the result of the operation and an error if any.
        """
        if self.right == Object.none:
            return None, TypeError(self.right.pos_start, self.right.pos_end, f"Unsupported operand type(s) for {self.left.__class__.__name__} * None", self.right.context)
        if self.left == Object.none:
            return None, TypeError(self.left.pos_start, self.left.pos_end, f"Unsupported operand type(s) for None * {self.right.__class__.__name__}", self.left.context)
        else:
            return self, None
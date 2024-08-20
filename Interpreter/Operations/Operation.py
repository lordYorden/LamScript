from Interpreter.Objects.Object import Object
from Error.RuntimeError import TypeError
class Operation:
    def __init__(self, op_token, left, right=None):
        self.left = left
        self.right = right
        self.op_token = op_token
        self.op_func = None
        
    def set_op_func(self, op_func):
        self.op_func = op_func
        return self

    def eval(self):
        raise NotImplementedError(f"{self.op_token} Operation not implemented!")
    
    def __repr__(self):
        return f'{self.op}'
    
class UnaryOperation(Operation):
    def __init__(self, op_token, Object):
        super().__init__(op_token, Object)
        
    def eval(self):
        if self.left == Object.none:
            return None, TypeError(self.right.pos_start, self.right.pos_end, f"Unsupported operand type(s) None",self.left.context)
        else:
            return self, None
        
class BinaryOperation(Operation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        
    def eval(self):
        if self.right == Object.none:
            return None, TypeError(self.right.pos_start, self.right.pos_end, f"Unsupported operand type(s) for {self.left.__class__.__name__} * None",self.right.context)
        if self.left == Object.none:
            return None, TypeError(self.left.pos_start, self.left.pos_end, f"Unsupported operand type(s) for None * {self.right.__class__.__name__}", self.left.context)
        else:
            return self, None
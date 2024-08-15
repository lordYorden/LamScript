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
        return super().eval()
        
class BinaryOperation(Operation):
    def __init__(self, op_token, left, right):
        super().__init__(op_token, left, right)
        
    def eval(self):
        return super().eval()
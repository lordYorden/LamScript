from Error.RuntimeError import TypeError

class Object: 
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()
        
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def set_context(self, context=None):
        self.context = context
        return self
    
    def unary_op(self, op_token):
        op, error = self.find_unary_op(op_token)
        if error:
            return None, error
        
        op = op(op_token, self)
        object, error = op.eval()
        if error:
            return None, error
        
        object.set_context(self.context)
        return object, None
    
    def bin_op(self, op_token, other):
        op, error = self.find_bin_op(op_token)
        if error:
            return None, error
        
        op = op(op_token, self, other)
        object, error = op.eval()
        if error:
            return None, error
        object.set_context(self.context)
        object.set_pos(self.pos_start, other.pos_end)
        return object, None

    def find_bin_op(self, op_token):
        pass
    
    def find_unary_op(self, op_token):
        pass
    
    def find_op(self, op_token, operations):
        op = operations.get(op_token.type, None)
        if op is None:
            return None, TypeError(self.pos_start, self.pos_end, f"Unsupported operand type(s) for {op_token}: '{self.__class__.__name__}'", self.context)
        else:
            return op, None
        
    def __repr__(self):
        return f'{self.value}'
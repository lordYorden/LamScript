from Lexer.myerror import TypeError

class Object:
    operations = {}  # Add this line to define the self.operations attribute
    
    def __init__(self, value):
        self.value = value
        self.set_pos()
        
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def unary_op(self, op_token):
        op, error = self.find_op(op_token)
        if error:
            return None, error
        
        op = op(op_token, self)
        object, error = op.eval()
        if error:
            return None, error
        return object, None
    
    def bin_op(self, op_token, other):
        op, error = self.find_op(op_token)
        if error:
            return None, error
        
        op = op(op_token, self, other)
        object, error = op.eval()
        if error:
            return None, error
        return object, None

    def find_op(self, op_token):
        pass
        
    def __repr__(self):
        return f'{self.value}'
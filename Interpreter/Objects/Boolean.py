from Interpreter.Objects.Object import Object
import Interpreter.Operations.BooleanOperations as BooleanOperation
from Lexer.mytoken import Tokens
from Lexer.myerror import TypeError

class Boolean(Object):
    bin_operations = {Tokens.EQUEL: BooleanOperation.equels, 
                    Tokens.NEQUEL: BooleanOperation.not_equels,
                    Tokens.AND: BooleanOperation.and_op,
                    Tokens.OR: BooleanOperation.or_op,
                    Tokens.NOT: BooleanOperation.not_op}
    
    unary_operations = {Tokens.NOT: BooleanOperation.not_op}
    
    def __init__(self, value):
        super().__init__(value)
        
    def find_bin_op(self, op_token):
        return self.find_op(op_token, self.bin_operations)
        
    def find_unary_op(self, op_token):
        return self.find_op(op_token, self.unary_operations)
        
    def __repr__(self):
        return f'{self.value}'
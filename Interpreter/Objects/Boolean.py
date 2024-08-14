from Interpreter.Objects.Object import Object
import Interpreter.Operations.BooleanOperations as BooleanOperation
from Lexer.mytoken import Tokens

class Boolean(Object):
    operations = {Tokens.EQUEL: BooleanOperation.equels, 
                    Tokens.NEQUEL: BooleanOperation.not_equels,
                    Tokens.AND: BooleanOperation.and_op,
                    Tokens.OR: BooleanOperation.or_op,
                    Tokens.NOT: BooleanOperation.not_op,
                    Tokens.GREATER: BooleanOperation.greater,
                    Tokens.LESS: BooleanOperation.less,
                    Tokens.GREATERE: BooleanOperation.greater_eq,
                    Tokens.LESSE: BooleanOperation.less_eq}
    
    def __init__(self, value):
        super().__init__(value)
        
    def find_op(self, op_token):
        op = self.operations.get(op_token, None)
        if op is None:
            return None, TypeError(self.pos_start, self.pos_end, f"Unsupported operand type(s) for {op_token}: '{self.__class__.__name__}'")
        else:
            return op, None
        
    def __repr__(self):
        return f'{self.value}'
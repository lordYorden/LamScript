from Interpreter.Objects.Object import Object
import Interpreter.Operations.NumberOperations as NumberOperations #add, sub, mul, div, idiv, mod, neg
from Lexer.mytoken import Tokens

class Number(Object):
    operations  = {Tokens.ADD: NumberOperations.add, 
                            Tokens.SUB: NumberOperations.sub,
                            Tokens.MUL: NumberOperations.mul,
                            Tokens.DIV: NumberOperations.div,
                            Tokens.IDIV: NumberOperations.idiv,
                            Tokens.MOD: NumberOperations.mod}
    
    def __init__(self, value):
        super().__init__(value)
    
    #make it general for all types   
    def find_op(self, op_token):
        op = self.operations.get(op_token.type, None)
        if op is None:
            return None, TypeError(self.pos_start, self.pos_end, f"Unsupported operand type(s) for {op_token}: '{self.__class__.__name__}'")
        else:
            return op, None
        
    def copy(self):
        return Number(self.value, self.pos_start, self.pos_end)
    
    def set_value(self, value):
        self.value = value
        return self
        
        
    def __repr__(self):
        return f'{self.value}'
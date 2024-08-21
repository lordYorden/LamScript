from Interpreter.Objects.Object import Object
import Interpreter.Operations.NumberOperations as NumberOperations
from Lexer.Tokens import Tokens
from Error.RuntimeError import TypeError
class Number(Object):
    """the Number object class and its operations

    Args:
        Object (object): the base object class
    """
    bin_operations  = {Tokens.ADD: NumberOperations.add, 
                            Tokens.SUB: NumberOperations.sub,
                            Tokens.MUL: NumberOperations.mul,
                            Tokens.DIV: NumberOperations.idiv,
                            Tokens.IDIV: NumberOperations.idiv,
                            Tokens.MOD: NumberOperations.mod,
                            Tokens.GREATER: NumberOperations.greater,
                            Tokens.GREATERE: NumberOperations.greater_eq,
                            Tokens.LESS: NumberOperations.less,
                            Tokens.LESSE: NumberOperations.less_eq,
                            Tokens.EQUEL: NumberOperations.equels,
                            Tokens.NEQUEL: NumberOperations.not_equels}
    
    unary_operations = {Tokens.SUB: NumberOperations.neg,
                        Tokens.ADD: NumberOperations.sign}
    
    def __init__(self, value):
        """Initializes the Number object

        Args:
            value (int): the value of the object
        """
        super().__init__(value)
    
    #make it general for all types   
    # def find_op(self, op_token):
    #     op = self.operations.get(op_token.type, None)
    #     if op is None:
    #         return None, TypeError(self.pos_start, self.pos_end, f"Unsupported operand type(s) for {op_token}: '{self.__class__.__name__}'")
    #     else:
    #         return op, None
        
    def find_bin_op(self, op_token):
        """finds the binary operation

        Args:
            op_token (token): the token of the operation

        Returns:
            NumberResult: the result of the operation
        """
        return self.find_op(op_token, self.bin_operations)
    
    def find_unary_op(self, op_token):
        """finds the unary operation

        Args:
            op_token (token): the token of the operation

        Returns:
            NumberResult: the result of the operation
        """
        return self.find_op(op_token, self.unary_operations)
        
    def copy(self):
        """Copies the Number object

        Returns:
            number: the copied Number object
        """
        return Number(self.value, self.pos_start, self.pos_end)
    
    def set_value(self, value):
        """sets the value of the Number object

        Args:
            value (int): the value of the Number object

        Returns:
            object: the Number object
        """
        self.value = value
        return self
    

Number.null = Number(0)
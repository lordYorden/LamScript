from Interpreter.Objects.Object import Object
import Interpreter.Operations.BooleanOperations as BooleanOperation
from Lexer.Tokens import Tokens

class Boolean(Object):
    """the Boolean object class and its operations

    Args:
        Object (object): the base object class
    """
    bin_operations = {Tokens.EQUEL: BooleanOperation.equels, 
                    Tokens.NEQUEL: BooleanOperation.not_equels,
                    Tokens.AND: BooleanOperation.and_op,
                    Tokens.OR: BooleanOperation.or_op,
                    Tokens.NOT: BooleanOperation.not_op,
                    Tokens.ADD: BooleanOperation.add}
    
    unary_operations = {Tokens.NOT: BooleanOperation.not_op}
    
    def __init__(self, value):
        """Initializes the Boolean object

        Args:
            value (boolean): the boolean value of the object
        """
        super().__init__(value)
        
    def find_bin_op(self, op_token):
        """overides the find_bin_op method in the Object class

        Args:
            op_token (token): the token of the operation

        Returns:
            BineryOperation: the binary operation that matches the op_token
        """
        return self.find_op(op_token, self.bin_operations)
        
    def find_unary_op(self, op_token):
        """overides the find_unary_op method in the Object class

        Args:
            op_token (token): the token of the operation

        Returns:
            UnaryOperation: the unary operation that matches the op_token
        """
        return self.find_op(op_token, self.unary_operations)
    
Boolean.true = Boolean(True)
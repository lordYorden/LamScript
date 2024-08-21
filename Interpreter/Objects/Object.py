from Error.RuntimeError import TypeError

class Object: 
    def __init__(self, value=None):
        """Initializes the Object class

        Args:
            value (python object, none): the value of the object. Defaults to None.
        """
        self.value = value
        self.set_pos()
        self.set_context()
        
    def set_pos(self, pos_start=None, pos_end=None):
        """Sets the position of the object

        Args:
            pos_start (position, none): the start position of the object. Defaults to None.
            pos_end (position, none): the end position of the object. Defaults to None.

        Returns:
            object: the object
        """
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def set_context(self, context=None):
        """Sets the context of the object

        Args:
            context (context, none): the context of the object. Defaults to None.

        Returns:
            object: the object
        """
        self.context = context
        return self
    
    def unary_op(self, op_token):
        """Performs a unary operation on the object

        Args:
            op_token (token): the token of the operation

        Returns:
            object, error: the result of the operation and the error    
        """
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
        """Performs a binary operation on the object

        Args:
            op_token (token): the token of the operation
            other (object): the other object

        Returns:
           object, error: the result of the operation and the error   
        """
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
        """finds the binary operation

        Args:
            op_token (token): the token of the operation

        Returns:
            none, TypeError: the result of the operation and the error
        """
        return None, TypeError(self.pos_start, self.pos_end, f"Unsupported operand type(s) for {op_token}: '{'None' if self == Object.none else self.__class__.__name__}'", self.context)
    
    def find_unary_op(self, op_token):
        """finds the unary operation

        Args:
            op_token (token): the token of the operation

        Returns:
            none, TypeError: the result of the operation and the error
        """
        return None, TypeError(self.pos_start, self.pos_end, f"Unsupported operand type(s) for {op_token}: '{'None' if self == Object.none else self.__class__.__name__}'", self.context)
    
    def find_op(self, op_token, operations):
        """finds the operation

        Args:
            op_token (token): the token of the operation
            operations (object): the operations object

        Returns:
            object, none: the result of the operation and the error
        """
        op = operations.get(op_token.type, None)
        if op is None:
            return None, TypeError(self.pos_start, self.pos_end, f"Unsupported operand type(s) for {op_token}: '{self.__class__.__name__}'", self.context)
        else:
            return op, None
        
    def __repr__(self):
        """Return the string representation of the object

        Returns:
            string: the string representation of the object
        """
        return f'{self.value}'.lower() if self.value is not None else ''
    
Object.none = Object()
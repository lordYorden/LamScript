from Interpreter.Objects.Object import Object
class RuntimeResult:
    def __init__(self):
        """Initializes the RuntimeResult object"""
        self.error = None
        self.value = Object.none
        
    def reset(self):
        """Resets the RuntimeResult object to its default state"""
        self.error = None
        self.value = Object.none
        self.func_return_value = Object.none
        self.func_should_return = False
        self.loop_should_continue = False
        self.loop_should_break = False
    
    def register(self, res):
        """Registers the result of a visited node

        Args:
            res (RuntimeResult): the result of a visited node

        Returns:
            Object: the value to be registered
        """
        if res.error: self.error = res.error
        self.func_return_value = res.func_return_value
        self.func_should_return = res.func_should_return
        self.loop_should_continue = res.loop_should_continue
        self.loop_should_break = res.loop_should_break
        return res.value
    
    def success(self, value):
        """Registers a successful result

        Args:
            value (Object): the value to be registered

        Returns:
            RuntimeResult: the current RuntimeResult object
        """
        self.reset()
        self.value = value
        return self
    
    def success_return(self, value):
        """Registers a successful result that should return

        Args:
            value (Object): the value to be registered

        Returns:
            RuntimeResult: the current RuntimeResult object
        """
        self.reset()
        self.func_should_return = True
        self.func_return_value = value
        return self
    
    def success_continue(self):
        """Registers a successful result that should continue

        Returns:
            RuntimeResult: the current RuntimeResult object
        """
        self.reset()
        self.loop_should_continue = True
        return self
    
    def success_break(self):
        """Registers a successful result that should break

        Returns:
            RuntimeResult: the current RuntimeResult object
        """
        self.reset()
        self.loop_should_break = True
        return self
    
    def failure(self, error):
        """Registers a failed result

        Args:
            error (Error): the error to be registered

        Returns:
            RuntimeResult: the current RuntimeResult object
        """
        self.reset()
        self.error = error
        return self
    
    def should_return(self):
        """Returns whether the function should return

        Returns:
            Boolean: dose the function should return
        """
        return self.func_should_return
    
from Interpreter.Objects.Object import Object
from Interpreter.Context import Context
from Interpreter.RuntimeResult import RuntimeResult
from Error.RuntimeError import RunTimeError

class BaseFunction(Object):
    def __init__(self, name):
        """initializes the BaseFunction object

        Args:
            name (string): the name of the function
        """
        super().__init__(name)
        self.name = name
        
    def generate_new_context(self):
        """Generates a new context object

        Returns:
            context: the new context object
        """
        from Interpreter.Context import Context
        context = Context(self.name, self.context, self.pos_start)
        return context
    
    def check_args(self, arg_names, args):
        """Checks if the number of arguments passed into the function is correct

        Args:
            arg_names (string []): list of names of the arguments
            args (object []): list of arguments

        Returns:
            method: the success or failure method
        """
        res = RuntimeResult()
        if len(args) > len(arg_names):
            return res.failure(RunTimeError(self.pos_start, self.pos_end, f"{len(args) - len(arg_names)} too many args passed into '{self.name}'", self.context))
        
        if len(args) < len(arg_names):
            return res.failure(RunTimeError(self.pos_start, self.pos_end, f"{len(arg_names) - len(args)} too few args passed into '{self.name}'", self.context))
        
        return res.success(None)
    
    def populate_args(self, arg_names, args, exec_ctx):
        """Populates the arguments into the symbol table

        Args:
            arg_names (string []): list of names of the arguments
            args (object []): list of arguments
            exec_ctx (context): the current context
        """
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx).set_pos(self.pos_start, self.pos_end)
            exec_ctx.symbol_table.set(arg_name, arg_value)
            
    def check_and_populate_args(self, arg_names, args, exec_ctx):
        """Checks and populates the arguments into the symbol table

        Args:
            arg_names (string []): list of names of the arguments
            args (object []): list of arguments
            exec_ctx (context): the current context

        Returns:
        RuntimeResult: dose the arguments pass the check
        """
        res = RuntimeResult()
        res.register(self.check_args(arg_names, args))
        if res.error: return res
        
        self.populate_args(arg_names, args, exec_ctx)
        return res
    
        
    

    
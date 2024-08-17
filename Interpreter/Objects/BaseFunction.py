from Interpreter.Objects.Object import Object
from Interpreter.Context import Context
from Interpreter.RuntimeResult import RuntimeResult
from Error.RuntimeError import RunTimeError

class BaseFunction(Object):
    def __init__(self, name):
        super().__init__(name)
        
    def generate_new_context(self):
        from Interpreter.Context import Context
        context = Context(self.name, self.context, self.pos_start)
        return context
    
    def check_args(self, arg_names, args):
        
        res = RuntimeResult()
        if len(args) > len(arg_names):
            return res.failure(RunTimeError(self.pos_start, self.pos_end, f"{len(args) - len(arg_names)} too many args passed into '{self.name}'", self.context))
        
        if len(args) < len(arg_names):
            return res.failure(RunTimeError(self.pos_start, self.pos_end, f"{len(arg_names) - len(args)} too few args passed into '{self.name}'", self.context))
        
        return res.success(None)
    
    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx).set_pos(self.pos_start, self.pos_end)
            exec_ctx.symbol_table.set(arg_name, arg_value)
            
    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RuntimeResult()
        res.register(self.check_args(arg_names, args))
        self.populate_args(arg_names, args, exec_ctx)
        return res
    
        
    

    
from Interpreter.Objects.BaseFunction import BaseFunction
from Interpreter.RuntimeResult import RuntimeResult
import os
from Interpreter.Objects.Object import Object

class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)
    
    def execute(self, args):
        res = RuntimeResult()
        new_context = self.generate_new_context()
        
        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_execute_method)
        
        res.register(self.check_and_populate_args(method.arg_names, args, new_context))
        if res.error: return res
        
        return_value = res.register(method(new_context))
        if res.error: return res
        
        return res.success(return_value)
    
    def no_execute_method(self, context):
        res = RuntimeResult()
        return res.failure(RuntimeError(self.pos_start, self.pos_end, f"'{self.name}' is not defined", context))
    
    def execute_print(self, context):
        print(str(context.symbol_table.get('value')))
        return RuntimeResult().success(Object.none)
    execute_print.arg_names = ['value']
    
    def execute_clear(self, context):
        os.system('cls' if os.name == 'nt' else 'clear')
        return RuntimeResult().success(Object.none)
    execute_clear.arg_names = []
    
    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    
    def __str__(self):
        return f"<built-in function {self.name}>"
    
BuiltInFunction.print = BuiltInFunction('print')
BuiltInFunction.clear = BuiltInFunction('clear')
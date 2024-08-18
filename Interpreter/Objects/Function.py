from Interpreter.Objects.Object import Object
# from Interpreter.Context import Context
from Interpreter.Objects.BaseFunction import BaseFunction
import Interpreter.interpreter as Interpreter
# from Error.RuntimeError import RunTimeError

class Function(BaseFunction):
    def __init__(self, name, body_nodes, arg_name, auto_return):
        super().__init__(name)
        self.name = name or "<anonymous>"
        self.body_nodes = body_nodes
        self.arg_name = arg_name
        self.auto_return = auto_return
        
    def execute(self, args):
        res = Interpreter.RuntimeResult()
        interpreter = Interpreter.Interpreter()
        
        res.register(self.check_and_populate_args(self.arg_name, args, self.context))
        if res.error: return res
        
        return_value = Object.none
        for node in self.body_nodes:
            return_value = res.register(interpreter.visit(node, self.context))
            if res.error: return res     
            if res.should_return(): break

        return_value = res.func_return_value or (return_value if self.auto_return else Object.none)
        return res.success(return_value)
    
    def copy(self):
        copy = Function(self.name, self.body_nodes, self.arg_name, self.auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
        
    def __repr__(self):
        return f'<Function {self.name}>'
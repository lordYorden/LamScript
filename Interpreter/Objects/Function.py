from Interpreter.Objects.Object import Object
# from Interpreter.Context import Context
from Interpreter.Objects.BaseFunction import BaseFunction
import Interpreter.interpreter as Interpreter
# from Error.RuntimeError import RunTimeError

class Function(BaseFunction):
    def __init__(self, name, body_node, arg_name):
        super().__init__(name)
        self.name = name or "<anonymous>"
        self.body_node = body_node
        self.arg_name = arg_name
        
    def execute(self, args):
        res = Interpreter.RuntimeResult()
        interpreter = Interpreter.Interpreter()
        
        res.register(self.check_and_populate_args(self.arg_name, args, self.context))
        if res.error: return res
        
        return_value = res.register(interpreter.visit(self.body_node, self.context))
        if res.error: return res
        return res.success(return_value)
    
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
        
    def __repr__(self):
        return f'<Function {self.name}>'
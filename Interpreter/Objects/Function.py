from Interpreter.Objects.Object import Object
from Interpreter.Context import Context
import Interpreter.interpreter as Interpreter
from Error.RuntimeError import RunTimeError

class Function(Object):
    def __init__(self, name, body_node, arg_name):
        super().__init__(name)
        self.name = name
        self.body_node = body_node
        self.arg_name = arg_name
        
    def execute(self, args):
        res = Interpreter.RuntimeResult()
        interpreter = Interpreter.Interpreter()
        
        if len(args) > len(self.arg_name):
            return res.failure(RunTimeError(self.pos_start, self.pos_end, f"{len(args) - len(self.arg_name)} too many args passed into '{self.name}'", self.context))
        
        if len(args) < len(self.arg_name):
            return res.failure(RunTimeError(self.pos_start, self.pos_end, f"{len(self.arg_name) - len(args)} too few args passed into '{self.name}'", self.context))
        
        for i in range(len(args)):
            arg_name = self.arg_name[i]
            arg_value = args[i]
            arg_value.set_context(self.context).set_pos(self.pos_start, self.pos_end)
            self.context.symbol_table.set(arg_name, arg_value)
        
        res = interpreter.visit(self.body_node, self.context)
        if res.error: return res
        
        return res.success(res.value)
    
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
        
    def __repr__(self):
        return f'<Function {self.name}>'
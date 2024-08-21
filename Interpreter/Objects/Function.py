from Interpreter.Objects.Object import Object
# from Interpreter.Context import Context
from Interpreter.Objects.BaseFunction import BaseFunction
import Interpreter.interpreter as Interpreter
# from Error.RuntimeError import RunTimeError

class Function(BaseFunction):
    def __init__(self, name, body_nodes, arg_name, auto_return):
        """initializes the Function object

        Args:
            name (string): the name of the function
            body_nodes (node): the body of the function
            arg_name (string): the name of the argument
            auto_return (boolean): whether the function should return automatically
        """
        super().__init__(name)
        self.name = name or "<anonymous>"
        self.body_nodes = body_nodes
        self.arg_name = arg_name
        self.auto_return = auto_return
        
    def execute(self, args):
        """Executes the function

        Args:
            args (object): the arguments passed into the function

        Returns:
            RuntimeResult: the result of the function execution
        """
        res = Interpreter.RuntimeResult()
        interpreter = Interpreter.Interpreter()
        
        res.register(self.check_and_populate_args(self.arg_name, args, self.context))
        if res.error: return res
        
        return_value = Object.none
        for node in self.body_nodes:
            return_value = res.register(interpreter.visit(node, self.context))
            if res.error: return res     
            if res.should_return(): break

        if self.auto_return:
            return res.success(return_value)
        elif res.should_return():
            return res.success(res.func_return_value)
        else:
            return res.success(Object.none)
    
    def copy(self):
        """Copies the function object

        Returns:
            Function: the copied function object
        """
        copy = Function(self.name, self.body_nodes, self.arg_name, self.auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
        
    def __repr__(self):
        """Return the string representation of the function

        Returns:
            string: the string representation of the function
        """
        return f'<Function {self.name}>'
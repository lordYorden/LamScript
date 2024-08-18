from Interpreter.Objects.Object import Object
class RuntimeResult:
    def __init__(self):
        self.error = None
        self.value = Object.none
        
    def reset(self):
        self.error = None
        self.value = Object.none
        self.func_return_value = Object.none
        self.func_should_return = False
        self.loop_should_continue = False
        self.loop_should_break = False
    
    def register(self, res):
        if res.error: self.error = res.error
        self.func_return_value = res.func_return_value
        self.func_should_return = res.func_should_return
        self.loop_should_continue = res.loop_should_continue
        self.loop_should_break = res.loop_should_break
        return res.value
    
    def success(self, value):
        self.reset()
        self.value = value
        return self
    
    def success_return(self, value):
        self.reset()
        self.func_should_return = True
        self.func_return_value = value
        return self
    
    def success_continue(self):
        self.reset()
        self.loop_should_continue = True
        return self
    
    def success_break(self):
        self.reset()
        self.loop_should_break = True
        return self
    
    def failure(self, error):
        self.reset()
        self.error = error
        return self
    
    def should_return(self):
        return self.func_should_return #self.func_return_value != Object.none
    
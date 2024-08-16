from Interpreter.Objects.Number import Number
from Interpreter.Objects.Boolean import Boolean
from Interpreter.Objects.Object import Object
from Interpreter.RuntimeResult import RuntimeResult
from Error.RuntimeError import RunTimeError

class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        mehtod = getattr(self, method_name, self.no_visit_method)
        return mehtod(node, context)
    
    def no_visit_method(self, node, context):
        res = RuntimeResult()
        return res.failure(RunTimeError(node.pos_start, node.pos_end, f'No visit_{type(node).__name__} method defined', context))
    
    def visit_NumberNode(self, node, context):
        res = RuntimeResult()
        return res.success(Number(node.token.value).set_pos(node.pos_start, node.pos_end).set_context(context))
    
    def visit_BooleanNode(self, node, context):
        res = RuntimeResult()
        return res.success(Boolean(node.token.value).set_pos(node.pos_start, node.pos_end).set_context(context))
    
    def visit_BinOpNode(self, node, context):
        res = RuntimeResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return None, res.error
        
        right = res.register(self.visit(node.right_node, context))
        if res.error: return None, res.error
        
        object, error = left.bin_op(node.op_token, right)
        if error: return res.failure(error)
        
        return res.success(object.set_pos(node.pos_start, node.pos_end))
        
    def visit_UnaryOpNode(self, node, context):
        res = RuntimeResult()
        object = res.register(self.visit(node.node, context))
        if res.error: return None, res.error
        
        object, error = object.unary_op(node.op_token)
        if error: return res.failure(error)
        
        return res.success(object.set_pos(node.pos_start, node.pos_end))
    
    def visit_SymbolAcsessNode(self, node, context):
        res = RuntimeResult()
        sym_name = node.identifier_token.value
        value = context.symbol_table.get(sym_name)
        
        if not value:
            return res.failure(RunTimeError(node.pos_start, node.pos_end, f"'{sym_name}' is not defined", context))
        return res.success(value.set_pos(node.pos_start, node.pos_end).set_context(context))
    
    def visit_whileNode(self, node, context):
        res = RuntimeResult()
        while True:
            condition_value = res.register(self.visit(node.condition_node, context))
            if res.error: return None, res.error
            
            if not condition_value:
                break
            
            value = res.register(self.visit(node.body_node, context))
            if res.error: return None, res.error
            #for debugging
            print(value)
        
        return res.success(None)
        
        
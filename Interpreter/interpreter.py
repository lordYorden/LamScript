from Interpreter.Objects.Number import Number
from Interpreter.Objects.Boolean import Boolean
from Interpreter.Objects.Object import Object
from Interpreter.RuntimeResult import RuntimeResult
from Error.RuntimeError import RunTimeError
from Interpreter.Objects.Function import Function
from Interpreter.Context import Context
from Lexer.Tokens import Tokens

class Interpreter:
    def visit(self, node, context):
        """Visits an Abstract Syntax Tree node

        Args:
            node (BaseNode): the node to visit
            context (Context): the current context of the program

        Returns:
            RuntimeResult: the result of the visit
        """
        method_name = f'visit_{type(node).__name__}'
        mehtod = getattr(self, method_name, self.no_visit_method)
        return mehtod(node, context)
    
    def no_visit_method(self, node, context):
        """Handles the case where no visit method is defined

        Args:
            node (BaseNode): the node to visit
            context (Context): the current context of the program

        Returns:
            RuntimeResult: the result of the visit
        """
        res = RuntimeResult()
        return res.failure(RunTimeError(node.pos_start, node.pos_end, f'No visit_{type(node).__name__} method defined', context))
    
    def visit_NumberNode(self, node, context):
        """Visits a Number Node

        Args:
            node (BaseNode): the node to visit
            context (Context): the current context of the program

        Returns:
            RuntimeResult: the result of the visit
        """
        res = RuntimeResult()
        return res.success(Number(node.token.value).set_pos(node.pos_start, node.pos_end).set_context(context))
    
    def visit_BooleanNode(self, node, context):
        """Visits a Boolean Node

        Args:
            node (BaseNode): the node to visit
            context (Context): the current context of the program

        Returns:
            RuntimeResult: the result of the visit
        """
        res = RuntimeResult()
        return res.success(Boolean(node.token.value).set_pos(node.pos_start, node.pos_end).set_context(context))
    
    def visit_BinOpNode(self, node, context):
        """Visits a Binary Operation Node
        Handles Short-circuit evaluation for the OR and AND operators

        Args:
            node (BaseNode): the node to visit
            context (Context): the current context of the program

        Returns:
            RuntimeResult: the result of the visit
        """
        res = RuntimeResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        
        if node.op_token.type == Tokens.OR:
            if isinstance(left,Boolean) and left.value == True:
                return res.success(left)
        if node.op_token.type == Tokens.AND:
            if isinstance(left,Boolean) and left.value == False:
                return res.success(left)
                
        
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res
        
        object, error = left.bin_op(node.op_token, right)
        if error: return res.failure(error)
        
        return res.success(object.set_pos(node.pos_start, node.pos_end))
        
    def visit_UnaryOpNode(self, node, context):
        """Visits a Unary Operation Node

        Args:
            node (BaseNode): the node to visit
            context (Context): the current context of the program

        Returns:
            RuntimeResult: the result of the visit
        """
        res = RuntimeResult()
        object = res.register(self.visit(node.node, context))
        if res.error: return res
        
        object, error = object.unary_op(node.op_token)
        if error: return res
        
        return res.success(object.set_pos(node.pos_start, node.pos_end))
    
    def visit_SymbolAcsessNode(self, node, context):
        """Visits a Symbol Access Node

        Args:
            node (BaseNode): the node to visit
            context (Context): the current context of the program

        Returns:
            RuntimeResult: the result of the visit
        """
        res = RuntimeResult()
        sym_name = node.identifier_token.value
        value = context.symbol_table.get(sym_name)
        
        if not value:
            return res.failure(RunTimeError(node.pos_start, node.pos_end, f"'{sym_name}' is not defined", context))
        return res.success(value.set_pos(node.pos_start, node.pos_end).set_context(context))
    
    def visit_whileNode(self, node, context):
        """Visits a While Node checks for break and continue statements

        Args:
            node (BaseNode): the node to visit
            context (Context): the current context of the program

        Returns:
            RuntimeResult: the result of the visit
        """
        res = RuntimeResult()
        while True:
            condition_value = res.register(self.visit(node.condition_node, context))
            if res.error: return res.failure(res.error)
            
            if not condition_value.value:
                break
            
            continue_loop = False
            
            for n in node.body_nodes:
                value = res.register(self.visit(n, context))
                if res.error: return res
                
                if res.should_return():
                    return res
                elif res.loop_should_break:
                    return res.success(Object.none)
                elif res.loop_should_continue:
                    continue_loop = False
                    break
                
            if continue_loop:
                continue_loop = False
                continue
        
        return res.success(Object.none)
    
    def visit_FuncDefNode(self, node, context):
        """Visits a Function Definition Node

        Args:
            node (BaseNode): the node to visit
            context (Context): the current context of the program

        Returns:
            RuntimeResult: the result of the visit
        """
        res = RuntimeResult()
        function_name = node.identifier_token.value if node.identifier_token else None
        arg_name = [arg_name.get_token().value for arg_name in node.arg_nodes]
        body_nodes = node.body_nodes
        
        function_value = Function(function_name, body_nodes, arg_name, node.auto_return).set_context(context).set_pos(node.pos_start, node.pos_end)
        
        if function_name:
            context.symbol_table.set(function_name, function_value)
        return res.success(function_value)
    
    def visit_FuncCallNode(self, node, context):
        """Visits a Function Call Node

        Args:
            node (BaseNode): the node to visit
            context (Context): the current context of the program

        Returns:
            RuntimeResult: the result of the visit
        """
        res = RuntimeResult()
        args = []
        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error: return res
        
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)
        new_context = Context(value_to_call.value, context, node.pos_start)
        value_to_call.set_context(new_context)
        
        for arg_node in node.arg_nodes:
            arg = res.register(self.visit(arg_node,new_context))
            if res.error: return res
            args.append(arg)
        
        return_value = res.register(value_to_call.execute(args))
        if res.error: return res
        
        return res.success(return_value.set_pos(node.pos_start, node.pos_end).set_context(new_context))
    
    def visit_ReturnNode(self, node, context):
        """Visits a Return Node

        Args:
            node (BaseNode): the node to visit
            context (Context): the current context of the program

        Returns:
            RuntimeResult: the result of the visit
        """
        res = RuntimeResult()
        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.error: return res
        else:
            value = Object.none
        
        return res.success_return(value)
    
    def visit_ContinueNode(self, node, context):
        """Visits a Continue Node

        Args:
            node (BaseNode): the node to visit
            context (Context): the current context of the program

        Returns:
            RuntimeResult: the result of the visit
        """
        return RuntimeResult().success_continue()
    
    def visit_BreakNode(self, node, context):  
        """Visits a Break Node

        Args:
            node (BaseNode): the node to visit
            context (Context): the current context of the program

        Returns:
            RuntimeResult: the result of the visit
        """
        return RuntimeResult().success_break()
        
        
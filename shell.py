from Lexer.lexer import Lexer
from Parser.parser import Parser
from Interpreter.interpreter import Interpreter
from Interpreter.Context import Context
from Interpreter.SymbolTable import SymbolTable
from Interpreter.Objects.Number import Number
from Interpreter.Objects.BuiltInFunction import BuiltInFunction
from Interpreter.Objects.Object import Object
import sys

VERSION = "1.0.0"
FILE_EXTENSION = ".ls"
run_line_by_line = False

def main():
    global run_line_by_line
    if len(sys.argv) > 1:
        
        if sys.argv[1] == "-l":
            run_line_by_line = True
            if len(sys.argv) > 2:
                fn = sys.argv[2]
            else:
                print("Error! No file was specified")
                return
        else:
            fn = sys.argv[1]
        
        if not fn.endswith(FILE_EXTENSION):
            print(f"Invalid file type file must end with {FILE_EXTENSION} file")
            return
        elif run_line_by_line:
             print(f"Running {fn} file in line by line mode:")
        else:
            print(f"Running {fn} file (for a line by line use: -l {fn}):")
        
        file = open(fn, 'r')
        ftx = file.read()
        result,error = run(f'<{fn}>', ftx)
        if error:
            print(error.as_string())
        elif result != Object.none:
            print(result)
        return
    else:
        print(f"LamScript v{VERSION}")
        print("Type 'clear' to clear the screen")
        print("Type 'exit' to exit the shell")
        while True:
            command = input('LamScript> ')
            result,error = run('<stdin>',command)
            if error:
                print(error.as_string())
            elif result != Object.none:
                print(result)
            

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null)
global_symbol_table.set("none", Object.none)
global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("clear", BuiltInFunction.clear)
global_symbol_table.set("exit", BuiltInFunction.exit)
global_symbol_table.set("x", Number(10)) #for testing

def run(fn, text):
    global run_line_by_line
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    
    #print("finshed lexing")
    #print(tokens)
    
    #parse tree
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error
    
    #print(ast.node)

    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    
    result = Object.none
    if isinstance(ast.node, list):
        for node in ast.node:
            
            if run_line_by_line:
                #print(node)
                print(node.get_statement_text())
                print("result: ", end="")
                
            result = interpreter.visit(node, context)
            if result.error: break
            
            if run_line_by_line:
                if result.value != Object.none:
                    print(result.value)
                sys.stdout.flush()
                input("\nPress Enter to move to the next statement...\n")

    else:
        result = interpreter.visit(ast.node, context)
        
    return result.value, result.error

if __name__ == '__main__':
    main()
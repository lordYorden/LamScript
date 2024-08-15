from Lexer.lexer import Lexer
from Parser.parser import Parser
from Interpreter.interpreter import Interpreter
from Interpreter.Context import Context

def main():
    while True:
        command = input('LamScript> ')
        result,error = run('<stdin>',command)
        if error:
            print(error.as_string())
        else:
            print(result)
            

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    
    #print("finshed lexing")
    print(tokens)
    
    #parse tree
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error
    
    print(ast.node)
    
    interpreter = Interpreter()
    context = Context('<program>')
    result = interpreter.visit(ast.node, context)
    
    return result.value, result.error

if __name__ == '__main__':
    main()
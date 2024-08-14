from Lexer.lexer import Lexer
from Parser.parser import Parser
from Interpreter.interpreter import Interpreter

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
    object, error = interpreter.visit(ast.node)
    if error:
        return None, error
    
    return object, None

if __name__ == '__main__':
    main()
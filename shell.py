from Lexer.lexer import Lexer
from Parser.parser import Parser

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
    
    return ast.node, ast.error

if __name__ == '__main__':
    main()
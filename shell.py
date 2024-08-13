import Lexer.lexer as Lexer

def main():
    while True:
        command = input('LamScript> ')
        result,error = Lexer.run('<stdin>',command)
        if error:
            print(error.as_string())
        else:
            print(result)

if __name__ == '__main__':
    main()
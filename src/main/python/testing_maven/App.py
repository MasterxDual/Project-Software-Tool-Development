import sys
from antlr4 import *
from compiladoresLexer  import compiladoresLexer
from compiladoresParser import compiladoresParser
from TheListener import TheListener

def main(argv):
    archivo = "input/programa.txt"
    if len(argv) > 1 :
        archivo = argv[1]
    input = FileStream(archivo)
    lexer = compiladoresLexer(input)
    stream = CommonTokenStream(lexer)
    parser = compiladoresParser(stream)
    listen = TheListener()
    parser.addParseListener(listen)
    tree = parser.program()
    #print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main(sys.argv)
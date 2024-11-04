#https://github.com/MasterxDual
#https://github.com/MasterxDual/Project-Software-Tool-Development

import sys
from antlr4 import *
from compiladoresLexer  import compiladoresLexer
from compiladoresParser import compiladoresParser
from TheListener import TheListener
from Walker import Walker

def main(argv):
    archivo = "input/test.txt"
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
    #walker = Walker()
    #walker.visitProgram(tree)

if __name__ == '__main__':
    main(sys.argv)
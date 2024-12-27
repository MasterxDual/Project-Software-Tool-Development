#https://github.com/MasterxDual
#https://github.com/MasterxDual/Project-Software-Tool-Development

import sys
from antlr4 import *
from compiladoresLexer  import compiladoresLexer
from compiladoresParser import compiladoresParser
from TheListener import TheListener
from Walker import Walker

def main(argv):
    archivo = "input/opal.txt"
    if len(argv) > 1 :
        archivo = argv[1]
    input = FileStream(archivo) #Entradas de codigo fuente
    lexer = compiladoresLexer(input) #Analizador lexico y consume los caracteres del codigo fuente
    stream = CommonTokenStream(lexer) #Tokens (Secuencia)
    parser = compiladoresParser(stream) #Analizador Sintactico se alimenta con los tokens strings
    listen = TheListener() #Escucha eventos de arbol
    parser.addParseListener(listen) #Los eventos de arbol se los informo al parser
    tree = parser.program() #Empieza por la regla 'programa' (la raiz del arbol) y nos devuelve un arbol sintactico, el parser es el que dirige o guia
    #print(tree.toStringTree(recog=parser)) #Arbol gramatical
    walker = Walker() #Construye el objeto Walker
    walker.visitProgram(tree) #Le pasa el arbol para que comience a caminar sobre el arbol terminado

if __name__ == '__main__':
    main(sys.argv)
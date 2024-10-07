from antlr4 import ErrorNode, TerminalNode
from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser

class TheListener(compiladoresListener):
    tokensNum = 0
    nodeNum = 0

    def enterProgram(self, ctx:compiladoresParser.ProgramContext):
        print("Comienza la compilacion")

    def exitProgram(self, ctx:compiladoresParser.ProgramContext):
        print("Fin de la compilacion")
        print("Se encontraron:")
        print("\tNodos: " + str(self.nodeNum))
        print("\tTokens: " + str(self.tokensNum))

    def enterWhilei(self, ctx:compiladoresParser.WhileiContext):
        print("Encontre while")
        print("\tCantidad hijos: " + str(ctx.getChildCount()))
        print("\tTokens: " + ctx.getText())

    def exitWhilei(self, ctx:compiladoresParser.WhileiContext):
        print("Fin del while")
        print("\tCantidad hijos: " + str(ctx.getChildCount()))
        print("\tTokens: " + ctx.getText())

    def enterDeclaration(self, ctx:compiladoresParser.DeclarationContext):
        print(" ### Declaracion")

    def exitDeclaration(self, ctx:compiladoresParser.DeclarationContext):
        print("Nombre variable: " + ctx.getChild(1).getText())

    def visitTerminal(self, node: TerminalNode):
        print(" ---> Token: " + node.getText())

    def visitErrorNode(self, node: ErrorNode):
        print(" ---> ERROR")
    def enterEveryRule(self, ctx):
        self.nodeNum += 1
from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser

class Walker(compiladoresVisitor):
    def visitProgram(self, ctx: compiladoresParser.ProgramContext):
        print("=-" * 20)
        print("-- Comienza a caminar")
        return super().visitProgram(ctx)
    
    def visitBlock(self, ctx: compiladoresParser.BlockContext):
        print("Nuevo contexto")
        print(ctx.getText())
        return super().visitInstructions(ctx.getChild(1))
    
    def visitDeclaration(self, ctx: compiladoresParser.DeclarationContext):
        print(ctx.getChild(0).getText() + " - " + ctx.getChild(1).getText())
        return None
    
    #def visitTerminal(self, node):
    #   print(" ==>> Token " + node.getText())
    #    return super().visitTerminal(node)
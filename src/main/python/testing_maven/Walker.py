from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser

class Temporal():
    def __init__(self):
        self.contador = -1

    def get_temporal(self):
        self.contador += 1
        return f't{self.contador}'

class Walker(compiladoresVisitor):
    _temporales             = []
    _etiquetas              = []
    _identificadores        = []
    generadorDeTemporales   = Temporal()
    
    def visitProgram(self, ctx: compiladoresParser.ProgramContext):
        print("-" + "=" * 30 + "-")
        print("-- Comienza a generar Codigo Intermedio --")
        self.file = open("./output/codigoIntermedio.txt", "w")

        self.visitInstructions(ctx.getChild(0))

        self.file.close()
        print("-- Codigo Intermedio generado Correctamente --")
        print("-" + "=" * 30 + "-")

    # Visit a parse tree produced by compiladoresParser#instrucciones.
    def visitInstructions(self, ctx:compiladoresParser.InstructionsContext):
        self.visitInstruction(ctx.getChild(0))

        if ctx.getChild(1).getChildCount() != 0:
            self.visitInstructions(ctx.getChild(1))

        if ctx.getChildCount() == 0:
            return
    
    # Visit a parse tree produced by compiladoresParser#instruccion.
    def visitInstruction(self, ctx:compiladoresParser.InstructionContext):
        if isinstance (ctx.getChild(0), compiladoresParser.DeclarationContext):
            self.visitDeclaration(ctx.getChild(0))
        elif isinstance (ctx.getChild(0), compiladoresParser.AssignmentContext):
            self.visitAssignment(ctx.getChild(0))
        else:
            return

    # Visit a parse tree produced by compiladoresParser#declaracion.
    def visitDeclaration(self, ctx:compiladoresParser.DeclarationContext):
        self._identificadores.append(ctx.getChild(1).getText())
        if ctx.getChild(2).getChildCount() != 0:
            self.visitDefinition(ctx.getChild(2))
        else:
            return

    # Visit a parse tree produced by compiladoresParser#definicion.
    def visitDefinition(self, ctx:compiladoresParser.DefinitionContext):
        self.visitOpal(ctx.getChild(1))
        return

    # Visit a parse tree produced by compiladoresParser#opal.
    def visitOpal(self, ctx:compiladoresParser.OpalContext):
        self.visitOplogic(ctx.getChild(0))
        return

    # Visit a parse tree produced by compiladoresParser#oplogicos.
    def visitOplogic(self, ctx:compiladoresParser.OplogicContext):
        self.visitLogic(ctx.getChild(0))
        return

    # Visit a parse tree produced by compiladoresParser#logico.
    def visitLogic(self, ctx:compiladoresParser.LogicContext):
        self.visitSet(ctx.getChild(0))
        return

    # Visit a parse tree produced by compiladoresParser#conjunto.
    def visitSet(self, ctx:compiladoresParser.SetContext):
        self.visitC(ctx.getChild(0))
        return

    # Visit a parse tree produced by compiladoresParser#c.
    def visitC(self, ctx:compiladoresParser.CContext):
        self.visitExp(ctx.getChild(0))
        return

    # Visit a parse tree produced by compiladoresParser#exp.
    def visitExp(self, ctx:compiladoresParser.ExpContext):
        self.visitTerm(ctx.getChild(0))
        return

    # Visit a parse tree produced by compiladoresParser#term.
    def visitTerm(self, ctx:compiladoresParser.TermContext):
        self.visitFactor(ctx.getChild(0))
        return

    # Visit a parse tree produced by compiladoresParser#factor.
    def visitFactor(self, ctx:compiladoresParser.FactorContext):
        if ctx.getChildCount() == 1:
            id = self._identificadores.pop()
            self.file.write(id + '=' + ctx.getChild(0).getText() + '\n')
            return

    # Visit a parse tree produced by compiladoresParser#asignacion.
    def visitAssignment(self, ctx:compiladoresParser.AssignmentContext):
        self._identificadores.append(ctx.getChild(0).getText())
        self.visitOpal(ctx.getChild(2))
        # Cuando la asignacion no es directa (uso temporales)
        return
    
    # def visitDeclaration(self, ctx: compiladoresParser.DeclaracionContext):
    #     # No accede mediante el 'super()' sino mediante el metodo para obtener los hijos (nodos del arbol)
    #     print(ctx.getChild(0).getText() + " - " +   # Quiero ver el tipo de dato
    #           ctx.getChild(1).getText())            # Quiero ver el ID

    #     # return super().visitDeclaration(ctx)
    #     return None

    # def visitBloque(self, ctx: compiladoresParser.BloqueContext):
    #     print("Nuevo Contexto")
    #     print(ctx.getText())
    #     return super().visitInstructions(ctx.getChild(1))
    #     # return super().visitBloque(ctx)

    # def visitTerminal(self, node):
    #     print(" ==> Token " + node.getText())
    #     return super().visitTerminal(node)
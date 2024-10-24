from antlr4 import ErrorNode, TerminalNode
from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser
from SymbolTable import SymbolTable
from Id import DataType
from Variable import Variable
class TheListener(compiladoresListener):
    tokensNum = 0
    nodeNum = 0
    variablesStack = []

    def enterProgram(self, ctx:compiladoresParser.ProgramContext):
        print("Comienza la compilacion")
        self.instance_symbol_table = SymbolTable()
        self.instance_symbol_table.add_context()

    def exitProgram(self, ctx:compiladoresParser.ProgramContext):
        print("Fin de la compilacion")
        print("Se encontraron:")
        print("\tNodos: " + str(self.nodeNum))
        print("\tTokens: " + str(self.tokensNum))
        print(self.instance_symbol_table)

    def enterBlock(self, ctx: compiladoresParser.BlockContext):
        self.instance_symbol_table.add_context()

    def exitBlock(self, ctx: compiladoresParser.BlockContext):
        self.instance_symbol_table.del_context()

    def enterDeclaration(self, ctx:compiladoresParser.DeclarationContext):
        print(" ### Declaration. Adding a new symbol into the symbol table...")
        
    def exitDeclaration(self, ctx:compiladoresParser.DeclarationContext):
        id_name = ctx.getChild(1).getText()
        data_type = ctx.getChild(0).getText().upper()
            
        self.current_data_type = data_type
        self.instance_symbol_table.add_identifier(Variable(id_name, DataType[data_type]))
        for _ in range(len(self.variablesStack)):
            self.instance_symbol_table.add_identifier(Variable(self.variablesStack.pop(), DataType[data_type]))


    def exitVarlist(self, ctx: compiladoresParser.VarlistContext):
        if(ctx.getChildCount() != 0):
            self.variablesStack.append(ctx.getChild(1).getText())
            
    #def enterWhilei(self, ctx:compiladoresParser.WhileiContext):
    #    print("Encontre while")
    #    print("\tCantidad hijos: " + str(ctx.getChildCount()))
    #    print("\tTokens: " + ctx.getText())

    #def exitWhilei(self, ctx:compiladoresParser.WhileiContext):
    #    print("Fin del while")
    #    print("\tCantidad hijos: " + str(ctx.getChildCount()))
    #    print("\tTokens: " + ctx.getText()) """

    def visitTerminal(self, node: TerminalNode):
        print(" ---> Token: " + node.getText())

    def visitErrorNode(self, node: ErrorNode):
        print(" ---> ERROR")
    def enterEveryRule(self, ctx):
        self.nodeNum += 1
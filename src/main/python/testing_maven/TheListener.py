from antlr4 import ErrorNode, TerminalNode
from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser
from SymbolTable import SymbolTable
from Id import DataType
from Variable import Variable
from Context import Context
class TheListener(compiladoresListener):
    """
    Clase que implementa el listener para el analizador sintáctico. 
    """

    variables_dict = {} #Diccionario para almacenar variables temporales
    symbol_table = SymbolTable()  #Instancia de la tabla de símbolos
    errors = [] #Lista para almacenar errores encontrados
    warnings = [] #Lista para almacenar advertencias encontradas

    def bugReport(self, ctx, type_error:str, message:str):
        """
        Genera un reporte de errores para el compilador

        Este método se encarga de registrar los errores encontrados durantex
        el proceso de compilación. Se extrae la línea del contexto donde
        ocurrió el error y se agrega un mensaje de error a la lista de errores.

        Parámetros:
            - ctx: El contexto del error, que contiene información sobre la ubicación del error.
            - type_error: Una cadena que indica el tipo de error ("Sintáctico", "Semántico").
            - message: Un message descriptivo que explica el error.
        """
        line = ctx.start.line # Obtiene el número de línea donde ocurrió el error desde el contexto
        self.errors.append(f"Error {type_error} en la linea {line}: {message}") # Agrega un mensaje de error a la lista de errores, incluyendo el tipo y la línea

    def warningReport(self, ctx, message:str):
        """
        Genera un reporte de advertencias para el compilador
        """
        
        line = ctx.start.line # Obtiene el número de línea donde se controno la advertencia desde el contexto
        self.warnings.append(f"Advertencia en la linea {line}: {message}") # Agrega un mensaje de advertencia a la lista de advertencias, incluyendo la línea        

    def enterProgram(self, ctx:compiladoresParser.ProgramContext):
        """
        Método que se ejecuta al entrar en el contexto de la regla "programa".
        Inicializa el contexto global y comienza el proceso de compilación.
        """

        print("\n+" + "="*10, "Comienza la Compilacion", "="*10 + "+\n")
        global_context = Context()                          # Crea el contexto global
        self.symbol_table.add_context(global_context) # Agrega el contexto global (primer contexto) a la tabla de simbolos

    def exitProgram(self, ctx:compiladoresParser.ProgramContext):
        """
        Método que se ejecuta al salir del contexto de la regla "programa".
        Finaliza el proceso de compilación y muestra los reportes de errores y advertencias.
        """
        print("\n+" + "="*10, "Fin de la Compilacion", "="*10 + "+\n")
        self.symbol_table.del_context() # Borra el contexto global (Ultimo contexto restante)

        # Muestra el reporte de Errores
        if self.errors:
            print("\nSe encontraron los siguientes errores:")
            for error in self.errors:
                print(error)
        else:
            print("Compilación exitosa. No se encontraron errores.")

        # Muestra el reporte de Advertencias
        if self.warnings:
            print("\nAdvertencias a tener en cuenta:")
            for warning in self.warnings:
                print(warning)
        else:
            print("No aparecieron advertencias.")

        # Muestra la tabla de simbolos
        print(self.symbol_table) 

    def exitInstruccion(self, ctx:compiladoresParser.InstruccionContext):
        """
        Método que se ejecuta al salir del contexto de la regla "instruccion".
        Verifica si la instrucción termina con un punto y coma.
        """

        # Verifica si el contexto corresponde a uno de estos tipos de instrucción válidos
        if (ctx.declaration() or ctx.assignment() or ctx.returning() or ctx.function_prototype() or ctx.function_call()):
            if ctx.getChild(1).getText() != ';': # Si no termina con ';' muestra un error
                self.bugReport(ctx, "Sintactico", "se esperaba ';'")
        

    def enterBlock(self, ctx: compiladoresParser.BlockContext):
        """
        Método que se ejecuta al entrar en el contexto de la regla "bloque".
        Crea un nuevo contexto para las variables locales.
        """

        new_context = Context() # Crea un nuevo Contexto
        self.symbol_table.add_context(new_context) # Agrega un nuevo Contexto a la tabla de simbolos

    def exitBlock(self, ctx: compiladoresParser.BlockContext):
        """
        Método que se ejecuta al salir del contexto de la regla "bloque".
        Verifica las variables no inicializadas y no usadas en el bloque.
        """
        #Obtenemos todos los contextos de la tabla de simbolos
        contexts = self.symbol_table.get_contexts()

        # Recorremos el contexto actual en busca de ID no inicializados y/o usados
        for variable in contexts[-1].get_identifiers().values():
            if variable.get_initialized() is False: # Si no esta inicializado
                self.warningReport(ctx, f"La variable '{variable.obtenerNombre()}' no fue inicialzada")
            if variable.get_used() is False: # Si no esta usado
                self.warningReport(ctx, f"La variable '{variable.obtenerNombre()}' no fue usada")

        self.symbol_table.del_context() # Borra el contexto actual

    def enterDeclaration(self, ctx:compiladoresParser.DeclarationContext):
        print(" ### Declaration. Adding a new symbol into the symbol table...")
        
    def exitDeclaration(self, ctx:compiladoresParser.DeclarationContext):
        """
        Maneja la salida de un contexto de declaración de variables.

        Verifica si la variable ya está declarada en el ámbito local. Si no lo está,
        crea la variable y la agrega a la tabla de símbolos. También maneja la 
        declaración de múltiples variables en una sola instrucción.
        """
        # Verifica si la variable ya está declarada en el ámbito local
        if self.symbol_table.local_search(ctx.getChild(1).getText()) is None:
            data_type = str(ctx.getChild(0).getText().upper()) # Obtiene el tipo de dato y lo convierte a mayúsculas
            id_name = str(ctx.getChild(1).getText()) # Obtiene el nombre de la variable
            variable = Variable(id_name, data_type) # Crea un objeto Variable con el nombre y tipo de dato
            self.symbol_table.add_identifier(variable) # Agrega la variable a la tabla de símbolos en el contexto actual

            # Para validar si realmente se estan agregando los ID's a la tabla de contextos en su contexto correspondiente
            print(f"Nueva variable: '{self.symbol_table.local_search(id_name).name}'" + 
                f" de tipo '{data_type}' agregada.\n")

            if str(ctx.getChild(2).getText()) != '': # Si el 3er hijo en la declaracion es distinto de vacio, existe una definicion
                variable.set_initialized() # Marca la variable como inicializada si se proporciona un valor

            # Maneja la declaración de múltiples variables (si es necesario)
            if self.variables_dict:
                while self.variables_dict:
                    new_variable, is_initialized = self.variables_dict.popitem()

                    # Verifica si la variable ya ha sido declarada en el ámbito local
                    if self.symbol_table.local_search(new_variable) is None:
                        variable = Variable(new_variable, data_type)
                        self.symbol_table.add_identifier(variable)

                        # Para validar si realmente se estan agregando los ID's a la tabla de contextos en su contexto correspondiente
                        print(f"Nueva variable: '{self.symbol_table.local_search(variable.name).name}'" + 
                            f" de tipo '{data_type}' agregada.\n")
                        
                        if is_initialized:  #Marca la variable como inicializada si es True
                            variable.set_initialized()
                    else:
                        #Error si la variable ya fue declarada
                        self.bugReport(ctx, "Semantico", f"El identificador '{ctx.getChild(1).getText()}' ya esta definido en este bloque")
                        return
        else:
            # Imprime un mensaje de error si la variable ya fue declarada
            self.bugReport(ctx, "Semantico", f"El identificador '{ctx.getChild(1).getText()}' ya esta definido en este bloque")
            return
        
        self.variables_dict.clear() # Para vaciar la pila de nombres de variables después de procesar la declaración.



    def exitVarlist(self, ctx: compiladoresParser.VarlistContext):
        """
        Maneja la salida de un contexto de lista de variables.
        """
        if ctx.getChildCount():
            if str(ctx.getChild(2).getText()) != '': # Si el tercer hijo en la lista de variables es distinto de vacio, existe definicion
                self.variables_dict.update({ctx.getChild(1).getText(): True})
                # El dict almacena el nombre de la var como nombre y si esta inicializada con valor (True o False)
            else:
                self.variables_dict.update({ctx.getChild(1).getText(): False})

            
    def exitAssignment(self, ctx: compiladoresParser.AssignmentContext):
        """
        Maneja la salida de un contexto de asignación.
        """
        identifier = self.symbol_table.global_search(ctx.getChild(0).getText())
        if identifier is None: # Si el identificador no existe en la tabla de simbolos
            # Notifica el uso de un ID sin declarar
            self.bugReport(ctx, "Semantico", f"El identificador '{ctx.getChild(0).getText()}' no esta definido")
            return

        # Verifica si el valor asignado es correcto
        if ctx.getChild(2) == ctx.opal():
            identifier.set_initialized() # Se inicializa la variable

    """ ------------------------------------------------------------------------------------ """

    def exitWhilei(self, ctx:compiladoresParser.WhileiContext):
        """
        Maneja la salida de un contexto de while.
        """
        if ctx.getChild(1).getText() != '(':
            self.bugReport(ctx, "Sintactico", "Falta parentesis de apertura")
            return
        
        if ctx.getChild(3).getText() != ')':
            self.bugReport(ctx, "Sintactico", "Falta parentesis de cierre")
        

    def exitFori(self, ctx: compiladoresParser.ForiContext):
        """
        Maneja la salida de un contexto de for.
        """
        if ctx.getChild(1).getText() != '(':
            self.bugReport(ctx, "Sintactico", "Falta parentesis de apertura")
            return
        
        if ctx.getChild(7).getText() != ')':
            self.bugReport(ctx, "Sintactico", "Falta parentesis de cierre")

    def exitIfi(self, ctx: compiladoresParser.IfiContext):
        """
        Maneja la salida de un contexto de if.
        """
        if ctx.getChild(1).getText() != '(':
            self.bugReport(ctx, "Sintactico", "Falta parentesis de apertura")
            return
        
        if ctx.getChild(3).getText() != ')':
            self.bugReport(ctx, "Sintactico", "Falta parentesis de cierre")
        
    def exitFunction_call(self, ctx: compiladoresParser.Function_callContext):
        """
        Maneja la salida de un contexto de llamada a funcion.
        """
        if ctx.getChild(1).getText() != '(':
            self.bugReport(ctx, "Sintactico", "Falta parentesis de apertura")
            return
        
        if ctx.getChild(3).getText() != ')':
            self.bugReport(ctx, "Sintactico", "Falta parentesis de cierre")


    def exitFactor(self, ctx:compiladoresParser.FactorContext):
        """
        Maneja la salida de un contexto de factor.
        """
        if ctx.ID(): # Si el factor es un ID 
            identifier = self.symbol_table.global_search(ctx.getChild(0).getText()) # Busca el ID en la tabla de símbolos
            if identifier is None:
                # Notifica el uso de un ID sin declarar
                self.bugReport(ctx, "Semantico", f"El identificador '{ctx.getChild(0).getText()}' no esta definido")
                return
            else: #Si el ID fue declarado actualiza su estado a usado en caso que no lo este
                self.symbol_table.update_used(identifier.name)

        # Manejo de parentesis en operaciones logicas:
        if ctx.LPAR() and ctx.getChild(2).getText() != ')':
            self.bugReport(ctx, "Semantico", "Falta de cierre de parentesis")
            return
        
        if ctx.RPAR() and ctx.getChild(0).getText() != '(':
            self.bugReport(ctx, "Semantico", "Falta de apertura de parentesis")
        
    def visitTerminal(self, node: TerminalNode):
        print(" ---> Token: " + node.getText())

    def visitErrorNode(self, node: ErrorNode):
        print(" ---> ERROR")

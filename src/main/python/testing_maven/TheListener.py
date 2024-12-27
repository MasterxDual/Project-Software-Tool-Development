from antlr4 import ErrorNode, TerminalNode
from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser
from SymbolTable import SymbolTable
from Id import DataType
from Variable import Variable
from Context import Context
from Function import Function
from typing import Optional
class TheListener(compiladoresListener):
    """
    Clase que implementa el listener para el analizador sintáctico. 
    """

    variables_dict = {} #Diccionario para almacenar variables temporales
    symbol_table = SymbolTable()  #Instancia de la tabla de símbolos
    errors = [] #Lista para almacenar errores encontrados
    warnings = [] #Lista para almacenar advertencias encontradas
    actual_function: Optional[Function] = None # Para rastrear la funcion actual
    stack_arguments = [] # Lista para almacenar los argumentos que espera una funcion
    arguments_to_function = [] # Esta lista tendra que guardar los argumentos que se pasan a la funcion en la invocaion
    types_list = []

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

    def getContextName(self, ctx):
        """
        Obtiene el nombre del contexto actual.
        Este método determina el nombre del contexto basado en el tipo de estructura
        """
        father = ctx.parentCtx
        # Verifica si padre es una instancia de la clase especifica proporcionada
        if isinstance(father, compiladoresParser.FunctionContext): # Si el padre es una función
            return f"Función {father.getChild(1).getText()}"
        elif isinstance(father, compiladoresParser.InstructionContext): # Si el padre es una instrucción
            if isinstance(father.parentCtx, compiladoresParser.IwhileContext): # Si el padre es 'while'
                return "While"
            elif isinstance(father.parentCtx, compiladoresParser.IforContext): # Si el padre es 'for'
                return "For"
            elif isinstance(father.parentCtx, compiladoresParser.IifContext): # Si el padre es 'if'
                return "If"
            elif isinstance(father.parentCtx, compiladoresParser.IelseContext): # Si el padre es 'else'
                return "Else"
        else: 
            return None

    def searchWarningsContext(self, ctx):
        """
        Busca advertencias en el contexto actual.
        Este método busca advertencias en el contexto actual y las agrega a la lista de advertencias
        """
        # Obtenemos todos los contextos de la tabla de simbolos
        contexts = self.symbol_table.get_contexts()

        # Recorremos el contexto actual en busca de ID no inicializados y/o usados
        for variable in contexts[-1].get_identifiers().values(): 
            if variable.get_initialized() is False: # Si no esta incializado
                self.warningReport(ctx, f"Identificador '{variable.name}' no inicializada")
            if variable.get_used() is False: # Si no esta usado:
                self.warningReport(ctx, f"Identificador '{variable.name}' no usada")


    def enterProgram(self, ctx:compiladoresParser.ProgramContext):
        """
        Método que se ejecuta al entrar en el contexto de la regla "programa".
        Inicializa el contexto global y comienza el proceso de compilación.
        """

        print("\n+" + "="*10, "Comienza la Compilacion", "="*10 + "+\n")
        self.symbol_table.add_context("Global") # Agrega el contexto global (primer contexto) a la tabla de simbolos
        print(f"=== Entrando al Contexto Global ===")

    def exitProgram(self, ctx:compiladoresParser.ProgramContext):
        """
        Método que se ejecuta al salir del contexto de la regla "programa".
        Finaliza el proceso de compilación y muestra los reportes de errores y advertencias.
        """
        context_name = self.symbol_table.get_contexts()

        try: 
            print(f"\n=== Saliendo Contexto: {context_name[-1].name} ===") # Notifica que salimos de dicho contexto
        except IndexError:
            print(f"\n=== Saliendo Contexto: Global ===") # Si no hay contexto
        
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

    def exitInstruction(self, ctx:compiladoresParser.InstructionContext):
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
        context_name = self.getContextName(ctx)
        if context_name: 
            self.symbol_table.add_context(context_name) # Agrega un nuevo Contexto a la tabla de simbolos
            print(f"\n=== Entrando al Contexto: {context_name} ===")

        # Verifica si padre es una funcion
        if context_name not in {"While", "For", "If", "Else", None}:
            for arg in self.stack_arguments:
                self.symbol_table.add_identifier(arg)
                print(f"Se agrego el ID '{arg.name}' a la funcion '{context_name}'")

    def exitBlock(self, ctx: compiladoresParser.BlockContext):
        """
        Método que se ejecuta al salir del contexto de la regla "bloque".
        Verifica las variables no inicializadas y no usadas en el bloque.
        """
        # Reporte de errores
        if ctx.getChild(2).getText() != '}':
            linea = ctx.RBRACE().getSymbol().line
            self.errors.append(f"Error Sintactico en la linea {linea}: se esperaba una instrucción")
            return

        context_name = self.getContextName(ctx)
        self.searchWarningsContext(ctx) 
        print(f"\n=== Saliendo del Contexto: {context_name} ===")
        self.symbol_table.del_context() # Borra el contexto actual
    

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
            print(f"Nueva variable: '{id_name}' de tipo '{data_type}' agregada.\n") #Revisar para que no agregue el simbolo o solo reporte un error

            if str(ctx.getChild(2).getText()) != '': # Si el 3er hijo en la declaracion es distinto de vacio, existe una definicion
                if self.data_type_obtained: #Evaluar si los tipos de datos son compatibles en la asignacion
                    if data_type != self.data_type_obtained:
                        self.warningReport(ctx, "Sintactico: tipo de dato no compatible")
                        return
                    variable.set_initialized() #Marca la variable como inicializada si se proporciona un valor
                    self.data_type_obtained = None
                else:
                    #Si no fuese un ID
                    variable.set_initialized() #Marca la variable como inicializada si se proporciona un valor

            # Maneja la declaración de múltiples variables (si es necesario)
            if self.variables_dict:
                while self.variables_dict:
                    new_variable, is_initialized = self.variables_dict.popitem()

                    # Verifica si la variable ya ha sido declarada en el ámbito local
                    if self.symbol_table.local_search(new_variable) is None:
                        variable = Variable(new_variable, data_type)
                        self.symbol_table.add_identifier(variable)

                        # Para validar si realmente se estan agregando los ID's a la tabla de contextos en su contexto correspondiente
                        print(f"Nueva variable: '{self.symbol_table.local_search(variable.name).name}'" + f" de tipo '{data_type}' agregada.\n")
                        
                        if is_initialized:  #Marca la variable como inicializada si es True
                            variable.set_initialized()
                    else:
                        #Error si la variable ya fue declarada
                        self.bugReport(ctx, "Semantico", f"El identificador '{ctx.getChild(1).getText()}' ya esta definido en este bloque")
        else:
            # Imprime un mensaje de error si la variable ya fue declarada
            self.bugReport(ctx, "Semantico", f"El identificador '{ctx.getChild(1).getText()}' ya esta definido en este bloque")
        
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
        variable_name = ctx.getChild(0).getText()
        identifier = self.symbol_table.global_search(variable_name)
        if identifier is None: # Si el identificador no existe en la tabla de simbolos
            # Notifica el uso de un ID sin declarar
            self.bugReport(ctx, "Semantico", f"El identificador '{ctx.getChild(0).getText()}' no esta definido")
            return
        else: #Evaluar si los tipos de datos son compatibles en la asignacion
            data_type = identifier._data_type
            if self.data_type_obtained:
                if data_type != self.data_type_obtained:
                    self.warningReport(ctx, "Sintactico: tipo de dato no compatible")
                    return
                identifier.set_initialized() #Marca la variable como inicializada si se proporciona un valor
                self.data_type_obtained = None

        # Verifica si el valor asignado es correcto
        if ctx.getChild(2) == ctx.opal():
            identifier.set_initialized() # Se inicializa la variable

    """----------------------------------------------------------------"""
    data_type_obtained = None

    def exitWhilei(self, ctx:compiladoresParser.WhileiContext):
        """
        Maneja la salida de un contexto de while.
        """
        if ctx.getChild(1).getText() != '(':
            self.bugReport(ctx, "Sintactico", "Falta parentesis de apertura")
            return
        
        if ctx.getChild(3).getText() != ')':
            self.bugReport(ctx, "Sintactico", "Falta parentesis de cierre")
            return
        
        # Verifica si es una estructura de una sola linea donde se hace una declaracion:
        if isinstance(ctx.getChild(4).getChild(0), compiladoresParser.DeclarationContext):
            self.bugReport(ctx, "Sintactico", "Una instrucción dependiente no puede ser una declaración")
        

    def exitFori(self, ctx: compiladoresParser.ForiContext):
        """
        Maneja la salida de un contexto de for.
        """
        if ctx.getChild(1).getText() != '(':
            self.bugReport(ctx, "Sintactico", "Falta parentesis de apertura")
            return
        
        if ctx.getChild(7).getText() != ')':
            self.bugReport(ctx, "Sintactico", "Falta parentesis de cierre")

        # Verifica si es una estructura de una sola linea donde se hace una declaracion:
        if isinstance(ctx.getChild(8).getChild(0), compiladoresParser.DeclarationContext):
            self.bugReport(ctx, "Sintactico", "Una instrucción dependiente no puede ser una declaración")

    def exitIfi(self, ctx: compiladoresParser.IfiContext):
        """
        Maneja la salida de un contexto de if.
        """
        if ctx.getChild(1).getText() != '(':
            self.bugReport(ctx, "Sintactico", "Falta parentesis de apertura")
            return
        
        if ctx.getChild(3).getText() != ')':
            self.bugReport(ctx, "Sintactico", "Falta parentesis de cierre")

        # Verifica si es una estructura de una sola linea donde se hace una declaracion:
        if isinstance(ctx.getChild(4).getChild(0), compiladoresParser.DeclarationContext):
            self.bugReport(ctx, "Sintactico", "Una instrucción dependiente no puede ser una declaración")
        

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
                self.data_type_obtained = identifier._data_type
                self.symbol_table.update_used(identifier.name)
        else:
            self.data_type_obtained = None

        # Manejo de parentesis en operaciones logicas:
        if ctx.LPAR() and ctx.getChild(2).getText() != ')':
            self.bugReport(ctx, "Semantico", "Falta de cierre de parentesis")
            return
        
        if ctx.RPAR() and ctx.getChild(0).getText() != '(':
            self.bugReport(ctx, "Semantico", "Falta de apertura de parentesis")


    def exitElsei(self, ctx: compiladoresParser.ElseiContext):
        """
        Maneja la salida de un contexto de else.
        """
        # Verifica si es una estructura de una sola linea donde se hace una declaracion:
        if isinstance(ctx.getChild(2).getChild(0), compiladoresParser.DeclarationContext):
            self.bugReport(ctx, "Sintactico", "Una instrucción dependiente no puede ser una declaración")
            

    def exitFunction_prototype(self, ctx: compiladoresParser.Function_prototypeContext):
        """
        Maneja la salida de un contexto de prototipo de función.
        Es decir, mameja la declaracion de funciones.
        """
        return_type = ctx.getChild(0).getText().upper()
        function_name = ctx.getChild(1).getText()

        #Verificar si la función ya existe
        if self.symbol_table.global_search(function_name):
            self.bugReport(ctx, "Semantico", f"Funcion '{function_name}' ya fue declarada")
            # Vacia la pila de argumentos
            if self.stack_arguments:
                self.stack_arguments.clear()
            return

        #Crear nueva función
        _function = Function(function_name, return_type)
        self.actual_function = _function #Guardamos la funcion actual.

        #Procesamos los argumentos de la funcion, si existen
        if str(ctx.getChild(3).getText()) != '': #Si la funcion tiene argumentos
            for arg in self.stack_arguments:
                self.actual_function.add_arg(arg)

        #Si la funcion no existe Agregar función a la tabla de símbolos
        self.symbol_table.add_identifier(_function)
        print(f"Nueva funcion: '{self.symbol_table.local_search(function_name).name}' agregada.\n")

        # Vacia la pila de argumentos
        if self.stack_arguments:
            self.stack_arguments.clear()


    def exitArguments(self, ctx: compiladoresParser.ArgumentsContext):
        """
        Maneja la salida de un contexto de argumentos
        """
        if ctx.getChildCount():
            name = ctx.getChild(1).getText()
            data_type = ctx.getChild(0).getText()
            new_variable = Variable(name, data_type)
            new_variable.set_initialized()  # Los parámetros se consideran inicializados
            new_variable.set_used()
            self.stack_arguments.append(new_variable)    
    
    def exitArguments_list(self, ctx: compiladoresParser.Arguments_listContext):
        """
        Se ejecuta al final de la lista de argumentos de una función.
        """
        if ctx.getChildCount():
            name = ctx.getChild(2).getText()
            data_type = ctx.getChild(1).getText()
            new_variable = Variable(name, data_type)
            new_variable.set_initialized()  # Los parámetros se consideran inicializados
            new_variable.set_used()
            self.stack_arguments.append(new_variable)

    def exitFunction(self, ctx: compiladoresParser.FunctionContext):
        """
        Maneja la salida de un contexto de función.
        """
        name = ctx.getChild(1).getText()
        function = self.symbol_table.global_search(name)

        #Verificar si la funcion no existe
        if function is None: # Si la funcion no existe ==> no tiene prototipo
            #Crear nueva funcion
            return_type = ctx.getChild(0).getText().upper()
            function = Function(name, return_type)
            self.actual_function = function # Guardamos la funcion actual

            # Procesamos los argumentos de la funcion, si existen
            if str(ctx.getChild(3).getText()) != '': # Si la funcion tiene argumentos
                for arg in self.stack_arguments:
                    self.actual_function.add_arg(arg)

            # Si la funcion no existe Agregar función a la tabla de símbolos
            self.symbol_table.add_identifier(function)
            function.set_initialized() # Se inicializa porque su definicion esta escrita correctamente
            print(f"Nueva funcion: '{function.name}' agregada.\n")

            if name == 'main':
                function.set_used() #Marco la funcion principal main como usada

            #Vacia la pila de argumentos
            if self.stack_arguments:
                self.stack_arguments.clear()
        else:
            # Si la función ya existe, verificar si los argumentos coinciden
            if function.get_type() != ctx.getChild(0).getText().upper():
                self.bugReport(ctx, "Semantico", f"Tipo de retorno de la funcion no coincide con la declaracion")
                #Vacia la pila de argumentos
                if self.stack_arguments:
                    self.stack_arguments.clear()
                return
            
            try:
                # Verificar si los argumentos coinciden
                for ii, arg in enumerate(self.stack_arguments):
                    if function.args[ii].name != arg.name or function.args[ii]._data_type != arg.data_type:
                        self.bugReport(ctx, "Semantico", f"Argumento no coincide con su prototipo")
                        # Vacia la pila de argumentos
                        if self.stack_arguments:
                            self.stack_arguments.clear()
                        return
            except IndexError: # Si la cantidad de argumentos no coincide
                self.bugReport(ctx, "Semantico", f"Número incorrecto de argumentos para función '{function.name}'. "f"Esperados: {len(function.args)}, Recibidos: {len(self.stack_arguments)}")

            # Si todo salio bien, y el prototipo tiene su definicion de funcion entonces la inicializo
            function.set_initialized() # Se inicializa porque su definicion esta escrita correctamente

            #Vacia la pila de argumentos
            if self.stack_arguments:
                self.stack_arguments.clear()
        
    def exitFunction_call(self, ctx: compiladoresParser.Function_callContext):
        """
        Maneja las llamadas a funciones.
        """
        if ctx.getChild(1).getText() != '(':
            self.bugReport(ctx, "Sintactico", "Falta parentesis de apertura")
            self.arguments_to_function.clear()
            return
        if ctx.getChild(3).getText() != ')':
            self.bugReport(ctx, "Sintactico", "Falta parentesis de cierre")
            self.arguments_to_function.clear()
            return
        
        function_name = ctx.getChild(0).getText()
        _function = self.symbol_table.global_search(function_name)

        if _function: # Si la funcion existe en la tabla de simbolos comprueba que se reciban la misma cantidad de parametros esperados
            if len(_function.args) != len(self.arguments_to_function):
                self.reporteErrores(ctx, "Semantico", f"Número incorrecto de argumentos para función '{_function.name}'. "f"Esperados: {len(_function.args)}, Recibidos: {len(self.stack_arguments)}")
                self.arguments_to_function.clear()
                return
            
            _function.set_used() # Si la funcion existe, se marca como usada por la invocacion
            print(f"Se invoco la Funcion: {_function.name} correctamente")
        else:  # Si la funcion no existe reporta el error
            self.bugReport(ctx, "Semantico", f"Funcion '{function_name}' no fue declarada")
            self.arguments_to_function.clear()
            

    """ def exitReturning(self, ctx: compiladoresParser.ReturningContext):
        if ctx.getChild(1).getText() == ctx.

            id_name = ctx.getChild(0).getText()
            ctx_actual = ctx.parentCtx
            if isinstance(ctx_actual, compiladoresParser.ReturningContext):
                id_found = self.symbol_table.local_search(id_name)
                if id_found is not None:
                    self.types_list.append(id_found.data_type.name)
     """            

    def exitArguments_to_function_list(self, ctx: compiladoresParser.Arguments_to_function_listContext):
        """
        Se ejecuta al final de la lista de argumentos de una llamada a función.
        """
        if ctx.getChildCount():
            self.arguments_to_function.append(ctx.getChild(1).getText())

    def exitArguments_to_function(self, ctx:compiladoresParser.Arguments_to_functionContext):
        """
        Se ejecuta al final de la lista de argumentos de una llamada a función.
        """
        if ctx.getChildCount():
            self.arguments_to_function.append(ctx.getChild(0).getText())
from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser

class Temporal():
    def __init__(self):
        self.counter = -1

    def get_temporal(self):
        self.counter += 1
        return f't{self.counter}'
    
class Label():
    def __init__(self):
        self.counter = -1

    def get_label(self):
        self.counter += 1
        return f'l{self.counter}'

class Walker(compiladoresVisitor):
    def __init__(self):  
        self.file                    = None
        self.route                    = './output/codigoIntermedio.txt' 
        self.temporary              = []
        self.labels               = []
        self.temporaryGenerator   = Temporal()
        self.LabelsGenerator    = Label()

        self.operating1               = None
        self.operating2               = None
        self.operator               = None
        self.isAdder               = False

        # Constantes Codigo Intermedio de Tres Direcciones
        self.label   = 'label'
        self.b          = 'jmp'
        self.bneq       = 'ifnjmp'
    
    def visitProgram(self, ctx: compiladoresParser.ProgramContext):
        print("-" + "=" * 30 + "-")
        print("-- Comienza a generar Codigo Intermedio --")
        self.file = open(self.route, "w")

        self.visitInstructions(ctx.getChild(0))

        self.file.close()
        print("-- Codigo Intermedio generado Correctamente --")
        print("-" + "=" * 30 + "-")

    # # Visit a parse tree produced by compiladoresParser#instrucciones.
    # def visitInstructiones(self, ctx:compiladoresParser.InstruccionesContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#instruccion.
    # def visitInstruccion(self, ctx:compiladoresParser.InstruccionContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#bloque.
    # def visitBloque(self, ctx:compiladoresParser.BloqueContext):
    #     return self.visitChildren(ctx)

    # Visit a parse tree produced by compiladoresParser#declaration.
    def visitDeclaration(self, ctx:compiladoresParser.DeclarationContext):
        # Guardo el valor del identificador de la declaracion
        _id = ctx.getChild(1).getText()

        # Si existe el hijo 2 (Definicion), entonces hay una asignacion a la variable
        if ctx.getChild(2).getChildCount() != 0:
            self.visitDefinition(ctx.getChild(2))

            # Si hay un temporal, es el ultimo paso de la asignacion, es decir, hubo operaciones dentro de la asignacion
            if self.temporales:
                self.file.write(f"{_id} = {self.temporary.pop()}\n\n")
                
            # De la contrario la variable solo almacena un factor
            else:
                self.file.write(f"{_id} = {self.operating1}\n\n")

            # Reseteo los elementos para las operaciones
            self.operating1 = None
            self.operating2 = None
            self.operator  = None

        # De lo contrario solo se declaro la varible vacia
        else:
            self.file.write(f'Declaracion de la variable {_id}\n')
        
        if ctx.getChild(3).getChildCount() != 0:
            self.visitVarlist(ctx.getChild(3))


    # Visit a parse tree produced by compiladoresParser#definition.
    def visitDefinition(self, ctx:compiladoresParser.DefinitionContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        self.visitOpal(ctx.getChild(1))

    # Visit a parse tree produced by compiladoresParser#varList.
    def visitVarlist(self, ctx:compiladoresParser.VarlistContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        # Guardo el valor del identificador de la declaracion
        _id = ctx.getChild(1).getText()

        # Si existe el hijo 3 (Definicion), entonces hay una asignacion a la variable
        if ctx.getChild(2).getChildCount() != 0:
            self.visitDefinition(ctx.getChild(2))

            # Si hay un temporal, es el ultimo paso de la asignacion, es decir, hubo operaciones dentro de la asignacion
            if self.temporary:
                self.file.write(f"{id} = {self.temporary.pop()}\n\n")
                
            # De la contrario la variable solo almacena un factor
            else:
                self.file.write(f"{id} = {self.operating1}\n\n")

            # Reseteo los los elementos para las operaciones
            self.operating1 = None
            self.operating2 = None
            self.operator  = None

        # De lo contrario solo se declaro la varible vacia
        else:
            self.file.write(f'Declaracion de la variable {_id}\n')

        if ctx.getChild(3).getChildCount() != 0:
            self.visitVarlist(ctx.getChild(3))

    # Visit a parse tree produced by compiladoresParser#assignment.
    def visitAssignment(self, ctx:compiladoresParser.AssignmentContext):
        # Guardo el valor del identificador de la declaracion
        _id = ctx.getChild(0).getText()

        self.visitOpal(ctx.getChild(2))

        # Si hay un temporal, es el ultimo paso de la asignacion, es decir, hubo operaciones dentro de la asignacion
        if self.temporary:
            self.file.write(f"{_id} = {self.temporary.pop()}\n\n")
        
        # De lo contrario la variable solo almacena un factor
        else:
            self.file.write(f"{_id} = {self.operating1}\n\n")

        # Reseteo los los elementos para las operaciones
        self.operating1 = None
        self.operating2 = None
        self.operator  = None

    # Visit a parse tree produced by compiladoresParser#opal.
    def visitOpal(self, ctx:compiladoresParser.OpalContext):
        self.visitOplogic(ctx.getChild(0))
        
     # Visit a parse tree produced by compiladoresParser#oplogic.
    def visitOplogic(self, ctx:compiladoresParser.OplogicContext):
        self.visitLogic(ctx.getChild(0))

        if ctx.getChild(1).getChildCount() != 0:
            # Si el operando1 es un temporal, es el ultimo paso de la asignacion
            if self.temporary:
                self.operating1 = self.temporary.pop()
            # En caso contrario, operando1 es el primer factor, el valor queda como esta
            
            self.visitLor(ctx.getChild(1))

    # Visit a parse tree produced by compiladoresParser#lor.
    def visitLor(self, ctx:compiladoresParser.LorContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        # Creo una copia del actual operando1
        operating1 = self.operating1

        # Visito el segundo conjunto de la operacion AND
        self.visitLogic(ctx.getChild(1))

        # Si el operando 2 es un temporal, es el ultimo paso de la asignacion
        if self.temporary:
            self.operating2 = self.temporary.pop()
        # En caso contrario, operando2 es un facotr simple guardado en operando1
        else:
            self.operating2 = self.operating1

        # Recupero el valor del operando1 de la operacion OR actual
        self.operating1 = operating1

        # Guardo el operador OR
        self.operator = ctx.getChild(0).getText()

         # Genero un temporal para la operacion OR
        self.temporary.append(self.temporaryGenerator.get_temporal())

        # Escribo en el archivo la operacion OR
        self.file.write(f'{self.temporary[-1]} = {self.operating1} {self.operator} {self.operating2}\n')

        # Si el hijo 2 (Lor) no es vacio, entonces hay otra operacion OR
        if ctx.getChild(2).getChildCount() != 0:
            # El operando1 para la siguiente operacion OR es el temporal generado en esta
            self.operating1 = self.temporary.pop()

            # Visita la regla Lor para escribir la siguiente operacion
            self.visitLor(ctx.getChild(2))

    # Visit a parse tree produced by compiladoresParser#logic.
    def visitLogic(self, ctx:compiladoresParser.LogicContext):
        self.visitSet(ctx.getChild(0))

        if ctx.getChild(1).getChildCount() != 0:
            # Si el operando 1 es un temporal, es el ultimo paso de la asignacion
            if self.temporary:
                self.operating1 = self.temporary.pop()
            # En caso contrario, operando1 es el primer factor, el valor queda como esta

            self.visitLand(ctx.getChild(1))

    # Visit a parse tree produced by compiladoresParser#land.elf.operating1
    def visitLand(self, ctx:compiladoresParser.LandContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        # Creo una copia del actual operando1
        operating1 = self.operating1

        # Visito el segundo conjunto de la operacion AND
        self.visitSet(ctx.getChild(1))

        # Si el operando 2 es un temporal, es el ultimo paso de la asignacion
        if self.temporary:
            self.operating2 = self.temporary.pop()
        # En caso contrario, operando2 es un facotr simple guardado en operando1
        else:
            self.operating2 = self.operating1

        # Recupero el valor del operando1 de la operacion AND actual
        self.operating1 = operating1

        # Guardo el operador AND
        self.operator = ctx.getChild(0).getText()

        # Genero un temporal para la operacion AND
        self.temporary.append(self.temporaryGenerator.get_temporal())

        # Escribo en el archivo la operacion AND
        self.file.write(f'{self.temporary[-1]} = {self.operating1} {self.operator} {self.operating2}\n')

        # Si el hijo 2 (Land) no es vacio, entonces hay otra operacion AND
        if ctx.getChild(2).getChildCount() != 0:
            # El operando1 para la siguiente operacion AND es el temporal generado en esta
            self.operating1 = self.temporary.pop()

            # Visita la regla Land para escribir la siguiente operacion
            self.visitLand(ctx.getChild(2))

    # Visit a parse tree produced by compiladoresParser#set.
    def visitSet(self, ctx:compiladoresParser.SetContext):
        # Si el hijo 1 (Igualdad) no es vacio, entonces hay una comparacion de igualdad
        if ctx.getChild(1).getChildCount() != 0:
            # Si el hijo 0 (C) tiene un hijo 1 (Comparar) vacio, entonces no hay operacion de comparacion
            cond1 = ctx.getChild(0).getChild(1).getChildCount() == 0

            # Si el hijo 0 (C) tiene un hijo 0 (Exp) tiene un hijo 1 (E) vacio, entonces no hay operacion de suma/resta
            cond2 = ctx.getChild(0).getChild(0).getChild(1).getChildCount() == 0

            # Si el hijo 0 (C) tiene un hijo 0 (Exp) tiene un hijo 0 (Term) que tiene un hijo 1 (T) vacio, entonces es un termino simple
            cond3 = ctx.getChild(0).getChild(0).getChild(0).getChild(1).getChildCount() == 0

            # Entonces si se cumplen las condiciones, operando1 es un termino simple
            if cond1 and cond2 and cond3:
                self.visitC(ctx.getChild(0))

            # De lo contrario
            else:
                self.visitC(ctx.getChild(0))

                self.operating1 = self.temporary.pop(0)

            # Visito Igualdad  en busca de comparaciones de igualdad
            self.visitEquality(ctx.getChild(1))                
        
        # De lo contrario no hay comparaciones de igualdad, asi que solo visita al subconjunto en busca de operaciones de comparacion
        else:                
            self.visitC(ctx.getChild(0))


    # Visit a parse tree produced by compiladoresParser#equality.
    def visitEquality(self, ctx:compiladoresParser.EqualityContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        # Guarda el valor actual del operando1
        operating1 = self.operating1

        # Si el hijo 1 (C) tiene un hijo 1 (Comparar) vacio, entonces no hay operacion de comparacion
        cond1 = ctx.getChild(1).getChild(1).getChildCount() == 0

        # Si el hijo 1 (C) tiene un hijo 0 (Exp) tiene un hijo 1 (E) vacio, entonces no hay operacion de suma/resta
        cond2 = ctx.getChild(1).getChild(0).getChild(1).getChildCount() == 0

        # Si el hijo 1 (C) tiene un hijo 0 (Exp) tiene un hijo 0 (Term) que tiene un hijo 1 (T) vacio, entonces es un termino simple
        cond3 = ctx.getChild(1).getChild(0).getChild(0).getChild(1).getChildCount() == 0

        # Entonces si se cumplen estas condiciones
        if cond1 and cond2 and cond3:
            self.visitC(ctx.getChild(1))
            self.operating2 = self.operating1

        # De lo contrario
        else:
            self.visitC(ctx.getChild(1))

            self.operating2 = self.temporary.pop(0) 

        # Guardo el valor del operador de comparacion de igualdad
        self.operator = ctx.getChild(0).getText()

        # Reasigno el valor original del operando1
        self.operating1 = operating1

        # Genera un temporal para la operacion
        self.temporary.append(self.temporaryGenerator.get_temporal())

        # Escribe en el archivo de salida la suma/resta de los terminos igualados a un temporal generado
        self.file.write(f'{self.temporary[-1]} = {self.operating1} {self.operator} {self.operating2}\n')

        # Si el hijo 2 (igualdad) no es vacio, hay mas operaciones de comparacion de igualdad
        if ctx.getChild(2).getChildCount() != 0:
            # Genero un temporal para guardar el resultado de la sigueinte operacion
            temporal = self.temporaryGenerator.get_temporal()

            # Operando1 para la siguiente operacion sera el temporal generado en la operacion actual
            self.operating1 = self.temporary.pop()

            # Agrego el temporal generado a la lista de temporales
            self.temporary.append(temporal)

            # Visita Igualdad para obtener el resultado de la siguiente operacion de suma/resta
            self.visitEquality(ctx.getChild(2))


    # Visit a parse tree produced by compiladoresParser#c.
    def visitC(self, ctx:compiladoresParser.CContext):

        """ ------------------------------------------ Function --------------------------------------------------- """
        def visit_expression (ctx):
            """ 
                Visita la regla gramatical Exp, y evalua si la bandera para el segundo recorrido esta activa para 
                sumar/restar los terminos obtenidos en la primera pasada
            """
            
            # Visita Exp
            self.visitExp(ctx.getChild(0))

            # Si la bandera es True recorro el arbol para sumar los terminos
            if self.isAdder:
                self.visitExp(ctx.getChild(0)) # Los terminos se encuentran dentro de Exp (expresion)
                # super().visitExp(ctx) # Los terminos se encuentran dentro de Exp (expresion)
                self.isAdder = False # Reseteo la bandera
            """ -------------------------------------- Fin de la Funcion --------------------------------------------- """
            
        # Si el hijo 1 (Comparar) no es vacio, entonces hay una operacion de comparacion
        if ctx.getChild(1).getChildCount() != 0:
            # Si el hijo 0 (Exp) tiene un hijo 1 (E) vacio, entonces no hay operacion de suma/resta
            cond1 = ctx.getChild(0).getChild(1).getChildCount() == 0

            # Si el hijo 0 (Exp) tiene un hijo 0 (Term) tiene un hijo 1 (T) vacio, entonces es un termino simople
            cond2 = ctx.getChild(0).getChild(0).getChild(1).getChildCount() == 0

            # Entonces si ambas se cumplen:
            if cond1 and cond2:
                visit_expression(ctx)
            
            # De lo contrario
            else:
                visit_expression(ctx)
                self.operating1 = self.temporary.pop(0)
            
            # Visito Comparar en busca de operaciones de comparacion
            self.visitComparity(ctx.getChild(1))

        # De lo contrario no hay mas comparaciones
        else:
            visit_expression(ctx)

    # Visit a parse tree produced by compiladoresParser#comparar.
    def visitComparity(self, ctx:compiladoresParser.ComparityContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount == 0:
            return
        
        """ ------------------------------------------ Function --------------------------------------------------- """
        def visit_expression (ctx):
            """ 
                Visita la regla gramatical Exp, y evalua si la bandera para el segundo recorrido esta activa para 
                sumar/restar los terminos obtenidos en la primera pasada
            """

            # Visita Exp
            self.visitExp(ctx.getChild(1))

            # Si la bandera es True recorro el arbol para sumar los terminos
            if self.isAdder:
                self.visitExp(ctx.getChild(1)) # Los terminos se encuentran dentro de Exp (expresion)
                # super().visitExp(ctx) # Los terminos se encuentran dentro de Exp (expresion)
                self.isAdder = False # Reseteo la bandera
        """ -------------------------------------- Fin de la Funcion --------------------------------------------- """

        # Guardo el valor del operando1
        operating1 = self.operating1

        # Si el hijo 1 (Exp) tiene un hijo 1 (E) vacio, entonces no hay operacion de suma/resta
        cond1 = ctx.getChild(1).getChild(1).getChildCount() == 0

        # Si el hijo 1 (Exp) tiene un hijo 0 (Term) tiene un hijo 1 (T) vacio, entonces es un termino simople
        cond2 = ctx.getChild(1).getChild(0).getChild(1).getChildCount() == 0

        # Entonces si ambas se cumplen:
        if cond1 and cond2:
            visit_expression(ctx)
            
            # Como Exp es llamada dentro de Comparar, el operando1 obtenido es el operando2
            self.operating2 = self.operating1

        # De lo contrario, hay una operacion de suma/resta guardada
        else:
            visit_expression(ctx)
            self.operating2 = self.temporary.pop(0)

        # Restauro el valor original del operando1
        self.operating1 = operating1

        # Guardo el operador de comparacion
        self.operator = ctx.getChild(0).getText()

        # Genera el temporal para trabajar con la operacion actual
        self.temporary.append(self.temporaryGenerator.get_temporal())

        # Escribo en el archivo la operacion de comparacion igualada a un temporal
        self.file.write(f'{self.temporary[-1]} = {self.operating1} {self.operator} {self.operating2}\n')

        # Si el hijo 2 (Comparar) no es vacio, hay una operacion de comparacion
        if ctx.getChild(2).getChildCount() != 0:

            # El ultimo temporal de la lista, sera el primer operando para la siguiente operacion
            self.operating1 = self.temporary.pop()

            # Visito el hijo 2 (Comparar)
            self.visitComparity(ctx.getChild(2))

    # Visit a parse tree produced by compiladoresParser#exp.
    def visitExp(self, ctx:compiladoresParser.ExpContext):

        # Si el hijo 1 (E) no es vacio, entonces hay una operacion de suma/resta
        if ctx.getChild(1).getChildCount() != 0:
            # Si la bandera es True, estoy en la segunda pasada encargada de sumar los terminos (temporales y factores)
            if self.isAdder:
                # Si el hijo 0 (Term) tiene un hijo 1 (T) que esta vacio, entonces el termino es un factor y no una operacion de multiplicacion/division
                if ctx.getChild(0).getChild(1).getChildCount() == 0:
                    # Visita Term para obtener operando1 que es un termino simple (factor, es decir, un numero o un id)
                    self.visitTerm(ctx.getChild(0)) 

                # De lo contrario el hijo 0 (Term) es un termino compuesto el cual se guardo en la lista de temporales
                else:
                    self.operating1 = self.temporary.pop(0)

                # Visita el hijo 1 (E) para obtener operando2 y el operador de suma/resta
                self.visitE(ctx.getChild(1))
            # Si la bandera es False, estoy en la primera pasada en busca operaciones de multiplicacion/division
            else:
                # Si es un termino compuesto (x * y) visito Term para generar los temporales correspondientes
                if ctx.getChild(0).getChild(1).getChildCount() != 0:
                    # Visito Primero Term en busca de operaciones de multiplicacion/division
                    self.visitTerm(ctx.getChild(0))

                # Visito E en busca de operaciones de multiplicacion/division
                self.visitE(ctx.getChild(1))

                # Como primero busco operaciones de multiplicacion/division y existen sumas/restas debo sumar los terminos
                self.isAdder = True
                # Al activar esta bandera se realizara la segunda pasada para sumar los terminos invocada por la regla gramatical C

        # De lo contrario no hay mas sumas/restas y visita el unico termino de la operacion
        else:                
            self.visitTerm(ctx.getChild(0))

    # Visit a parse tree produced by compiladoresParser#e.
    def visitE(self, ctx:compiladoresParser.EContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        # Si la bandera esta activa, entonces estoy en la segunda pasada encargada de sumar/restar los terminos
        if self.isAdder:
            # Guarda el valor actual del operando1 que bien puede ser un termino simple o un temporal
            operating1 = self.operating1

            # Si el hijo 1 (Term) tiene un hijo 1 (T) que esta vacio, entonces el term es un termino simple
            if ctx.getChild(1).getChild(1).getChildCount() == 0:
                # Visita Term para obtener el valor del operando1 (termino simple de un factor)
                self.visitTerm(ctx.getChild(1))

                # Dentro del hijo (E) trabaja el lado derecho de la suma/resta, por lo tanto el operando1 es en realidad el operando2 de toda la operacion que invoca a (E)
                self.operating2 = self.operating1

            # De lo contrario el hijo 1 (Term) tiene un hijo 1 (T) que no esta vacio, entonces es un termino compuesto (temporal)
            else:
                # Como estoy en E, el operando2 es el valor del temporal que se creo en la primera pasada (resultados de las multiplicaciones/divisiones)
                self.operating2 = self.temporary.pop(0)

            # Guarda el operador de suma/resta de la operacion actual
            self.operator  = ctx.getChild(0).getText()

            # Reasigno el valor original del operando1
            self.operating1 = operating1

            # Genera el temporal para trabajar con la operacion actual
            self.temporary.append(self.temporaryGenerator.get_temporal())

            # Escribe en el archivo de salida la suma/resta de los terminos igualados a un temporal generado
            self.file.write(f'{self.temporary[-1]} = {self.operating1} {self.operator} {self.operating2}\n')

            # Si el hijo 2 (E) no es vacio, hay mas operaciones de suma/resta
            if ctx.getChild(2).getChildCount() != 0:

                # Operando1 para la siguiente operacion sera el temporal generado en la operacion actual
                self.operating1 = self.temporary.pop()

                # Visita E para obtener el resultado de la siguiente operacion de suma/resta
                self.visitE(ctx.getChild(2))

        # De lo contrario, estoy en la primera pasada en busca de operaciones de multiplicacion/division
        else:
            # Si el hijo 2 (E) no es vacio, entonces hay una operacion de suma/resta. Esto significa que tengo 2 o mas sumas/restas
            if ctx.getChild(2).getChildCount() != 0:

                # Si es un termino compuesto (x * y), lo visito para generar el temporal de la operacion
                if ctx.getChild(1).getChild(1).getChildCount() != 0:
                    self.visitTerm(ctx.getChild(1))

                # Visita E en busca de la siguiente operacion de suma/resta
                self.visitE(ctx.getChild(2))

            # De lo contrario no hay mas operaciones de suma/resta
            else:
                # Si es un termino compuesto (x * y) lo visito en busca de operaciones de creacion de temporales
                if ctx.getChild(1).getChild(1).getChildCount() != 0:
                    self.visitTerm(ctx.getChild(1))

    # Visit a parse tree produced by compiladoresParser#term.
    def visitTerm(self, ctx:compiladoresParser.TermContext): 
        # Guardo el primer operando de la operacion de multiplicacion/division
        self.operating1 = self.visitFactor(ctx.getChild(0))

        # Si el hijo 1 no es vacio, entonces hay una operacion de multiplicacion/division
        if ctx.getChild(1).getChildCount() != 0:
            # Visita la regla gramatical T
            self.visitT(ctx.getChild(1))

    # Visit a parse tree produced by compiladoresParser#t.
    def visitT(self, ctx:compiladoresParser.TContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        # Guardo el segundo operando de la operacion de multiplicacion/division
        self.operating2 = self.visitFactor(ctx.getChild(1))

        # Guardo el operador de la operacion de multiplicacion/division
        self.operator   = ctx.getChild(0).getText()

        # Genero un temporal para la operacion actual
        self.temporary.append(self.temporaryGenerator.get_temporal())

        # Escribo en el archivo la operacion de multiplicacion/division igualada a un temporal
        self.file.write(f'{self.temporary[-1]} = {self.operating1} {self.operator} {self.operating2}\n')

        # Si el hijo 2 (T) no es vacio, hay una operacion de multiplicacion/division
        if ctx.getChild(2).getChildCount() != 0:
            # El ultimo temporal de la lista, sera el primer operando para la siguiente operacion
            self.operating1 = self.temporary.pop()

            # Visito el hijo 2 (T)
            self.visitT(ctx.getChild(2))

    # Visit a parse tree produced by compiladoresParser#factor.
    def visitFactor(self, ctx:compiladoresParser.FactorContext):
        # Si Factor tiene 1 hijo, entonces es un factor simple (un numero o un id)
        if ctx.getChildCount() == 1:
            # operando sera un factor simple, es decir o un id o un numero
            operating = ctx.getChild(0).getText()

            # retorno el operando esperado en la operacion de multiplicacion/division invocante
            return operating
        
        # Si Factor tiene 2 hijos, entonces es un factor negado
        elif ctx.getChildCount() == 2:

            # Obtengo el valor del factor negado
            value = self.visitFactor(ctx.getChild(1))

            # Guardo el operador de negacion
            denial_operator = ctx.getChild(0).getText()

            # Genero un temporal para la operacion de negacion
            self.temporary.append(self.temporaryGenerator.get_temporal())

            # Escribo en el archivo la operacion
            self.file.write(f'{self.temporary[-1]} = {denial_operator}{value}\n')

            # Devuelvo el temporal creado
            return self.temporary.pop()
        
        # Si Factor tiene 3 hijos, entonces es una operacion entre parentesis
        elif ctx.getChildCount() == 3:
            # Guardo el valor actual del operando1 ya que sera sobreescrita en la sig. invocacion
            operating1 = self.operating1

            if self.isAdder:
                self.isAdder = False

                # Visito la regla gramatical Oplogicos
                self.visitOplogic(ctx.getChild(1))

                self.isAdder = True
            else:
                # Visito la regla gramatical Oplogicos
                self.visitOplogic(ctx.getChild(1))

            # Recupero el valor del operando1
            self.operating1 = operating1

            # Retorno el ultimo temporal de la lista
            return self.temporary.pop()

    # Visit a parse tree produced by compiladoresParser#iwhile.
    def visitWhilei(self, ctx:compiladoresParser.WhileiContext):
        # Genero la etiqueta para el salto condicional del bucle While
        self.labels.append(self.LabelsGenerator.get_label())

        # Escribo en el archivo la etiqueta para iniciar el bucle while
        self.file.write(f'{self.label} {self.labels[-1]}\n')

        # Visito la Regla Cond, en busca de la condicion del bucle While
        self.visitCondition(ctx.getChild(2))

        # Genero la etiqueta para finalizar el bucle while
        self.labels.append(self.LabelsGenerator.get_label())

        # Escribo en el archivo el salto condicional del bucle While
        self.file.write(f'{self.bneq} {self.temporary.pop()}, {self.labels[-1]}\n')

        # Visito la Regla Instruccion, para escribir en el archivo la instruccion del bucle While
        self.visitInstruction(ctx.getChild(4))
        
        # Escribo en el archivo el salto al final del bucle While
        self.file.write(f'{self.b} {self.labels.pop(0)}\n')

        # Escribo en el archivo la etiqueta para salir del bucle while
        self.file.write(f'{self.label} {self.labels.pop(0)}\n')

    # Visit a parse tree produced by compiladoresParser#ifor.
    def visitFori(self, ctx:compiladoresParser.ForiContext):
        # Caso para bucle for infinito
        if ctx.getChild(2).getChildCount() == 0 and ctx.getChild(4).getChildCount() == 0 and ctx.getChild(6).getChildCount() == 0:
            # Genero la etiqueta para el salto condicional del bucle for
            self.labels.append(self.LabelsGenerator.get_label())

            # Escribo en el archivo la etiqueta para iniciar el bucle for
            self.file.write(f'{self.label} {self.labels[-1]}\n')

            # Visito la Regla Instruccion, para escribir en el archivo la instruccion del bucle While
            self.visitInstruction(ctx.getChild(8))

            # Escribo en el archivo el salto al comienzo del bucle for
            self.file.write(f'{self.b} {self.labels.pop(0)}\n')

        # Caso para bucle for con condicion
        else:
            # Visita la Regla Init para obtener la asignacion inicial del bucle for
            self.visitInit(ctx.getChild(2))

            # Genero la etiqueta para el salto condicional del bucle for
            self.labels.append(self.LabelsGenerator.get_label())

            # Escribo en el archivo la etiqueta para iniciar el bucle for
            self.file.write(f'{self.label} {self.labels[-1]}\n')

            # Visito la Regla Cond, en busca de la condicion del bucle for
            self.visitCondition_for(ctx.getChild(4))

            # Genero la etiqueta para finalizar el bucle for
            self.labels.append(self.LabelsGenerator.get_label())

            # Escribo en el archivo el salto condicional del bucle for
            self.file.write(f'{self.bneq} {self.temporary.pop()}, {self.labels[-1]}\n')

            # Visito la Regla Instruccion, para escribir en el archivo la instruccion del bucle While
            self.visitInstruction(ctx.getChild(8))

            # Visita la Regla Iter, para obtener la accion post-ejecucion del bucle for (iterador)
            self.visitIter(ctx.getChild(6))

            # Escribo en el archivo el salto al comienzo del bucle for
            self.file.write(f'{self.b} {self.labels.pop(0)}\n')

            # Escribo en el archivo la etiqueta para salir del bucle while
            self.file.write(f'{self.label} {self.labels.pop(0)}\n')

    # Visit a parse tree produced by compiladoresParser#iter.
    def visitIter(self, ctx:compiladoresParser.IterContext):
        # Si el iter tiene 1 hijo, es una asignacion
        if ctx.getChildCount() == 1:
            self.visitAssignment(ctx.getChild(0))

        # Si Iter tiene 2 hijos, es un iterador
        elif ctx.getChildCount() == 2:
            # Genero un temporal para la operacion del iterador
            self.temporary.append(self.temporaryGenerator.get_temporal())

            # Casos para pre-incrementos/decrementos
            if ctx.getChild(0).getText() == '++' or ctx.getChild(0).getText() == '--':
                # Guardo la variable
                _id = ctx.getChild(1).getText()

                # Guardo el operador de ibcremento/decremento
                inc_dec = ctx.getChild(0).getText()

            # Casos para post-incrementos/decrementos
            else:
                # Guardo la variable
                _id = ctx.getChild(0).getText()

                # Guardo el operador de incremento/decremento
                inc_dec = ctx.getChild(1).getText()

            # Evaluo si se trata de un incremento o de un decremento
            if inc_dec == '++':
                self.operator = '+'
            else:
                self.operator = '-'

            # Escribo en el archivo la operacion de incremento/decremento dentro de un temporal
            self.file.write(f'{self.temporary[-1]} = {id} {self.operator} 1\n')

            # Escribo en el archivo, la asignacion del temporal a la variable
            self.file.write(f'{id} =  {self.temporary.pop()}\n')




        


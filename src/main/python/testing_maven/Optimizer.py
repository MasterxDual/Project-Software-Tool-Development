import re

class Optimizer:
    """ 
        Clase que implementa la optimización de código intermedio de tres direcciones.
        Realiza dos tipos principales de optimizaciones:
        1. Eliminación de subexpresiones comunes (reemplazo de acciones repetidas)
        2. Propagación de constantes
    """

    def __init__(self):
        """ 
            Inicializa el optimizador abriendo los archivos de entrada y salida
            y creando las estructuras de datos necesarias para el seguimiento de variables
        """ 
        self.origin    = open("output/codigoIntermedio.txt", "r")              # Archivo de codigo intermedio
        self.destiny   = open("output/codigoIntermedioOptimizado.txt", "w+")   # Archivo de codigo optimizado
        self.variables = dict()    # Almacena el valor actual de las variables reales
        self.temporary = dict()    # Almacena el valor de las variables temporales
        self.actions = dict()    # Mapea expresiones a sus variables temporales
        self.temp_expressions = dict()    # Almacena las expresiones originales de los temporales
    
    def is_temporal(self, variable):
        """
            Determina si una variable es temporal (t seguido de un número)

            Args:
                variable (str): Nombre de la variable a verificar

            Returns:
                bool: True si es una variable temporal, False en caso contrario
        """
        # Verifica si la variable comienza con 't' y sigue un número
        return bool(re.match(r'^t\d+$', variable))
    
    def is_control_line(self, line):
        """
            Determina si una línea es una instrucción de control de flujo

            Args:
                linea (str): Línea a verificar

            Returns:
                bool: True si es una instrucción de control, False en caso contrario
        """
        return (line.startswith('label') or 
        line.startswith('jmp') or 
        line.startswith('ifnjmp') or 
        line.startswith('ifjmp') or
        line.startswith('pop') or
        line.startswith('push'))

    def evaluate_expression(self, expression):
        """
            Evalúa una expresión reemplazando variables con sus valores actuales

            Args:
                expresion (str): Expresión a evaluar

            Returns:
                str: Resultado de la evaluación o None si no se puede evaluar
        """
        # Intenta evaluar la expresion
        try:
            # Primero reemplazar temporales
            for temp, value in self.temporary.items():
                # Si existe un temporal en la expresion, lo reemplaza con su valor
                expression = re.sub(r'\b{}\b'.format(re.escape(temp)), str(value), expression)
            # Luego reemplazar variables normales
            for var, valor in self.variables.items():
                # Si existe una variableen la expresion, lo reemplaza con su valor constante
                expression = re.sub(r'\b{}\b'.format(re.escape(var)), str(valor), expression)

            # Devuelve la expresion evaluada, es decir, la resuelve matematicamente
            return eval(expression)
        except Exception as e:
            print("Error al evaluar la expresion: ", str(e))
            # Si no se puede evaluar, devuelve None
            return None

    def get_temporal_expression(self, temp):
        """
            Obtiene la expresión original de una variable temporal
            y la simplifica si es posible

            Args:
                temp (str): Variable temporal
            Returns:
                str: Expresión simplificada o la original si no se puede simplificar
        """
        # Si el temporal esta dentro de mi lista de expresiones con temporales
        if temp in self.temp_expressions:
            # Obtener la expresión original
            expression = self.temp_expressions[temp]

            # Intentar evaluar la expresión 
            result = self.evaluate_expression(expression)

            # Si el resultado no es None, retorno la expresion resuelta
            if result is not None:
                return str(result)
            # Si no se puede evaluar, retorno la expresion original
            return expression
        
        # Si no esta en la lista, retorno el temporal
        return temp

    def optimize_intermediate_code(self):
        """
        Método principal que coordina el proceso de optimización
        """
        print("Optimizando codigo intermedio...")

        # Primero, reemplazar acciones repetidas
        optimized_lines = self.replacement_repeated_actions()

        # Por ultimo, propagacion de constantes a partir de las lineas sin acciones repetidas
        self.constant_propagation(optimized_lines)

        # Cerrar los archivos
        self.origin.close()
        self.destiny.close()

        print("Optimizacion de codigo intermedio completado.")


    def replacement_repeated_actions(self):
        """
            Primera fase de optimización: elimina subexpresiones comunes
            
            Returns:
                list: Lista de líneas después de eliminar acciones repetidas
        """ 
        # Obtengo todas las lineas del archivo y las guardo en una lista
        lines = self.origin.readlines()       

        # Creo una lista para guardar las lineas optimizadas
        optimized_lines = []

        # Recorre todas las lineas del archivo (linea a linea)
        for line in lines:
            # Elimino los espacios al principio y al final de la linea
            line = line.strip()

            # Si la linea no está vacía
            if not line:
                # Voy al siguiente ciclo del bucle
                continue

            # Preservar declaraciones y control de flujo
            if line.startswith("Declaracion") or self.is_control_line(line):
                # Agrego la linea a la lista de lineas optimizadas
                optimized_lines.append(line)
                # Si la linea es una declaracion o una declaracion de flujo voy al siguiente ciclo
                continue

            # Divido la linea en partes a partir del igual
            parts = line.split('=')
            if len(parts) != 2:
                # Si la linea no tiene un igual, voy al siguiente ciclo
                continue

            # En cambio, si la linea tiene un igual, estoy ante una asignacion
            
            # Obtengo la parte izquierda y derecha de la linea
            variable    = parts[0].strip() # Parte izquierda (variable o temporal)
            expression   = parts[1].strip() # Parte derecha (expresion, accion o valor)

            # Guardar la expresión original para las variables temporales
            if self.is_temporal(variable):
                self.temp_expressions[variable] = expression

                # Si la expresión es una acción repetida, la elimino
                if expression in self.actions:
                    # Usar el temporal existente
                    variable = self.actions[expression]

                # En caso contrario, la agrego a la lista de acciones o expresiones
                else:
                    # Registrar nueva expresión
                    self.actions[expression] = variable
            
            # Sea el caso que sea, agrego la linea optimizada (o no) a la lista
            optimized_lines.append(f"{variable} = {expression}")

        # Cuando termina el bucle for, retorno la lista de las lienas_optimizadas obtenidas
        return optimized_lines

    def constant_propagation(self, lines):
        """
            Segunda fase de optimización: propaga constantes y genera código final

            Args:
                lineas (list): Lista de líneas después del reemplazo de acciones repetidas
        """
        # Recorro las lineas optimizadas obtenidas anteriormente
        for line in lines:
            # Preservar declaraciones y control de flujo
            if line.startswith("Declaracion") or self.is_control_line(line):
                # Si la linea es una declaracion o una declaracion de flujo voy al siguiente ciclo y la dejo como esta
                self.destiny.write(f'{line}\n')
                continue

            # Divido la linea en partes a partir del igual
            parts = line.split('=')

            # Si la linea no tiene un igual, voy al siguiente ciclo
            if len(parts) != 2:
                continue

            # En cambio, si la linea tiene un igual, estoy ante una asignacion

            # Obtengo la parte izquierda y derecha de la linea
            variable    = parts[0].strip() # Parte izquierda (variable o temporal)
            expression   = parts[1].strip() # Parte derecha (expresion, accion o valor)

            # Si la expresión contiene un temporal, obtener su expresión original
            if self.is_temporal(expression.strip()):
                expression = self.get_temporal_expression(expression.strip())

            # Evaluar la expresión
            result = self.evaluate_expression(expression)

            # Si se pudo evaluar la expresion
            if result is not None:
                # Determina si la variable en la linea es un temporal
                if self.is_temporal(variable):
                    # Si es un temporal, reemplazo su valor por el resultado de la expresion, en mi lista de temporales
                    self.temporary[variable] = str(result)
                else:
                    # Si no es un temporal, entonces es una variable
                    self.variables[variable] = str(result)

                    # Escribo la linea con el valor de la variable en el archivo
                    self.destiny.write(f"{variable} = {result}\n\n")
                
            # De lo contrario, si no se pudo evaluar la expresion
            else:
                # Si la variable en la linea no es un temporal
                if not self.is_temporal(variable):
                    # Divide la expresion en subcadenas a partir de los espacios en blanco, y guarda las subcadenas en una lista
                    expr_parts = expression.split()

                    # Recorro las partes de la expresion
                    for i, part in enumerate(expr_parts):
                        # Si la parte es un temporal
                        if self.is_temporal(part):
                            # Reemplazo el temporal por el resultado de su expresion original
                            expr_parts[i] = self.get_temporal_expression(part)

                    # Despues de procesar todas las partes comienza la Reconstrucción y Escritura de la Expresión Final:
                    final_expression = ' '.join(expr_parts)  # Se reconstruye la expresión completa uniendo las partes con espacios

                    # Escribo en el archivo la variable con su expresion optimizada
                    self.destiny.write(f"{variable} = {final_expression}\n")
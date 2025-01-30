import re

class Optimizer:
    """ 
        Clase dedicada a la optimizacion de codigo intermedio de tres direcciones.
    """

    def __init__(self):
        """ 
            Constructor de la Clase Optimizador.
        """ 
        self.origin     = open("output/codigoIntermedio.txt", "r") # archivo de codigo intermedio
        self.destiny    = open("output/codigoIntermedioOptimizado.txt", "w+") # archivo de codigo optimizado
        self.actions   = dict() # diccionario de acciones para evaluar acciones repetidas
        self.constants = dict() # diccionario de constantes para evaluar la propagacion de constantes
    
    def optimize_intermediate_code(self):
        """ 
            Funcion principal para comenzar a optimizar el codigo intermedio de tres direcciones.
        """
        print("Optimizando codigo intermedio...")

        self.replacement_repeated_actions()

        self.propagation_of_constants()

        # Cerrar los archivos
        self.origin.close()
        self.destiny.close()

        print("Optimizacion de codigo intermedio completado.")

    def replacement_repeated_actions(self):
        """ 
            Metodo para reemplazar todas las acciones repetidas dentro del codigo intermedio
        """
        # Lee la primera linea del archivo 'origen'
        line = self.origin.readline()

        # Continua leyendo hasta que la línea esté vacía (fin del archivo)
        while line: # Procesar la linea
            # Verificar si la línea comienza con 't' seguido de un número (tX)
            if re.match(r'^t\d+ =', line):
                # Dividir la línea en dos partes usando el signo igual
                parts = line.split('=')

                # Obtenemos cada parte de la linea sin espacios al inicio y al final
                key = parts[1].strip()  # Accion u operacion
                value = parts[0].strip()  # Variable o identificador

                # Verificar si hay valores (acciones repetidas) a reemplazar en la clave 
                for getValue in self.actions.values():  
                    # Si el valor del diccionario es una lista, entonces hay acciones repetidas por reemplazar
                    if isinstance(getValue, list):
                        # Recorro la lista de valores con acciones repetidas
                        for ii in range(1, len(getValue)):  # Empezar desde 1 para evitar el primer valor
                            # Obtengo el valor que guarda la accion repetida
                            value_to_replace = getValue[ii]

                            # Si el valor esta dentro de la clave (accion) entonces lo reemplazo por el primer valor de la lista (que guarda la accion original)
                            if value_to_replace in key:
                                key = re.sub(r'\b{}\b'.format(re.escape(value_to_replace)), getValue[0], key)

                # Actualizar el diccionario self.acciones
                if key in self.actions:
                    self.actions[key].append(value)
                else:
                    # Escribo en el diccionario la accion
                    self.actions[key] = [value]

                    # Escribo en el archivo de destino el codigo optimizado
                    self.destiny.write(f'{value} = {key}\n')
            
            else:
                parts = line.split('=') # Dividir la línea en dos partes usando el signo igual

                if len(parts) == 2:
                    # Optenemos cada parte de la linea sin espacios al inicio y al final
                    identifier  = parts[0].strip()  
                    assigned_value = parts[1].strip()

                    # Verificar si hay valores (acciones repetidas) a reemplazar en la clave 
                    for getValue in self.actions.values():
                        # Si el valor del diccionario es una lista, entonces hay acciones repetidas por reemplazar
                        if isinstance(getValue, list):
                            # Recorro la lista de valores con acciones repetidas
                            for ii in range(1, len(getValue)):  # Empezar desde 1 para evitar el primer valor
                                # Obtengo el valor que guarda la accion repetida
                                value_to_replace = getValue[ii]

                                # Si el valor esta dentro del valor asignado entonces lo reemplazo por el primer valor de la lista (que guarda la accion original)
                                if value_to_replace in assigned_value:
                                    assigned_value = re.sub(r'\b{}\b'.format(re.escape(value_to_replace)), getValue[0], assigned_value)

                    line = f'{identifier} = {assigned_value}\n'

                # Escribo en el archivo la linea actual
                self.destiny.write(f'{line}')

            # Leer la siguiente línea
            line = self.origin.readline()

    def propagation_of_constants(self):
        """ 
            Leer el archivo sin acciones repetidas para aplicar propagacion de constantes.
        """
        self.destiny.seek(0) # Vuelve al inicio del archivo para releerlo desde el principio.

        lines = self.destiny.readlines() # Leer todas las lineas del archivo

        self.destiny.seek(0) # Vuelve al inicio del archivo para sobreescribirlo

        self.destiny.truncate(0) # Limpia el archivo de destino antes de escribir en él.

        # Patrón para un identificador válido en C seguido de ' = ' y un número
        identifier_patron = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]* = \d+$')

        # Patrón para un identificador válido en C seguido de ' = ' y una opercion de dos operandos
        operation_identifier_patron = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]* = \d+(\.\d+)? [\+\-\*/] \d+(\.\d+)?$')

        # bandera que se activa cuando se modifica una linea
        were_changes = False

        # Recorro el archivo (linea a linea) en busca de propagacion de constantes
        for line in lines:
            print(f"Procesando línea: {line}")  # Línea de depuración

            # Verificar si la línea tiene el patrón identificador_espacio_igual_un_numero
            if identifier_patron.match(line.strip()):
                # Obtener el identificador y el valor de la línea

                parts = line.split('=') # Dividir la línea en dos partes usando el signo igual

                # Obtenemos cada parte de la linea sin espacios al inicio y al final
                variable = parts[0].strip() # variable o identificador
                value    = parts[1].strip() # valor u operacion asignada a la variable

                # Agrego al diccionario la variable asociado a su valor
                self.constants[variable] = value

                # Escribe en el archivo la asignacion directa
                self.destiny.write(f'{variable} = {value}\n')

            # Si es una asignacion de una operacion matematica
            elif operation_identifier_patron.match(line.strip()):
                # Obtener el identificador y la operación de la línea
                parts = line.split('=') # Dividir la línea en dos partes usando el signo igual

                # Obtenemos cada parte de la linea sin espacios al inicio y al final
                variable = parts[0].strip()
                operation = parts[1].strip()

                try:
                    # Evaluar la operacion matematica para obtener una constante como resultado
                    resulting_constant = eval(operation)

                    # Si la variable no esta dentro de las constantes guardadas, o si hay que reemplazarla por una nueva
                    self.constants[variable] = str(resulting_constant)

                    # Como se modifica una linea activo la bandera
                    were_changes = True

                    print(f"Constante resultante asignada: {variable} = {resulting_constant}") # Línea de depuración

                # Si no se puede evaluar la operacion
                except Exception as e:
                    self.destiny.write(f'{line}\n')
                    print(f"Error evaluando operación: {e}")

            # En caso contrario, si hay una accion, busco si tiene una constante que debe ser reemplazada
            else:
                original_line = line
                # Reemplazar constantes en la linea
                if self.constants:
                    # Encontrar la posición del signo igual
                    equal_pos = line.find('=')

                    # Si en la linea existe una asignacion
                    if equal_pos != -1:
                        # Divido la linea en dos partes a partir del '='
                        left = line[:equal_pos + 1]
                        right = line[equal_pos + 1:]

                        # Reemplazar la clave solo en la parte derecha
                        for key, value in self.constants.items():
                            right = re.sub(r'\b{}\b'.format(re.escape(key)), value, right)

                        # Concateno la nueva linea si hubo cambios o la restauro en caso de que no
                        line = left + right

                # Si la linea orignal fue modificada:
                if line != original_line:
                    were_changes = True # Activo la bandera
                    print(f"Línea modificada: {line}") # Linea de depuracion

                self.destiny.write(f'{line}')
        
        # Si se modifico al menos una liena
        if were_changes:
            print("Hubo cambios, llamando recursivamente a propagacionConstantes") # Línea de depuración
            self.propagation_of_constants() # Llamada recursiva
        else:
            print("No hubo cambios, finalizando propagation_of_constants") # Línea de depuración


""" 

x = (a * b - c) + (a * b + d)

// Codigo  de tres direcciones:
t0 =  a * b 
t1 = t0 - c
t2 = a * b   // Tengo operaciones repetidas
t3 = t2 + d
t4 = t1 + t3
x = t4

// Reemplazo de acciones repetidas:
t0 =  a * b 
t1 = t0 - c
t3 = t0 + d
t4 = t1 + t3  // En otra pasada podemos decir que estas ultimas dos instrucciones se plegan en una sola
x = t4

Propagación de constantes:

// Codigo en C
x = 5
y = x * 2 - 10
z = y + x;

// Codigo de tres direcciones
x = 5
t0 = x * 2
t1 = t0 - 10
y = t1
t2 = y + x
z = t2

// Propagacion de constantes
x = 5
t0 = 5 * 2
t1 = t0 - 10
y = t1
t2 = y + 5
z = t2

// En la siguiente pasada:
x = 5
t1 = 10 - 10
y = t1
t2 = y + 5
z = t2

// En la siguiente pasada:
x = 5
y = 0
t2 = y + 5
z = t2

// En la siguiente pasada:
x = 5
y = 0
z = 5

// Entonces la optimizacion lo resuelve y obtenemos, en este caso, asignaciones directas
 """
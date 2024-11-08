from typing import Optional
from Context import Context
from Id import Id

class SymbolTable:
    #Class variable that will store the single instance
    _instance = None
    
    _contexts: list[Context] = []
    """
    Think of __new__ as a "template" and __init__ as the "decoration" of the created
    object. In the case of the Singleton, we want to make sure that only a 
    single template is used, so we use __new__ to control that part. 
    super() is what allows us to access the actual process of creating the template (instance).
    """
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SymbolTable, cls).__new__(cls)
            #Optional
            #cls._instance.contexts = []  #Initializes the context list
        return cls._instance

    def add_context(self, name):
        """
        Agrega un nuevo contexto a la lista de la tabla de simbolos.
        """
        new_context = Context(name)
        self._contexts.append(new_context)

    def del_context(self):
        if self._contexts:
            self._contexts.pop()
        
    def get_contexts(self):
        return self._contexts

    def add_identifier(self, id: Id):
        #self.contexts[-1] accesses the last element in the self.contexts list.
        #This suggests that contexts are added to this list at some other point 
        #in the code, and the last context in the list is the "active context".
        if self._contexts:
            self._contexts[-1].add_identifier(id)
        
    def local_search(self, name: str) -> Optional[Id]:
        """
        Busca localmente en un Contexto el nombre de una variable o funcion
        Retorna el valor del ID encontrado o None si no existe
        """
        if self._contexts:
            return self._contexts[-1].search_id(name)
        return None

    def global_search(self, name: str) -> Optional[Id]:
        """ 
        Este método recorre la lista de contextos en orden inverso y utiliza 
        el método `buscarID` de cada contexto para intentar encontrar un 
        identificador que coincida con el nombre proporcionado.

        Args:
            nombre (str): El nombre del identificador que se desea buscar.

        Returns:
            ID: El identificador encontrado si existe en alguno de los contextos; 
            de lo contrario, devuelve None si no se encuentra o si la lista de 
            contextos está vacía.
        """
        if self._contexts:
            for context in reversed(self._contexts):
                _id = context.search_id(name)
                if _id:
                    return _id
        return None
    
    def update_used(self, name:str):
        """
            Busca localmente en un Contexto el nombre de una variable o funcion y 
            si no esta usado actualiza su estado a usado. El identificador debe
            existir en la tabla de simbolo, caso contrario no hace nada.
        """
        identifier = self.global_search(name)
        if identifier.get_used() is False: # Si el ID no esta usado
            identifier.set_used() # Setea su valor a usado

    def show_current_context (self):
        """ 
        Retorna el toString del Contexto actual
        """
        
        if self._contexts:
            return self._contexts[-1].__str__()

    def get_context_name(self):
        """
        Retorna el nombre del Contexto actual
        """
        if self._contexts:
            return self._contexts[-1].name
        return "Sin Contexto"
    
    def __str__(self):
        """
        Retorna el toString de la tabla de simbolos
        """
        
        return f"TablaSimbolos(contextos={self._contexts})"
    
    
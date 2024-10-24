from typing import Optional
from Context import Context
from Id import Id

class SymbolTable:
    #Class variable that will store the single instance
    _instance = None
    
    """
    Think of __new__ as a "template" and __init__ as the "decoration" of the created
    object. In the case of the Singleton, we want to make sure that only a 
    single template is used, so we use __new__ to control that part. 
    super() is what allows us to access the actual process of creating the template (instance).
    """
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SymbolTable, cls).__new__(cls)
            cls._instance.contexts = []  #Initializes the context list
        return cls._instance

    def add_context(self, context: Context=None):
        """
        Add a context to the contexts list. If no context is provided, a new Context 
        instance will be created and added.

        :param context: context to be added. By defect it's None
        """
        if context is None:
            #Here you are creating a new instance of the Context class. 
            #The parentheses () indicate that you are calling the class 
            #constructor (__init__), which creates a new object.
            #If no context is provided, create a new instance of Context
            self.contexts.append(Context())
        else:
            #If a context is provided, add it directly
            self.contexts.append(context)

    def del_context(self) -> Optional[Context]:
        if self.contexts:
            return self.contexts.pop()
        else:
            return None

    def add_identifier(self, id: Id):
        #self.contexts[-1] accesses the last element in the self.contexts list.
        #This suggests that contexts are added to this list at some other point 
        #in the code, and the last context in the list is the "active context".
        if self.contexts:
            self.contexts[-1].add_identifier(id)
        else:
            raise RuntimeError("There's no active context")
        
    def local_search(self, name: str) -> Optional[Id]:
        if self.contexts:
            return self.contexts[-1].search(name)
        return None

    def global_search(self, name: str) -> Optional[Id]:
        for context in reversed(self.contexts):
            _id = context.search(name)
            if _id:
                return _id
        return None
    
    def __str__(self):
        return "\n".join(str(context) for context in self.contexts)
    
    
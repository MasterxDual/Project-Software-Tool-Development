from enum import Enum
from abc import ABC, abstractmethod #ABC: abstract base class

class DataType(Enum):
    INT = 1
    FLOAT = 2
    CHAR = 3
    DOUBLE = 4
    VOID = 5

class Id(ABC):
    def __init__(self, name: str, data_type: DataType):
        self._name = name
        self._data_type = data_type
        self.initialized = False
        self.used = False

    """
    @property defines a getter, allowing you to access an
    attribute as if it were a property, even though it is 
    actually a method.
    """
    #Getter of attribute name
    @property
    def name(self) -> str:
        return self._name

    """
    @name.setter defines a setter, which allows you to modify an 
    attribute and add logic to control what values ​​are assigned.
    These decorators (@property and @name.setter) provide encapsulation 
    and validation, which improves code robustness without sacrificing simplicity of use.
    """
    @name.setter
    def name(self, value: str):
        self._name = value

    #Getter of attribute data_type
    @property
    def data_type(self) -> DataType:
        return self._data_type

    def is_initialized(self) -> bool:
        return self.initialized

    def set_used(self):
        self.used = True

    @abstractmethod
    def get_type(self) -> str:
        """
        Abstract method that will be implemented by the subclasses.\n. 
        It will show if the class that calls it its a 'Variable' or a 'Function'.\n.
        ->str indicates that the get_type() method should return an object of type str (string).

        :param self: id called by the class used in that instance
        :return: a string indicating if its a 'Variable' or a 'Function'
        """
        pass

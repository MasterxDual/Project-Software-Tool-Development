#List typing allows you to specify the type of items contained in a list.
#This provides more detailed information about the contents of the list.
from typing import List 
from Id import Id, DataType

#The parameter in the class Function means that Function inherits (hereda) from Id
class Function(Id):
    def __init__(self, name: str, data_type: DataType):
        super().__init__(name, data_type)
        self.args: List[Id] = []

    def add_arg(self, arg: Id):
        self.args.append(arg)

    def get_args(self) -> List[Id]:
        return self.args
    
    def get_type(self) -> str:
        return "Function"

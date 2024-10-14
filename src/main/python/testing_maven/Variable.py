from Id import Id, DataType

class Variable(Id):
    def __init__(self, name:str, data_type: DataType):
        super().__init__(name, data_type)
    
    def get_type(self) -> str:
        return "Variable"
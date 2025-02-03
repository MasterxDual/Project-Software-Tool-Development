from typing import Dict
from Id import Id

class Context:
    def __init__(self, name):
        self.tabla: Dict[str, Id] = {}
        self.name = name

    def add_identifier(self, id: Id):
        self.tabla[id.name] = id

    def search_id(self, name: str) -> Id:
        return self.tabla.get(name)
    
    def get_identifiers(self) -> dict:
        return self.tabla
    
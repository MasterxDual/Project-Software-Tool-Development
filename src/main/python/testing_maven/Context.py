from typing import Dict
from Id import Id

class Context:
    def __init__(self):
        self.tabla: Dict[str, Id] = {}

    def add_identifier(self, id: Id):
        self.tabla[id.name] = id

    def search(self, name: str) -> Id:
        return self.tabla.get(name)
    
    def __str__(self):
        return f"Context with identifiers: {list(self.tabla.keys())}"

"""
Classe Function : Stocke la définition d'une fonction utilisateur.
"""

class Function:
    def __init__(self, name, param_name, body_tokens):
        self.name = name
        self.param_name = param_name
        self.body_tokens = body_tokens

    def __repr__(self):
        return f"Function {self.name}({self.param_name})"
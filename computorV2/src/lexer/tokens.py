"""
Définit les types de Tokens (ID, NUM, PLUS, EQUAL, MATRIX_START, etc.).
"""

from enum import Enum, auto

class TokenType(Enum):

    NUMBER = auto()
    ID = auto()
    IMAGINARY = auto()

    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    POW = auto() # ^
    MAT_MUL = auto() # multi matricielle **

    ASSIGN = auto() # =
    QUESTION = auto() # ?

    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()

    COMMA = auto() # separe colonne matrice ou args
    SEMICOLON = auto() # separe ligne matrice
    
    EOF = auto()
    
class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        
    def __repr__(self):
        if self.value:
            return f"{self.type.name}({self.value})"
        return f"{self.type.name}"

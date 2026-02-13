"""
Gestion des exceptions personnalisées (SyntaxError, MathError).
"""
class ComputorError(Exception):
    pass

class MathError(ComputorError):
    pass

class ParseError(ComputorError):
    pass

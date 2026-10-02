from src.utils.errors import MathError

class Context:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.history = []

    def add_to_history(self, command, result):
        self.history.append(f"{command} -> {result}")

    def set_variable(self, name, value):
        name = name.lower()
        if name == 'i':
            raise MathError("Cannot reassign imaginary unit 'i'")
        self.variables[name] = value

    def get_variable(self, name):
        name = name.lower()
        if name in self.variables:
            return self.variables[name]
        raise MathError(f"Unknown variable '{name}'")

    def get_variable_safe(self, name):
        return self.variables.get(name.lower(), None)

    def set_function(self, name, func_obj):
        self.functions[name.lower()] = func_obj

    def get_function(self, name):
        return self.functions.get(name.lower(), None)
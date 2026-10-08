"""
Analyse la liste de tokens et construit l'AST (Abstract Syntax Tree).
"""
import copy
from src.lexer.tokens import TokenType
from src.lexer.list_lexer import ListLexer
from src.utils.errors import ParseError, MathError
from src.core.rational import Rational
from src.core.complex import Complex
from src.core.matrix import Matrix
from src.core.polynomial import Polynomial
from src.core.context import Context
from src.core.function import Function

class Parser:
    def __init__(self, lexer, context=None, is_solving=False):
        self.lexer = lexer
        self.context = context if context else Context()
        self.current_token = self.lexer.get_next_token()
        self.is_solving = is_solving

    def eat(self, token_type): #compare avec type attendu, avance ou error
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise ParseError(f"Expected {token_type}, got {self.current_token.type}")

    def expect_end(self): # leftover tokens mean the input was not fully understood
        if self.current_token.type != TokenType.EOF:
            raise ParseError(f"Expected end of input, got {self.current_token.type}")

    def parse(self):
        #Assignation de variable
        if (self.current_token.type == TokenType.ID and self.lexer.peek_token(1).type == TokenType.ASSIGN):
            return self.assignment()

        #Definition de fonction
        if (self.current_token.type == TokenType.ID and
            self.lexer.peek_token(1).type == TokenType.LPAREN and
            self.lexer.peek_token(2).type == TokenType.ID and
            self.lexer.peek_token(3).type == TokenType.RPAREN and
            self.lexer.peek_token(4).type == TokenType.ASSIGN):
            return self.definition()

        node = self.expr()
        self.expect_end()
        return node

    #ACTIONS

    def assignment(self):
        var_name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.ASSIGN)
        val = self.expr()
        self.expect_end()
        self.context.set_variable(var_name, val)
        return val

    def definition(self):
        func_name = self.current_token.value
        self.eat(TokenType.ID)         # f
        self.eat(TokenType.LPAREN)     # (
        param_name = self.current_token.value
        self.eat(TokenType.ID) # x
        self.eat(TokenType.RPAREN)     # )
        self.eat(TokenType.ASSIGN)     # =

        body_tokens = []
        while self.current_token.type != TokenType.EOF:
            body_tokens.append(self.current_token)
            self.eat(self.current_token.type)

        self.check_body(param_name, body_tokens)
        func = Function(func_name, param_name, body_tokens)
        self.context.set_function(func_name, func)
        return func

    def check_body(self, param_name, body_tokens): # syntax errors show up now, not at the first call
        local_context = copy.deepcopy(self.context)
        local_context.set_variable(param_name, Polynomial({1: Complex(1)}, var_name=param_name))
        sub_parser = Parser(ListLexer(body_tokens), local_context, is_solving=True)
        try:
            sub_parser.expr()
            sub_parser.expect_end()
        except (MathError, TypeError):
            # the parameter has no value yet, so only a ParseError means the body is wrong
            pass

    def resolve_function_call(self, func_obj, arg_value):
        local_context = copy.deepcopy(self.context)
        local_context.set_variable(func_obj.param_name, arg_value)
        
        list_lexer = ListLexer(func_obj.body_tokens)
        sub_parser = Parser(list_lexer, local_context)
        result = sub_parser.expr()
        sub_parser.expect_end()
        return result

    # NIVEAU 1 : Nombres, Parentheses
    def factor(self):
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Rational(token.value)
        
        if token.type == TokenType.IMAGINARY:
            self.eat(TokenType.IMAGINARY)
            return Complex(0, 1)

        if token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

        if token.type == TokenType.LBRACKET:
            return self.matrix()

        if token.type == TokenType.ID:
            name = token.value.lower()
            if self.lexer.peek_token(1).type == TokenType.LPAREN:
                self.eat(TokenType.ID)
                self.eat(TokenType.LPAREN)
                arg_value = self.expr()
                self.eat(TokenType.RPAREN)
                fun_obj = self.context.get_function(name)
                if not fun_obj:
                    raise ParseError(f"Unknown function '{name}'")
                return self.resolve_function_call(fun_obj, arg_value)
            self.eat(TokenType.ID)
            var_val = self.context.get_variable_safe(name)
            if var_val is not None:
                return var_val
            if self.is_solving:
                return Polynomial({1: Complex(1)}, var_name=name)
                
            raise ParseError(f"Unknown variable '{name}'")

        raise ParseError(f"Unexpected {token.type}")

    # GESTION DES MATRICES
    def matrix(self):
        self.eat(TokenType.LBRACKET)
        data = []

        while self.current_token.type == TokenType.LBRACKET:
            self.eat(TokenType.LBRACKET)
            row = []
            row.append(self.expr())

            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                row.append(self.expr())

            self.eat(TokenType.RBRACKET)
            data.append(row)

            if self.current_token.type == TokenType.SEMICOLON:
                self.eat(TokenType.SEMICOLON)
        
        self.eat(TokenType.RBRACKET)
        return Matrix(data)


    # NIVEAU 2 : Puissances
    def power(self):
        node = self.factor()

        if self.current_token.type == TokenType.POW:
            self.eat(TokenType.POW)
            # the exponent goes back through unary(): 2^3^2 is 2^(3^2), and 2^-1 works
            node = node ** self.unary()

        return node

    # unary minus sits above ^ so that -2^2 is -(2^2)
    def unary(self):
        if self.current_token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return self.unary() * Rational(-1)
        if self.current_token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            return self.unary()
        return self.power()

    # NIVEAU 3 : Termes(*, /, %, **)
    def term(self):
        node = self.unary()
        valid_ops = (TokenType.MUL, TokenType.DIV, TokenType.MOD, TokenType.MAT_MUL)
        implicit_muls = (TokenType.ID, TokenType.LPAREN)

        while self.current_token.type in valid_ops or self.current_token.type in implicit_muls:
            token = self.current_token

            if token.type in implicit_muls:
                node = node * self.unary()
            elif token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
                node = node * self.unary()
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
                node = node / self.unary()
            elif token.type == TokenType.MOD:
                self.eat(TokenType.MOD)
                node = node % self.unary()
            elif token.type == TokenType.MAT_MUL:
                self.eat(TokenType.MAT_MUL)
                right = self.unary()
                if not isinstance(node, Matrix):
                    raise MathError("** needs two matrices, use * for a scalar")
                node = node.matmul(right)
        return node

    # NIVEAU 4 : Expresssions (+, -)
    def expr(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                node = node + self.term()
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                node = node - self.term()
        return node

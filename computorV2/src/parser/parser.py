"""
Analyse la liste de tokens et construit l'AST (Abstract Syntax Tree).
"""
import copy
from src.lexer.tokens import TokenType
from src.lexer.list_lexer import ListLexer
from src.utils.errors import ParseError
from src.core.rational import Rational
from src.core.complex import Complex
from src.core.matrix import Matrix
from src.core.context import Context
from src.core.function import Function

class Parser:
    def __init__(self, lexer, context=None):
        self.lexer = lexer
        self.context = context if context else Context()
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type): #compare avec type attendu, avance ou error
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise ParseError(f"Expected {token_type}, got {self.current_token.type}")

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
    
        return self.expr()

    #ACTIONS

    def assignment(self):
        var_name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.ASSIGN)
        val = self.expr()
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
        while self.current_token.type != TokenType.EOF and self.current_token.type != TokenType.SEMICOLON:
            body_tokens.append(self.current_token)
            self.eat(self.current_token.type)

        func = Function(func_name, param_name, body_tokens)
        self.context.set_function(func_name, func)
        return func

    def resolve_function_call(self, func_obj, arg_value):
        local_context = copy.deepcopy(self.context)
        local_context.set_variable(func_obj.param_name, arg_value)
        
        list_lexer = ListLexer(func_obj.body_tokens)
        sub_parser = Parser(list_lexer, local_context)
        return sub_parser.expr()

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
            name = token.value
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
            return self.context.get_variable(name)
        raise ParseError(f"Unexpected token: {token}")

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

        while self.current_token.type == TokenType.POW:
            token = self.current_token
            self.eat(TokenType.POW)
            node = node ** self.factor()

        return node

    # NIVEAU 3 : Termes(*, /, %, **)
    def term(self):
        node = self.power()

        while self.current_token.type in (TokenType.MUL, TokenType.DIV, TokenType.MOD, TokenType.MAT_MUL):
            token = self.current_token

            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
                node = node * self.power()
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
                node = node / self.power()
            elif token.type == TokenType.MOD:
                self.eat(TokenType.MOD)
                node = node % self.power()
            elif token.type == TokenType.MAT_MUL:
                self.eat(TokenType.MAT_MUL)
                node = node * self.power()
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

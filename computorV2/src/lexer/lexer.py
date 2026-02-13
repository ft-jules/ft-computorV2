"""
Transforme une chaîne de caractères (input) en une liste de Tokens.
"""

from src.lexer.tokens import Token, TokenType

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        
        self.simple_tokens = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '/': TokenType.DIV,
            '%': TokenType.MOD,
            '^': TokenType.POW,
            '=': TokenType.ASSIGN,
            '?': TokenType.QUESTION,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            ';': TokenType.SEMICOLON,
            ',': TokenType.COMMA
        }

    def error(self):
        raise ParseError(f"Invalid character '{self.current_char}' at position {self.pos}")

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None

    def peek_token(self, offset=1):
        saved_pos = self.pos
        saved_char = self.current_char
        token = None
        for _ in range(offset):
            token = self.get_next_token()
            if token.type == TokenType.EOF:
                break
        self.pos = saved_pos
        self.current_char = saved_char
        
        return token

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.' and '.' in result:
                break
            result += self.current_char
            self.advance()

        if '.' in result:
            return Token(TokenType.NUMBER, float(result))
        return Token(TokenType.NUMBER, int(result))

    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        lower_result = result.lower()

        if lower_result == 'i':
            return Token(TokenType.IMAGINARY, 'i')

        return Token(TokenType.ID, lower_result)


    def get_next_token(self):
        while self.current_char is not None:
            
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit() or self.current_char == '.':
                return self.number()

            if self.current_char.isalpha():
                return self.identifier()

            if self.current_char == '*':
                if self.peek() == '*':
                    self.advance()
                    self.advance()
                    return Token(TokenType.MAT_MUL)
                self.advance()
                return Token(TokenType.MUL)

            if self.current_char in self.simple_tokens:
                token_type =  self.simple_tokens[self.current_char]
                self.advance()
                return Token(token_type)

            self.error()

        return Token(TokenType.EOF)

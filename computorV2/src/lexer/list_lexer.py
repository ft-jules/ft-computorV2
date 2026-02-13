from .tokens import Token, TokenType

class ListLexer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def get_next_token(self):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        return Token(TokenType.EOF, "")

    def peek_token(self, step=1):
        target_index = self.pos + step - 1
        if target_index < len(self.tokens):
            return self.tokens[target_index]
        return Token(TokenType.EOF, "")
"""
Classe Function : Stocke la définition d'une fonction utilisateur.
"""
from src.lexer.tokens import TokenType

BINARY_OPS = {
    TokenType.PLUS: "+",
    TokenType.MINUS: "-",
    TokenType.MUL: "*",
    TokenType.DIV: "/",
    TokenType.MOD: "%",
    TokenType.MAT_MUL: "**",
}

# after one of these, a + or - is a sign and not an operator
SIGN_CONTEXT = (TokenType.LPAREN, TokenType.LBRACKET, TokenType.COMMA, TokenType.SEMICOLON, TokenType.POW)

PLAIN_TOKENS = {
    TokenType.IMAGINARY: "i",
    TokenType.POW: "^",
    TokenType.LPAREN: "(",
    TokenType.RPAREN: ")",
    TokenType.LBRACKET: "[",
    TokenType.RBRACKET: "]",
    TokenType.COMMA: ", ",
    TokenType.SEMICOLON: "; ",
}

def format_value(value): # a value put back in a body must read as one block
    if hasattr(value, "inline"):
        return value.inline()
    text = str(value)
    if " " in text:
        return f"({text})"
    return text

def format_body(tokens): # rebuilds the body as typed, with the subject's spacing
    out = ""
    prev = None
    for tok in tokens:
        t = tok.type
        if t in BINARY_OPS:
            is_sign = t in (TokenType.PLUS, TokenType.MINUS) and (prev is None or prev.type in BINARY_OPS or prev.type in SIGN_CONTEXT)
            if is_sign:
                out += BINARY_OPS[t]
            else:
                out += f" {BINARY_OPS[t]} "
        else:
            # 4x and 2(x + 1) are implicit products, the subject prints them as 4 * x
            if prev is not None and prev.type in (TokenType.NUMBER, TokenType.ID, TokenType.IMAGINARY, TokenType.RPAREN):
                is_call = prev.type == TokenType.ID and t == TokenType.LPAREN
                if t in (TokenType.ID, TokenType.IMAGINARY, TokenType.NUMBER, TokenType.LPAREN) and not is_call:
                    out += " * "
            if t == TokenType.NUMBER:
                out += format_value(tok.value)
            elif t == TokenType.ID:
                out += str(tok.value)
            else:
                out += PLAIN_TOKENS.get(t, "")
        prev = tok
    return out

class Function:
    def __init__(self, name, param_name, body_tokens):
        self.name = name
        self.param_name = param_name
        self.body_tokens = body_tokens

    def __repr__(self):
        return format_body(self.body_tokens)

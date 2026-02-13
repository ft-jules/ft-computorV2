"""
Point d'entrée du programme. Lance le shell interactif.
"""

"""
BONUS:
division par des fractions avec la sous couche de rationels Expression
pas avec methode float sale car (2^1/2)^2 = 1.99999999

faire une interface pour le projet
"""

import sys
import readline
from src.lexer.lexer import Lexer
from src.lexer.tokens import TokenType
from src.parser.parser import Parser
from src.core.context import Context
from src.core.polynomial import Polynomial
from src.core.rational import Rational
from src.core.complex import Complex
from src.utils.errors import MathError, ParseError

def find_unknown_variable(text, context):
    lexer = Lexer(text)
    token = lexer.get_next_token()

    unknowns = set()

    while token.type != TokenType.EOF:
        if token.type == TokenType.ID:
            var_name = token.value
            if context.get_variable_safe(var_name) is None:
                if context.get_function(var_name) is None:
                    unknowns.add(var_name)
        token = lexer.get_next_token()
    
    if len(unknowns) == 0:
        return None
    elif len(unknowns) == 1:
        return unknowns.pop()
    else:
        raise MathError(f"Multiple unknowns found: {', '.join(unknowns)}. Can only solve univariate equations.")



def handle_equation(line, context):
    expression_text = line.replace('?', '')
    if '=' not in expression_text:
        print("Synthax Error: Equation must contain '='")
        return
    parts = expression_text.split('=')
    if len(parts) != 2:
        print("Synthax Error: Equation must have two parts separated by '='")
        return
    left_str = parts[0]
    right_str = parts[1]

    import copy

    try:
        unknown_name = find_unknown_variable(expression_text, context)
        equation_ctx = copy.deepcopy(context)
        if unknown_name:
            X = Polynomial({1: 1}, var_name=unknown_name)
            equation_ctx.set_variable(unknown_name, X)
        else:
            pass
        left_val = Parser(Lexer(left_str), equation_ctx).parse()
        right_val = Parser(Lexer(right_str), equation_ctx).parse()
        final_poly = left_val - right_val

        if not isinstance(final_poly, Polynomial):
            final_poly = Polynomial({0: final_poly})
        final_poly.solve(unknown_name if unknown_name else 'X')

    except (MathError, ParseError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ["--gui", "g"]:
        from src.gui.window import ComputorGui
        global_context = Context()
        app = ComputorGui(global_context)
        app.run()
        return
    print("Welcome to ComputorV2!")
    print("Type 'exit' to quit.")

    global_context = Context()

    while True:
        try:
            text = input("> ").strip()
            if not text:
                continue
            if text.lower() in ["exit", "quit"]:
                break
            if '?' in text:
                hanlde_equation(text, global_context)
            else:
                lexer = Lexer(text)
                parser = Parser(lexer, global_context)
                result = parser.parse()
                if result is not None:
                    print(result)
        except (MathError, ParseError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

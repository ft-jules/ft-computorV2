"""
Point d'entrée du programme. Lance le shell interactif.
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
    # In "... = ... ?" the user asks to solve, so a name can be the unknown even if it already
    # has a value: after x = 2 from the subject, funA(x) = y ? must still solve for x.
    tokens = []
    lexer = Lexer(text)
    token = lexer.get_next_token()
    while token.type != TokenType.EOF:
        tokens.append(token)
        token = lexer.get_next_token()

    names = []
    call_args = []
    for idx, tok in enumerate(tokens):
        if tok.type != TokenType.ID:
            continue
        is_call = idx + 1 < len(tokens) and tokens[idx + 1].type == TokenType.LPAREN
        if is_call and context.get_function(tok.value) is not None:
            if idx + 3 < len(tokens) and tokens[idx + 2].type == TokenType.ID and tokens[idx + 3].type == TokenType.RPAREN:
                call_args.append(tokens[idx + 2].value)
            continue
        if tok.value not in names:
            names.append(tok.value)

    undefined = [n for n in names if context.get_variable_safe(n) is None]
    if len(undefined) == 1:
        return undefined[0]
    if len(undefined) > 1:
        raise MathError(f"Multiple unknowns found: {', '.join(undefined)}. Can only solve univariate equations.")
    # every name has a value: a single name is the unknown, else the argument of funA(x)
    if len(names) == 1:
        return names[0]
    call_args = list(dict.fromkeys(call_args))
    if len(call_args) == 1:
        return call_args[0]
    return None



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
        left_val = Parser(Lexer(left_str), equation_ctx, is_solving=True).parse()
        right_val = Parser(Lexer(right_str), equation_ctx, is_solving=True).parse()
        final_poly = left_val - right_val

        if not isinstance(final_poly, Polynomial):
            final_poly = Polynomial({0: final_poly})
        final_poly.solve(unknown_name if unknown_name else 'X')

    except (MathError, ParseError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ["--gui", "-g"]:
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
            
            if text.lower() == "history":
                if not global_context.history:
                    print("History is empty.")
                else:
                    print("\n".join(global_context.history))
                continue

            if text.lower() == "vars":
                if not global_context.variables:
                    print("No variables stored.")
                else:
                    for name, val in global_context.variables.items():
                        print(f"{name} = {val}")
                continue
            
            needs_solving = ('=' in text) or ('?' in text)
            if '?' in text:
                clean_text = text.replace('?', '').strip()
                if clean_text.endswith('='):
                    expr_to_eval = clean_text[:-1].strip()
                    lexer = Lexer(expr_to_eval)
                    parser = Parser(lexer, global_context, is_solving=True)
                    result = parser.parse()
                    if result is not None:
                        print(result)
                        global_context.add_to_history(text, str(result))
                else:
                    handle_equation(text, global_context)
                    global_context.add_to_history(text, "Equation solved")
            else:
                lexer = Lexer(text)
                parser = Parser(lexer, global_context, is_solving=needs_solving)
                result = parser.parse()
                if result is not None:
                    print(result)
                    global_context.add_to_history(text, str(result))
                else:
                    global_context.add_to_history(text, "Assigned")

        except (MathError, ParseError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)
        except EOFError: # Ctrl-D, without this the loop reads EOF forever
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

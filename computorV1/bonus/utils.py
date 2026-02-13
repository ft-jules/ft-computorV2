import re

def ft_gcd(a, b): #plus grand diviseur commun
    
    while b:
        a, b = b , a % b
    return a

def get_fraction_str(numerator, denominator):

    if not (numerator.is_integer() and denominator.is_integer()):
        return str(numerator / denominator)

    num = int(numerator)
    denom = int(denominator)

    if denom == 0:
        return "Undefined"

    if denom < 0:
        num = -num
        denom = -denom
    
    common = ft_gcd(abs(num), abs(denom))

    reduced_num = num // common
    reduced_denom = denom // common

    if reduced_denom == 1:
        return str(reduced_num)

    return f"{reduced_num}/{reduced_denom}"


def parse_terms(expression):

    expression = expression.replace(" ", "")

    # Regex cherche 4 groupes potentiels :
    # 1 : Le signe (+ ou -)
    # 2 : Le nombre (entier ou flottant)
    # 3 : La lettre "X"
    # 4 : L'exposant (après un ^)
    # Pattern permissif (? -> optionnel) pour tout accepter.
    pattern = r"([-+]?)\s*(?:(\d+(?:\.\d*)?|\.\d+))?\s*\*?\s*(X?)(?:\^(\d+))?"

    matches = re.findall(pattern, expression)
    terms = []

    for sign, num, x_char, exp in matches:
        if not num and not x_char and not exp:
            continue

    # ----------LOGIQUE DE DEDUCTION----------

        try:
            if not num:
                coef = 1.0
            else:
                coef = float(num)
        except OverflowError:
            raise ValueError(f"The coefficient '{num}' is too large (Overflow).")

        if sign == "-":
            coef = -coef

        if not x_char:
            degree = 0
        elif not exp:
            degree = 1
        else:
            degree = int(exp)

        terms.append((coef, degree))

    return terms
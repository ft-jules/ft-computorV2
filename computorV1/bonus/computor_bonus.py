import sys
import re
from utils import parse_terms, get_fraction_str


def _ft_sqrt(number):
    return number ** 0.5


def ft_sqrt(number):
    if number < 0:
        raise ValueError("Cannot calculate square root of a negative number.")
    if number == 0:
        return 0.0

    guess = float(number)
    
    diff = 1.0
    while diff > 0.0000001:
        new_guess = 0.5 * (guess + (number / guess))
        
        diff = guess - new_guess
        if diff < 0:
            diff = -diff
            
        guess = new_guess

    return guess


def solve(polynomial, degree):
    a = polynomial.get(2, 0.0)
    b = polynomial.get(1, 0.0)
    c = polynomial.get(0, 0.0)
    # ax^2+bx+c

    # --- BONUS : AFFICHAGE DES ÉTAPES ---
    print("\n--- RESOLUTION STEPS ---")
    print(f"Coefficients: a={a}, b={b}, c={c}")
    # ------------------------------------

    # 4 * X^0 = 0 ou 2 * X^0 = 2 * X^0
    if degree == 0:
        print("Degree is 0. Checking if c == 0.") # Step
        if c == 0:
            print("Every real number is a solution.")
        else:
            print("No solution.")

    # 2 * X^1 + 4 * X^0 = 0 -> X = -c / b
    elif degree == 1:
        print(f"Linear equation: {b}X = {-c}") # Step
        
        res = -c / b
        if b.is_integer() and c.is_integer():
            frac = get_fraction_str(-c, b)
            print(f"The solution is:\n{res} (or {frac})")
        else:
            print(f"The solution is:\n{res}")

    # 3 * X^2 + 2 * X^1 + 4 * X^0 = 0
    elif degree == 2:
        delta = (b * b) - (4 * a * c)

        # Step
        print(f"Calculating Delta: b^2 - 4ac = {b}^2 - 4 * {a} * {c}")
        print(f"Delta = {delta}")

        if delta > 0:
            print("Delta > 0 -> 2 real solutions.") # Step
            print("Discriminant is strictly positive, the two solutions are:")
            sqrt_delta = ft_sqrt(delta)
            #sqrt_delta = _ft_sqrt(delta)

            # (-b ± √Δ) / 2a
            sol1 = (-b - sqrt_delta) / (2 * a)
            sol2 = (-b + sqrt_delta) / (2 * a)

            print(f"{sol1}\n{sol2}")

            if sqrt_delta.is_integer() and a.is_integer() and b.is_integer():
                print("\n(Fraction form:)")
                print(get_fraction_str(-b - sqrt_delta, 2 * a))
                print(get_fraction_str(-b + sqrt_delta, 2 * a))

        elif delta == 0:
            print("Delta == 0 -> 1 unique solution.") # Step
            print("Discriminant is zero, the solution is:")
            # -b / 2a
            sol = -b / (2 * a)

            if a.is_integer() and b.is_integer():
                frac = get_fraction_str(-b, 2 * a)
                print(f"{sol} (or {frac})")
            else:
                print(f"{sol}")

        else: # delta < 0
            print("Delta < 0 -> 2 complex solutions.") # Step
            print("Discriminant is strictly negative, the two complex solutions are:")
            sqrt_delta = ft_sqrt(-delta)
            #sqrt_delta = _ft_sqrt(-delta)
            reel = -b / (2 * a)
            imag = sqrt_delta / (2 * a)

            # "X + i * Y"
            print(f"{reel} - i * {abs(imag)}")
            print(f"{reel} + i * {abs(imag)}")

            frac_reel = get_fraction_str(-b, 2 * a)
            frac_imag = get_fraction_str(sqrt_delta, 2 * a)

            if sqrt_delta.is_integer() and a.is_integer() and b.is_integer():
                print("\n(Fraction form:)")
                frac_reel = get_fraction_str(-b, 2 * a)
                frac_imag = get_fraction_str(sqrt_delta, 2 * a)
                print(f"{frac_reel} - i * {frac_imag}")
                print(f"{frac_reel} + i * {frac_imag}")
            
    print("------------------------\n")


def main():

    # ----------PARSING----------

    if len(sys.argv) != 2:
        print("Usage: python3 computor.py \"5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0\"")
        return

    equation = sys.argv[1].replace(" ", "")

    if equation.count('=') != 1:
        print("Syntax Error: The equation must contain exactly one '=' sign.")
        return

    lhs_str, rhs_str = equation.split('=')
    
    if not lhs_str or not rhs_str:
        print("Syntax Error: One side of the equation is empty.")
        return
    
    # Définition du motif (Pattern)
    pattern = r"([-+]?\d*\.?\d+)\*X\^(\d+)"

    try:
        lhs_terms = parse_terms(lhs_str)
        rhs_terms = parse_terms(rhs_str)
    except Exception as e:
        print(f"Syntax Error: {e}")
        return

    #print(f"left terms : {lhs_terms}")
    #print(f"rigth terms : {rhs_terms}")


    # ----------REDUCTION----------

    # Dictionnaire { degré (int) : coef (float) }
    polynomial = {}

    def add_term(coef, exposant, signe_global=1):
        degree = int(exposant)
        valeur = float(coef) * signe_global
        
        if degree in polynomial:
            polynomial[degree] += valeur
        else:
            polynomial[degree] = valeur

    for coef, exposant in lhs_terms:
        add_term(coef, exposant, 1)

    for coef, exposant in rhs_terms:
        add_term(coef, exposant, -1)

    sorted_degrees = sorted(polynomial.keys())
    parts = []
    
    for degree in sorted_degrees:
        coef = polynomial[degree]
        if coef == 0:
            continue
            
        if coef < 0:
            sign = "- "
            val = -coef
        else:
            sign = "+ "
            val = coef
            
        if len(parts) == 0:
            if sign == "+ ":
                sign = ""
            else:
                sign = "- "
        
        if int(val) == val:
             parts.append(f"{sign}{int(val)} * X^{degree}")
        else:
             parts.append(f"{sign}{val} * X^{degree}")

    if not parts:
        reduced_form = "0 = 0"
    else:
        reduced_form = " ".join(parts) + " = 0"

    print(f"Reduced form: {reduced_form}")
    
    # ----------CALCUL DU DEGRÉ----------
    
    degree = 0
    for d in polynomial:
        if polynomial[d] != 0:
            if d > degree:
                degree = d

    print(f"Polynomial degree: {degree}")

    if degree > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        return
    try:
        solve(polynomial, degree)
    except OverflowError:
        print("Math Error: The numbers are too big to be calculated.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
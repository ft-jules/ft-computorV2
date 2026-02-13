import sys
import re


def _ft_sqrt(nombre):
    return nombre ** 0.5


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
    a = polynomial.get(2, 0)
    b = polynomial.get(1, 0)
    c = polynomial.get(0, 0)
    # ax^2+bx+c

    # 4 * X^0 = 0 ou 2 * X^0 = 2 * X^0
    if degree == 0:
        if c == 0:
            print("Every real number is a solution.")
        else:
            print("No solution.")

    # 2 * X^1 + 4 * X^0 = 0 -> X = -c / b
    elif degree == 1:
        res = -c / b
        print(f"The solution is:\n{res}")

    # 3 * X^2 + 2 * X^1 + 4 * X^0 = 0
    elif degree == 2:
        delta = (b * b) - (4 * a * c)

        if delta > 0:
            print("Discriminant is strictly positive, the two solutions are:")
            sqrt_delta = ft_sqrt(delta)
            #sqrt_delta = _ft_sqrt(delta)

            # (-b ± √Δ) / 2a
            sol1 = (-b - sqrt_delta) / (2 * a)
            sol2 = (-b + sqrt_delta) / (2 * a)

            print(f"{sol1}\n{sol2}")

        elif delta == 0:
            print("Discriminant is zero, the solution is:")
            # -b / 2a
            sol = -b / (2 * a)
            print(f"{sol}")

        else: # delta < 0
            print("Discriminant is strictly negative, the two complex solutions are:")
            sqrt_delta = ft_sqrt(-delta)
            #sqrt_delta = _ft_sqrt(-delta)
            reel = -b / (2 * a)
            imag = sqrt_delta / (2 * a)

            # "X + i * Y"
            print(f"{reel} - i * {abs(imag)}")
            print(f"{reel} + i * {abs(imag)}")
def main():

    # ----------PARSING----------

    if len(sys.argv) != 2:
        print("Usage: python3 computor.py \"5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0\"")
        return

    equation = sys.argv[1].replace(" ", "")
    
    if equation.count('=') != 1:
        print("Syntax Error: The equation must contain exactly one '=' sign.")
        return

    lhs, rhs = equation.split('=')

    if not lhs.strip() or not rhs.strip():
        print("Syntax Error: One side of the equation is empty.")
        return
    
    # Définition du motif (Pattern)
    # 1. ([-+]?\d*\.?\d+) : Capture le nombre (entier ou décimal, positif ou négatif)
    # 2. \*X\^            : Cherche littéralement "*X^"
    # 3. (\d+)            : Capture l'exposant (un nombre entier)
    pattern = r"([-+]?\d*\.?\d+)\*X\^(\d+)"

    lhs_terms = re.findall(pattern, lhs)
    rhs_terms = re.findall(pattern, rhs)

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

    print(f"Reducted form: {polynomial}")
    

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
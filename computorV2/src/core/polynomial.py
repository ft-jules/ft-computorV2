"""
Gestion des polynômes (réutilisation améliorée de V1).
"""
from .complex import Complex
from .rational import Rational
from src.utils.errors import MathError

class Polynomial:
    def __init__(self, coeffs=None, var_name='X'):
        self.var_name = var_name
        self.coeffs = {}
        if coeffs:
            for deg, val in coeffs.items():
                if isinstance(val, (int, float)):
                    val = Complex(val)
                if isinstance(val, Rational):
                    val = Complex(val)
                if val != Complex(0):
                    self.coeffs[deg] = val
        self._clean()

    def __repr__(self):
        if not self.coeffs:
            return "0"
        parts = []
        for deg in sorted(self.coeffs.keys(), reverse=True):
            val = self.coeffs[deg]
            val_str = str(val)
            sign_prefix = " + "
            if not parts:
                sign_prefix = ""
            coeff_str = val_str
            if deg > 0:
                if val_str == "1": coeff_str = ""
                elif val_str == "-1": coeff_str = "-"
            term_str = ""
            if deg == 0:
                term_str = f"{val_str}"
                if parts: sign_prefix = " + "
            elif deg == 1:
                term_str = f"{coeff_str}{self.var_name}"
            else:
                term_str = f"{coeff_str}{self.var_name}^{deg}"
            full_part = f"{sign_prefix}{term_str}"
            parts.append(full_part)
        result = "".join(parts)
        return result.replace(" + -", " - ")
        
    def _clean(self):
        keys_to_delete = [k for k, v in self.coeffs.items() if v == Complex(0)]
        for k in keys_to_delete:
            del self.coeffs[k]

    def __add__(self, other):
        new_coeffs = self.coeffs.copy()
        if isinstance(other, (int, float, Rational, Complex)):
            other = Polynomial({0: other})
        if isinstance(other, Polynomial):
            for deg, val in other.coeffs.items():
                new_coeffs[deg] = new_coeffs.get(deg, Complex(0)) + val
        else:
            return NotImplemented

        res = Polynomial(new_coeffs)
        res._clean()
        return res

    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        new_coeffs = self.coeffs.copy()

        if isinstance(other, (int, float, Rational, Complex)):
            other = Polynomial({0: other})

        if isinstance(other, Polynomial):
            for deg, val in other.coeffs.items():
                current = new_coeffs.get(deg, Complex(0))
                res = current - val
                new_coeffs[deg] = res
        else:
            return NotImplemented
        res = Polynomial(new_coeffs)
        res._clean()
        return res

    def __rsub__(self, other):
        if isinstance(other, (int, float, Rational, Complex)):
            other_poly = Polynomial({0: other})
            return other_poly - self
        return NotImplemented

    def __mul__(self, other):
        new_coeffs = {}

        if isinstance(other, (int, float, Rational, Complex)):
            other = Polynomial({0: other})

        if isinstance(other, Polynomial):
            for d1, c1 in self.coeffs.items():
                for d2, c2 in other.coeffs.items():
                    new_deg = d1 + d2
                    new_val = c1 * c2
                    current = new_coeffs.get(new_deg, Complex(0))
                    new_coeffs[new_deg] = current + new_val
        else:
            return NotImplemented
        res = Polynomial(new_coeffs)
        res._clean()
        return res

    def __rmul__(self, other):
        return self * other

    def __pow__(self, power):
        from .rational import Rational
        if isinstance(power, Rational):
            if power.denominator != 1:
                raise MathError("Polynomial power must be an integer")
            power = power.numerator
        if not isinstance(power, int):
            raise MathError("Polynomial power must be an integer")
        if power < 0:
            raise MathError("Cannot raise polynomial to negative power")
        if power == 0:
            return Polynomial({0: 1})
        res = Polynomial({0: 1})
        for _ in range(power):
            res = res * self
        return res


    def solve(self, unknown_name='X'):
        self.var_name = unknown_name
        print(f"Reduced form: {self} = 0")
        degree = max(self.coeffs.keys()) if self.coeffs else 0
        print(f"Polynomial degree: {degree}")
        if degree > 2:
            print("The polynomial degree is strictly greater than 2, i can't solve.")
            return
        
        a = self.coeffs.get(2, Complex(0))
        b = self.coeffs.get(1, Complex(0))
        c = self.coeffs.get(0, Complex(0))

        if degree == 2:
            self._solve_quadratic(a, b, c)
        elif degree == 1:
            print("The solution is:")
            res = (Complex(-1) * c) / b
            print(res)
        else:
            if c == Complex(0):
                print("Every real number is a solution")
            else:
                print("No solution")

    def _solve_quadratic(self, a , b, c):
        delta = (b * b) - (Complex(4) * a * c)
        root_delta = delta.sqrt()
        print(f"Discriminant (Delta): {delta}")
        if delta == Complex(0):
            print("Discriminant is 0, the solution is:")
            res = (Complex(-1) * b) / (Complex(2) * a)
            print(res)
        elif delta.imaginary.numerator == 0 and delta.real.numerator > 0:
            print("Discriminant is strictly positive, the two solutions are:")
            sol1 = ((Complex(-1) * b) - root_delta) / (Complex(2) * a)
            sol2 = ((Complex(-1) * b) + root_delta) / (Complex(2) * a)
            print(sol1)
            print(sol2)
        else:
            print("Discriminant is not null, there are two solutions:")
            sol1 = ((Complex(-1) * b) - root_delta) / (Complex(2) * a)
            sol2 = ((Complex(-1) * b) + root_delta) / (Complex(2) * a)
            print(sol1)
            print(sol2)

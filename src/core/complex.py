"""
Classe Complex : Gère les nombres complexes (partie réelle + imaginaire).
"""
from .rational import Rational
from src.utils.errors import MathError

class Complex:
    def __init__(self, real, imaginary=0):
        if not isinstance(real, Rational):
            real = Rational(real)
        if not isinstance(imaginary, Rational):
            imaginary = Rational(imaginary)
        self.real = real
        self.imaginary = imaginary

    def __repr__(self):
        if self.imaginary.numerator == 0:
            return f"{self.real}"
        if self.real.numerator == 0:
            if self.imaginary.numerator == 1 and self.imaginary.denominator == 1:
                return "i"
            if self.imaginary.numerator == -1 and self.imaginary.denominator == 1:
                return "-i"
            return f"{self.imaginary}i"
        
        sign = "+"
        im_val = self.imaginary

        if self.imaginary.numerator < 0:
            sign = "-"
            im_val = Rational(abs(self.imaginary.numerator), self.imaginary.denominator)
        
        im_str = f"{im_val}i"
        if im_val.numerator == 1 and im_val.denominator == 1:
            im_str = "i"
        return f"{self.real} {sign} {im_str}"

    def __eq__(self, other):
        if isinstance(other, (int, float, Rational)):
            other = Complex(other)
        if not isinstance(other, Complex):
            return False
        return self.real == other.real and self.imaginary == other.imaginary

# -------------------OPERATIONS ARITHMETIQUES------------------- #

    def __add__(self, other):
        if not isinstance(other, (int, float, Rational, Complex)):
            return NotImplemented
        if not isinstance(other, Complex):
            other = Complex(other)
        return Complex(self.real + other.real, self.imaginary + other.imaginary)

    def __sub__(self, other):
        if not isinstance(other, (int, float, Rational, Complex)):
            return NotImplemented
        if not isinstance(other, Complex):
            other = Complex(other)
        return Complex(self.real - other.real, self.imaginary - other.imaginary)

    def __mul__(self, other):
        if not isinstance(other, (int, float, Rational, Complex)):
            return NotImplemented
        if not isinstance(other, Complex):
            other = Complex(other)
        real_part = (self.real * other.real) - (self.imaginary * other.imaginary)
        imag_part = (self.real * other.imaginary) + (self.imaginary * other.real)
        return Complex(real_part, imag_part)

    def __truediv__(self, other):
        if not isinstance(other, (int, float, Rational, Complex)):
            return NotImplemented
        if not isinstance(other, Complex):
            other = Complex(other)
        if other.real.numerator == 0 and other.imaginary.numerator == 0:
            raise MathError("Division by zero")
        denominator = (other.real * other.real) + (other.imaginary * other.imaginary)
        num_real = (self.real * other.real) + (self.imaginary * other.imaginary)
        num_imag = (self.imaginary * other.real) - (self.real * other.imaginary) # '-' a cause du conjuge
        return Complex(num_real / denominator, num_imag / denominator)

    def __pow__(self, power):
        from .rational import Rational
        if isinstance(power, Rational):
            if power.denominator == 1:
                power = power.numerator
            else:
                raise MathError("Exponent must be an integer for Complex numbers")
        if not isinstance(power, int):
            raise MathError("Exponent must be an integer for Complex numbers")
        if power == 0:
            return Complex(1)
        if power < 0:
            return Complex(1) / (self ** -power)

        result = Complex(1)
        base = self
        for _ in range(power):
            result = result * base
        return result

    def __radd__(self, other):
        return self + other

    def __rmul__(self, other):
        return self * other

    def __rsub__(self, other):
        return Complex(other) - self

    def __rtruediv__(self, other):
        return Complex(other) / self

    def sqrt(self):
        if self.imaginary.numerator == 0 and self.real.numerator >= 0:
            val = self.real.numerator / self.real.denominator
            root = val ** 0.5
            return Complex(root, 0)
        if self.imaginary.numerator == 0 and self.real.numerator < 0:
            val = abs(self.real.numerator / self.real.denominator)
            root = val ** 0.5
            return Complex(0, root)
        c_val = complex(self.real.numerator/self.real.denominator, 
                        self.imaginary.numerator/self.imaginary.denominator)
        res = c_val ** 0.5
        return Complex(res.real, res.imag)
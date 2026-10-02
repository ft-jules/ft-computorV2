"""
Classe Matrix : Gère les opérations matricielles.
"""
from .complex import Complex
from src.utils.errors import MathError

class Matrix:
    def __init__(self, data):
        if not isinstance(data, list) or not data:
            raise MathError("Matrix cannot be empty")
        self.rows = len(data)
        self.cols = len(data[0])

        self.data = []

        for row in data:
            if not isinstance(row, list):
                raise MathError("Matrix must be a list of lists")
            if len(row) != self.cols:
                raise MathError("Matrix must be rectangular (all rows must have same lenght)")
            new_row = []
            for item in row:
                if not isinstance(item, Complex):
                    item = Complex(item)
                new_row.append(item)
            self.data.append(new_row)

    def __repr__(self):
        row_str = []
        for row in self.data:
            row_content = [str(x) for x in row]
            row_str.append(f"[{', '.join(row_content)}]")
        return f"[{'; '.join(row_str)}]"

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        if self.rows != other.rows or self.cols != other.cols:
            return False
        for i in range(self.rows):
            for j in range(self.cols):
                if self.data[i][j] != other.data[i][j]:
                    return False
        return True

    # -------------------OPERATIONS MATRICIELLES------------------- #

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise MathError("Cannot add matrix and Scalar")
        if self.rows != other.rows or self.cols != other.cols:
            raise MathError(f"Dimension mismatch for addition: ({self.rows},{self.cols}) vs ({other.rows},{other.cols})")
        
        new_data = []
        for i in range(self.rows):
            new_row = []
            for j in range(self.cols):
                new_row.append(self.data[i][j] + other.data[i][j])
            new_data.append(new_row)

        return Matrix(new_data)

    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise MathError("Cannot substract Matrix and Scalar")
        if self.rows != other.rows or self.cols != other.cols:
            raise MathError(f"Dimension mismatch for substraction: ({self.rows},{self.cols}) vs ({other.rows},{other.cols})")

        new_data = []
        for i in range(self.rows):
            new_row = []
            for j in range(self.cols):
                new_row.append(self.data[i][j] - other.data[i][j])
            new_data.append(new_row)

        return Matrix(new_data)

    def __mul__(self, other): # Matrix * scalar & Matrix * Matrix
        from .rational import Rational
        if isinstance(other, (int, float, Complex, Rational)):
            scalar = other if isinstance(other, (Complex, Rational)) else Complex(other)
            new_data = []
            for i in range(self.rows):
                new_row = []
                for j in range(self.cols):
                    new_row.append(self.data[i][j] * scalar)
                new_data.append(new_row)
            return Matrix(new_data)

        if isinstance(other, Matrix):
            if self.cols != other.rows:
                raise MathError(f"Diemsion mismatch for multiplication: ({self.rows},{self.cols}) vs ({other.rows},{other.cols}). Cols A must equal Rows B.")
            result_data = []
            for i in range(self.rows):
                new_row = []
                for j in range(other.cols):
                    sum_val = Complex(0)
                    for k in range(self.cols):
                        sum_val = sum_val + (self.data[i][k] * other.data[k][j])
                    new_row.append(sum_val)
                result_data.append(new_row)
            return Matrix(result_data)
        raise MathError("Unsupported operation for Matrix multiplication")  

    def __rmul__(self, other): # gere le cas nombre * matrice
        return self.__mul__(other)
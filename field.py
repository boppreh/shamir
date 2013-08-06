class FieldValue(long):
    """
    Class for operating on finite fields with overloaded operators.
    The field modulus e replicated on each field value.
    """
    def __new__(cls, value, mod):
        return long.__new__(cls, long(value % mod))

    def __init__(self, value, mod):
        self.mod = mod
        long.__init__(long(value))

    def __add__(self, other):
        return FieldValue(long.__add__(self, long(other)), self.mod)

    def __radd__(self, other):
        return FieldValue(long.__add__(self, long(other)), self.mod)

    def __sub__(self, other):
        result = long.__sub__(self, long(other))
        while result < 0:
            result += self.mod
        return FieldValue(result, self.mod)

    def __rsub__(self, other):
        result = long.__sub__(long(other), self)
        while result < 0:
            result += self.mod
        return FieldValue(result, self.mod)

    def __mul__(self, other):
        return FieldValue(long(self) * long(other % self.mod), self.mod)

    def __rmul__(self, other):
        return FieldValue(long(other % self.mod) * long(self), self.mod)

    def __div__(self, other):
        return self * FieldValue(other, self.mod).inverse()

    def __rdiv__(self, other):
        return other * self.inverse()

    def __pow__(self, other):
        return FieldValue(pow(long(self), long(other), self.mod), self.mod)

    def __eq__(self, other):
        return long(self) == long(other) % self.mod

    def inverse(self):
        """
        Returns the multiplicative inverse such that `a.inverse() * a == 1`.
        The modulus must be a prime for this to work.
        """
        return self.gcd(self.mod)[0]

    def gcd(self, other):
        a, b = self, other
        x, y = 0, 1
        lastx, lasty = 1, 0
        while b:
            quotient = a // b
            a, b = b, a % b
            x, lastx = lastx - quotient * x, x
            y, lasty = lasty - quotient * y, y

        return lastx, lasty

    def __str__(self):
        return '{}(%{})'.format(int(self), self.mod)


from itertools import izip_longest
class Polynomial(object):
    """
    Class for handling polynomials with overloaded operators.
    """
    def __init__(self, coefs=()):
        """
        Creates a new polynomial with the given coefficients.
        The coefficients are given in a list in big endian form, starting with
        the constant term.
        """
        coefs = list(coefs)
        while coefs and coefs[-1] == 0:
            coefs.pop()

        self.coefs = coefs
        self.degree = len(self.coefs)

    def __add__(self, other):
        return Polynomial(c1 + c2 for c1, c2 in self._wrap_zip(other))

    def __radd__(self, other):
        return Polynomial(c2 + c1 for c1, c2 in self._wrap_zip(other))

    def __sub__(self, other):
        return Polynomial(c1 - c2 for c1, c2 in self._wrap_zip(other))

    def __rsub__(self, other):
        return Polynomial(c2 - c1 for c1, c2 in self._wrap_zip(other))

    def __mul__(self, other):
        other = other.coefs if isinstance(other, Polynomial) else [other]
        coefs = [0] * (len(self.coefs) + len(other))
        for i, c1 in enumerate(self.coefs):
            for j, c2 in enumerate(other):
                coefs[i + j] += c1 * c2

        return Polynomial(coefs)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        if isinstance(other, Polynomial):
            raise NotImplemented('Division of Polynomial by Polynomial is not yet implemented.')
        return Polynomial(c1 / other for c1 in self.coefs)

    def __call__(self, x):
        """
        Evaluates the Polynomial at `x`.
        """
        power = 1
        total = 0
        for coef in self.coefs:
            total += power * coef
            power *= x

        return total

    def __str__(self):
        """
        Prints the polynomial in the format 10x^0 + 5x^1 + 2x^2 + ...
        """
        return ' + '.join('{}x^{}'.format(coef, power) for power, coef in enumerate(self.coefs))

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return self.coefs == other.coefs
        else:
            return self.coefs == other

    def _wrap_zip(self, value):
        """
        Wraps the value in a polynomial with same degree.
        """
        if isinstance(value, Polynomial):
            return izip_longest(self.coefs, value.coefs, fillvalue=0)
        else:
            return izip_longest(self.coefs, [value], fillvalue=0)

if __name__ == '__main__':
    two = FieldValue(2, 23)
    print(two * two.inverse())
    p = Polynomial([two, two, two])
    print(p(FieldValue(200000000000, 1023)))
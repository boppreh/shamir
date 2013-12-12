from __future__ import division
import unittest

from field import *
from shamir import *

mod = 997

class TestField(unittest.TestCase):
    def test_field_value(self):
        x = FieldValue(1, mod)
        y = FieldValue(2, mod)
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(x + y, 3)
        self.assertEqual(x + x, y)
        self.assertEqual(y - x, x)
        self.assertEqual(x * x, x)
        self.assertEqual(x * y, y)
        self.assertEqual(y * 2, 4)
        self.assertEqual(y / 2, x)
        self.assertEqual(2 / y, x)

        self.assertNotEqual(x, y)

    def test_polynomial(self):
        p = Polynomial([1, 2, 3])
        q = Polynomial([4, 5, 6])
        self.assertEqual(p, [1, 2, 3])
        self.assertEqual(p + 1, [2, 2, 3])
        self.assertEqual(p * 2, [2, 4, 6])
        self.assertEqual(p / 2, [.5, 1, 1.5])
        self.assertEqual(p + q, [5, 7, 9])
        self.assertEqual(q - p, [3, 3, 3])
        self.assertEqual(p * q, [4, 13, 28, 27, 18])

        self.assertEqual(p(0), 1)
        self.assertEqual(p(1), 6)
        self.assertEqual(p(2), 17)

        self.assertNotEqual(p, q)

    def test_field_poly(self):
        x = FieldValue(1, mod)
        y = FieldValue(2, mod)
        z = FieldValue(3, mod)
        p = Polynomial([x, y, z])

        self.assertEqual(p, [1, 2, 3])
        self.assertEqual(p + 1, [2, 2, 3])
        self.assertEqual(p - 3, [mod - 2, 2, 3])
        self.assertEqual(p * 2, [2, 4, 6])

        self.assertEqual(p(0), 1)
        self.assertEqual(p(1), 6)
        self.assertEqual(p(2), 17)
        self.assertEqual(p(1000), FieldValue(34, mod))

if __name__ == '__main__':
    unittest.main()

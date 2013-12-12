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
        self.assertEqual(p.degree, 3)
        self.assertEqual(p, [1, 2, 3])
        self.assertEqual(p + 1, [2, 2, 3])
        self.assertEqual(p * 2, [2, 4, 6])
        self.assertEqual(p / 2, [.5, 1, 1.5])
        self.assertEqual(p + q, [5, 7, 9])
        self.assertEqual(q - p, [3, 3, 3])
        self.assertEqual(p * q, [4, 13, 28, 27, 18])
        self.assertEqual((p * q).degree, 5)

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

class TestShamir(unittest.TestCase):
    def setUp(self):
        self.secret = 42
        s = [(1, 519), (2, 158), (3, 953), (4, 910), (5, 29)]
        self.shares = [(FieldValue(x, mod), FieldValue(y, mod)) for x, y in s]

    def test_basic(self):
        self.assertEqual(len(self.shares), 5)
        self.assertTrue(all(len(point) == 2 for point in self.shares))
        self.assertTrue(all(isinstance(point[1], FieldValue) for point in self.shares))

        self.assertEqual(join(self.shares), self.secret)
        self.assertEqual(join(self.shares[:4]), self.secret)
        self.assertEqual(join(self.shares[:3]), self.secret)
        self.assertNotEqual(join(self.shares[:2]), self.secret)
        self.assertNotEqual(join(self.shares[:1]), self.secret)

    def test_poly(self):
        self.assertEqual(reconstruct_poly(self.shares)(0), self.secret)
        self.assertEqual(reconstruct_poly(self.shares).degree, 3)
        self.assertEqual(reconstruct_poly(self.shares[:4]).degree, 3)
        self.assertEqual(reconstruct_poly(self.shares[:3]).degree, 3)

    def test_change_points(self):
        shares_delta = change_points(self.shares)
        new_shares = [(i[0], i[1] + j[1]) for i, j in
                      zip(self.shares, shares_delta)]

        self.assertEqual(join(new_shares), self.secret)

    def test_get_threshold(self):
        self.assertEqual(get_threshold(self.shares), 3)

        for i in range(0, mod, 200):
            self.assertEqual(get_threshold(self.shares), 3)
            self.assertEqual(get_threshold(self.shares[:-1]), 3)
            self.assertEqual(get_threshold(self.shares[:-2]), 3)
            self.assertEqual(get_threshold(self.shares[:-3]), 2)

            self.assertEqual(get_last_coefficient(self.shares), 0)
            self.assertEqual(get_last_coefficient(self.shares[:-1]), 0)
            self.assertNotEqual(get_last_coefficient(self.shares[:-2]), 0)
            self.assertNotEqual(get_last_coefficient(self.shares[:-3]), 0)

    def test_has_liars(self):
        self.assertFalse(has_liars(self.shares))
        self.assertFalse(has_liars(self.shares[:4]))
        self.assertTrue(has_liars(self.shares[:3]))
        self.assertTrue(has_liars(self.shares + [(6, 10)]))
        self.assertTrue(has_liars([(6, 10)] + self.shares))

    def test_get_honest(self):
        honest = set(self.shares)
        self.assertEqual(get_honest(self.shares), honest)
        fake1 = (6, 100)
        fake2 = (7, 150)
        self.assertEqual(get_honest(self.shares + [fake1]), honest)
        self.assertEqual(get_honest(self.shares + [fake1, fake2]), honest)
        self.assertEqual(get_honest([fake1] + self.shares + [fake2]), honest)


if __name__ == '__main__':
    unittest.main()



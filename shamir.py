from __future__ import division
import random
from itertools import combinations
from field import FieldValue, Polynomial

mod = 997

def split(secret, parts, threshold):
    """
    Splits a secret integer into a number of points, where at least
    `threshold` points are required to reconstruct the secret.
    """
    poly = make_random_poly(secret, threshold)
    return [(i + 1, poly(i + 1)) for i in range(parts)]

def join(points):
    """
    Joins a number of points above the threshold to reconstruct the original
    secret.
    """
    result = FieldValue(0, mod)

    for x1, y1 in points:
        top = 1
        bottom = 1
        for x2, y2 in points:
            if x1 != x2:
                top *= FieldValue(-x2, mod)
                bottom *= (x1 - x2)
                
        result += y1 * top / bottom

    return result

def make_random_poly(constant, degree):
    """
    Makes a polynomial with random coefficients, with a fixed constant value,
    thus always evaluating to `constant` at x=0.
    """
    coefficients = [FieldValue(random.randrange(mod), mod) for i in range(degree - 1)]
    return Polynomial([FieldValue(constant, mod)] + coefficients)

def reconstruct_poly(points):
    """
    Reconstructs the polynomial from a list of points.
    """
    result_poly = Polynomial()

    for x1, y1 in points:
        top = 1
        bottom = 1
        for x2, y2 in points:
            if x1 != x2:
                top *= Polynomial([-x2, 1])
                bottom *= (x1 - x2)
        result_poly += Polynomial([y1]) * top / bottom

    return result_poly

def get_threshold(points):
    """
    Returns the degree of the polynomial of a list of points.
    """
    # Starts trying with all points, assuming the threshold
    # is nearer len(points) than 0.
    for i in range(len(points), 1, -1):
        if get_last_coefficient(points[:i]) != 0:
            return i

    return len(points)

def get_last_coefficient(points):
    """
    Computes the last coefficient of the Lagrange Polynomial over the given
    points.
    """
    total = 0
    for x1, y1 in points:
        partial = 1
        for x2, y2 in points:
            if x1 != x2:
                partial *= (x1 - x2)
                
        total += y1 / partial
    
    return total

def change_points(points):
    """
    Given a list of points, creates a new polynomial that passes through the
    same secret but has different coefficients. Returns (x, delta y) of the
    points given.
    """
    secret = join(points)
    poly = make_random_poly(secret, len(points))
    for x, y in points:
        yield (x, poly(x) - y)

def has_liars(points):
    """
    Detects if one or more points are fake. The number of points must be N + 1
    above the threshold, where N is the maximum number of fake points able to
    be detected.
    """
    return get_threshold(points) == len(points)

def get_honest(points):
    """
    Detects and returns a list of honest points from `points`.
    """
    honest = set()

    for n_honest in range(0, len(points)):
        for combination in combinations(points, n_honest):
            if not has_liars(combination):
                honest.update(combination)

    return honest

n_polys = 0
n_collisions = 0

def a(points):
    for j in range(3, 9):
        for combination in combinations(points, j):
            threshold = get_threshold(combination)
            if threshold != j:
                rec_poly = reconstruct_poly(combination)
                if rec_poly != poly:
                    global n_collisions
                    n_collisions += 1
                    return



if __name__ == '__main__':
    from random import randint
    for i in range(1000):
        coefs = [FieldValue(randint(1, mod), mod) for i in range(6)]
        poly = Polynomial(coefs)
        n_polys += 1
        points = poly.points(*range(1, 9))
        a(points)

    print(100 * n_collisions / n_polys, "%")

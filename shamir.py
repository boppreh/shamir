import random
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
	result_poly = Polynomial()

	for x1, y1 in points:
		top = 1
		bottom = 1
		for x2, y2 in points:
			if x1 != x2:
				top *= FieldValue(-x2, mod)
				bottom *= (x1 - x2)
				
		result_poly += y1 * top / bottom

	return result_poly

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
	return reconstruct_poly(points).degree

if __name__ == '__main__':
	secret = 42
	n_parts = 200
	threshold = 200

	print 'Splitting secret {} in {} parts with threshold {}.'.format(secret, n_parts, threshold)

	shares = split(secret, n_parts, threshold)
	print 'Shares:', shares
	#print 'Detected threshold:', get_threshold(shares)

	import cProfile
	#cProfile.run('join(shares[:threshold])', sort=1)
	cProfile.run('reconstruct_poly(shares[:threshold])', sort=1)
	#print 'Reconstructed secret:', join(shares[:threshold])
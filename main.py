# Write a computer program to compute the key for the Shamir (t, w)-
# Threshold Scheme implemented in Zp. That is, given t public x-coordinates,
# x1, x2, . . . , xt
# , and t y-coordinates y1, . . . , yt
# , compute the resulting key using
# the Lagrange interpolation formula.
# (a) Test your program if p = 31847, t = 5, and w = 10, with the following
# shares:
# x1 = 413 y1 = 25439
# x2 = 432 y2 = 14847
# x3 = 451 y3 = 24780
# x4 = 470 y4 = 5910
# x5 = 489 y5 = 12734
# x6 = 508 y1 = 12492
# x7 = 527 y2 = 12555
# x8 = 546 y3 = 28578
# x9 = 565 y4 = 20806
# x10 = 584 y5 = 21462
# Verify that the same key is computed by using several different subsets
# of five shares.
# (b) Having determined the key, compute the share that would be given to
# a participant with x-coordinate equal to 10000. (Note that this can be
# done without computing the whole secret polynomial a(x).)

import random

# Function to evaluate the polynomial at a given x
def evaluate_polynomial(coefficients, x, p):
    result = 0
    power = 1
    for coefficient in coefficients:
        result = (result + coefficient * power) % p
        power = (power * x) % p
    return result

def generate_share(x, p, coefficients):
    return (x, evaluate_polynomial(coefficients, x, p))

def generate_lagrange_coefficients(shares, i, p):
    numerator = 1
    demoninator = 1
    xi, _ = shares[i]

    for j in range(len(shares)):
        xj, _  = shares[j]
        if i != j:
            """"
            General formula is: Product from j = 1; j <= t; j++; j != i
            bj *= (xj/(xj - xi)) mod p OR bj *= (numerator mod p)/(demo mod p)
            numerator *= -xj mod p (the -xj is the numerator of the lagrange coefficient)
            demoninator *= (xj - xi) mod p
            """
            numerator = (numerator * -xj) % p
            demoninator = (demoninator * (xj - xi)) % p
    # We multiply the numerator by the inverse of the demoninator to avoid division
    return  (numerator * pow(demoninator, -1, p)) % p

def compute_key_from_shares_shamir(shares, p = 31847, t = 5, w = 10):
    t_sample = random.sample(shares, t)
    print("t_sample: ", t_sample)
    key = 0
    for i in range(len(t_sample)):
        _, yi = t_sample[i]
        # The key will be y1 * (b1 mod p) + y2 * (b2 mod p) + ... + yt * (bt mod p)
        key += (yi * (generate_lagrange_coefficients(t_sample, i, p) % p))
    return key % p, t_sample

def generate_coefficients(key, samples):
    coefficients = [key]
    for i in range(len(samples)):
        coefficients.append(generate_lagrange_coefficients(samples, i, p))
    return coefficients

p = 31847; t = 5; w = 10

print("Letter A: Verify that the same key is computed by using several different subsets of five shares.")
shares = [(413, 25439), (432, 14847), (451, 24780), (470, 5910), (489, 12734), (508, 12492), (527, 12555), (546, 28578), (565, 20806), (584, 21462)]
key, t_sample = compute_key_from_shares_shamir(shares, p, t, w)
print("key: ", key)

print("Letter B: Having determined the key, compute the share that would be given to a participant with x-coordinate equal to 10000.")
# Using the same coefficients as the previous exercise
coefficients = generate_coefficients(key, t_sample)
share = generate_share(10000, p, coefficients)
print("share: ", share)
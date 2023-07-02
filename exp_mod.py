import sys

def modular_exp(base, exp, mod):
    if exp == 0:
        return 1
    elif exp % 2 == 0:
        return modular_exp(base, exp/2, mod)**2 % mod
    else:
        return base * modular_exp(base, exp-1, mod) % mod

# Path: exp_mod.py
if __name__ == '__main__':
    base = int(sys.argv[1])
    exp = int(sys.argv[2])
    mod = int(sys.argv[3])
    print(modular_exp(base, exp, mod))
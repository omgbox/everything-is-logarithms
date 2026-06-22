"""p-adic valuations as projections in logarithmic space."""

import numpy as np
from math import isqrt
from typing import Dict, List


def prime_factorization(n: int) -> Dict[int, int]:
    """Factor n into primes."""
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def nu_p(n: int, p: int) -> int:
    """p-adic valuation: exponent of p in factorization of n."""
    if n == 0:
        return float('inf')
    count = 0
    while n % p == 0:
        count += 1
        n //= p
    return count


class PProjection:
    """
    The p-projection functor: extracts the p-component in log-space.
    
    This is a natural transformation from the identity functor
    to the p-projection functor.
    """
    
    def __init__(self, p: int):
        self.p = p
    
    def __call__(self, n: int) -> int:
        """Project n onto its p-component."""
        return nu_p(n, self.p)
    
    def log_contribution(self, n: int) -> float:
        """The contribution of p to log(n)."""
        return nu_p(n, self.p) * np.log(self.p)
    
    def reconstruct(self, exponents: Dict[int, int]) -> int:
        """Reconstruct n from its p-adic projections."""
        n = 1
        for p, e in exponents.items():
            n *= p ** e
        return n


class LogarithmicBasis:
    """
    The set {log(p) : p prime} forms a basis for the logarithmic space
    of positive rationals.
    """
    
    def __init__(self, max_prime: int = 100):
        self.primes = self._sieve(max_prime)
        self.log_primes = {p: np.log(p) for p in self.primes}
    
    @staticmethod
    def _sieve(n: int) -> List[int]:
        """Sieve of Eratosthenes."""
        is_prime = [True] * (n + 1)
        is_prime[0] = is_prime[1] = False
        for i in range(2, isqrt(n) + 1):
            if is_prime[i]:
                for j in range(i * i, n + 1, i):
                    is_prime[j] = False
        return [i for i in range(2, n + 1) if is_prime[i]]
    
    def decompose(self, n: int) -> Dict[int, int]:
        """Decompose log(n) in the logarithmic basis."""
        return prime_factorization(n)
    
    def reconstruct_log(self, coeffs: Dict[int, int]) -> float:
        """Reconstruct log(n) from coefficients."""
        return sum(e * self.log_primes[p] for p, e in coeffs.items() if p in self.log_primes)

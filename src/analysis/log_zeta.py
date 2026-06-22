"""Logarithmic zeta function."""

import numpy as np
from ..core.padic_projections import LogarithmicBasis


class LogZeta:
    """
    The zeta function as a generating function over logarithmic invariants.
    
    zeta(s) = sum_{n>=1} n^{-s} = prod_p (1-p^{-s})^{-1}
    """
    
    def __init__(self, max_prime: int = 200):
        self.basis = LogarithmicBasis(max_prime)
    
    def zeta_direct(self, s: complex, N: int = 1000) -> complex:
        """Direct summation."""
        return sum(1.0 / (n ** s) for n in range(1, N + 1))
    
    def zeta_euler(self, s: complex, N_primes: int = 50) -> complex:
        """Euler product."""
        product = 1.0 + 0j
        for p in self.basis.primes[:N_primes]:
            product *= 1.0 / (1.0 - p ** (-s))
        return product
    
    def log_zeta_decomposition(self, s: complex, N: int = 100) -> dict:
        """
        Decompose zeta(s) into p-adic contributions.
        """
        contributions = {}
        for p in self.basis.primes[:N]:
            p_series = 1.0 / (1.0 - p ** (-s))
            contributions[p] = np.log(p_series) / np.log(p)
        return contributions

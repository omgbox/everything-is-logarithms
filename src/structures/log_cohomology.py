"""Logarithmic cohomology."""

import numpy as np
from typing import List, Dict, Tuple


class LogComplex:
    """
    A logarithmic cochain complex.
    
    Standard cochain complex: C^0 -> C^1 -> C^2 -> ...
    Log cochain complex: log(C^0) -> log(C^1) -> log(C^2) -> ...
    """
    
    def __init__(self, dimensions: List[int]):
        self.dimensions = dimensions
        self.n = len(dimensions)
        self.log_dimensions = [np.log(d) if d > 0 else 0 for d in dimensions]
    
    def euler_characteristic(self) -> float:
        """
        The Euler characteristic in log space:
        chi_log = SUM (-1)^n * log(dim(C^n))
        """
        return sum((-1)**n * self.log_dimensions[n] for n in range(self.n))
    
    def alternating_product(self) -> float:
        """The alternating product of dimensions."""
        return np.exp(self.euler_characteristic())


class LogCohomology:
    """
    Logarithmic cohomology: H^n_log(X) measures the multiplicative
    structure of X at scale n.
    """
    
    def __init__(self, complex: LogComplex):
        self.complex = complex
    
    def dimension(self, n: int) -> int:
        """Dimension of H^n_log."""
        if 0 <= n < self.complex.n:
            return self.complex.dimensions[n]
        return 0
    
    def log_dimension(self, n: int) -> float:
        """Logarithmic dimension of H^n_log."""
        d = self.dimension(n)
        return np.log(d) if d > 0 else 0
    
    def total_log_dimension(self) -> float:
        """SUM log(dim(H^n_log))."""
        return sum(self.log_dimension(n) for n in range(self.complex.n))
    
    def multiplicative_structure(self) -> Dict[Tuple[int, int], float]:
        """
        The multiplicative structure: how H^i x H^j -> H^{i+j}
        """
        structure = {}
        for i in range(self.complex.n):
            for j in range(self.complex.n - i):
                if i + j < self.complex.n:
                    log_dim_product = self.log_dimension(i) + self.log_dimension(j)
                    structure[(i, j)] = log_dim_product
        return structure

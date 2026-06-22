"""Finite fields and vector spaces."""

from math import isqrt
from typing import List


class GF:
    """Galois Field GF(p) for prime p."""
    
    def __init__(self, p: int):
        if not self._is_prime(p):
            raise ValueError(f"{p} is not prime")
        self.p = p
    
    @staticmethod
    def _is_prime(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, isqrt(n) + 1):
            if n % i == 0:
                return False
        return True
    
    def __repr__(self):
        return f"GF({self.p})"
    
    def __eq__(self, other):
        return isinstance(other, GF) and self.p == other.p
    
    def __hash__(self):
        return hash(("GF", self.p))
    
    @property
    def order(self) -> int:
        """|K| = number of elements in the field."""
        return self.p
    
    def elements(self) -> List[int]:
        """List all elements: {0, 1, ..., p-1}."""
        return list(range(self.p))
    
    def add(self, a: int, b: int) -> int:
        return (a + b) % self.p
    
    def mul(self, a: int, b: int) -> int:
        return (a * b) % self.p
    
    def inv(self, a: int) -> int:
        """Multiplicative inverse via Fermat's little theorem."""
        if a % self.p == 0:
            raise ZeroDivisionError
        return pow(a, self.p - 2, self.p)


class VectorSpace:
    """Vector space K^n over a finite field K = GF(p)."""
    
    def __init__(self, field: GF, n: int):
        self.field = field
        self.n = n
    
    def __repr__(self):
        return f"{self.field}^{self.n}"
    
    @property
    def dimension(self) -> int:
        """Standard dimension: n."""
        return self.n
    
    @property
    def cardinality(self) -> int:
        """|V| = |K|^n."""
        return self.field.order ** self.n
    
    def dim_as_log(self) -> float:
        """dim_K V = log_{|K|}(|V|)."""
        import numpy as np
        return np.log(self.cardinality) / np.log(self.field.order)

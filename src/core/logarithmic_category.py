"""The logarithmic category."""

from typing import Callable, List
from functools import reduce


class LogObject:
    """
    A log-object: (X, mu) where mu: X -> R>=0 is a size function.
    
    For finite sets, mu(X) = |X| (cardinality).
    """
    
    def __init__(self, elements: list, size_fn: Callable = None):
        self.elements = elements
        self.size_fn = size_fn or (lambda x: 1)
        self._size = None
    
    @property
    def size(self) -> float:
        if self._size is None:
            self._size = reduce(
                lambda a, b: a * b,
                [self.size_fn(x) for x in self.elements],
                1.0
            )
        return self._size
    
    def __repr__(self):
        return f"LogObj(size={self.size:.4f}, n_elements={len(self.elements)})"


class LogMorphism:
    """
    A log-morphism f: X -> Y preserving the logarithmic structure.
    """
    
    def __init__(self, source: 'LogObject', target: 'LogObject', map_fn: Callable):
        self.source = source
        self.target = target
        self.map_fn = map_fn
    
    def __call__(self, x):
        return self.map_fn(x)
    
    def is_log_preserving(self) -> bool:
        """Check if the morphism preserves logarithmic structure."""
        source_size = self.source.size
        image = set(self.map_fn(x) for x in self.source.elements)
        target_size = reduce(
            lambda a, b: a * b,
            [self.target.size_fn(y) for y in image],
            1.0
        )
        return target_size <= source_size + 1e-10

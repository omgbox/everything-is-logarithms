"""Information geometry as logarithmic invariant."""

import numpy as np
from typing import List


class LogEntropy:
    """
    Shannon entropy as a logarithmic invariant.
    
    H(X) = -SUM p(x) * log(p(x))
    """
    
    def __init__(self, probabilities: List[float]):
        self.p = np.array(probabilities)
        self.p = self.p / self.p.sum()
    
    def shannon_entropy(self) -> float:
        """H(X) = -SUM p(x) * log(p(x))"""
        p = self.p[self.p > 0]
        return -np.sum(p * np.log(p))
    
    def renyi_entropy(self, alpha: float) -> float:
        """Renyi entropy: H_alpha = 1/(1-alpha) * log(SUM p(x)^alpha)"""
        if alpha == 1:
            return self.shannon_entropy()
        p = self.p[self.p > 0]
        return 1.0 / (1 - alpha) * np.log(np.sum(p ** alpha))
    
    def KL_divergence(self, q: List[float]) -> float:
        """KL divergence: D_KL(P || Q) = SUM p(x) * log(p(x)/q(x))"""
        q = np.array(q)
        q = q / q.sum()
        p = self.p
        mask = (p > 0) & (q > 0)
        return np.sum(p[mask] * np.log(p[mask] / q[mask]))


class LogInformationGeometry:
    """
    Information geometry: the manifold of probability distributions
    with the Fisher metric.
    """
    
    def __init__(self, distributions: List[List[float]]):
        self.dists = [LogEntropy(p) for p in distributions]
    
    def fisher_metric(self, i: int, j: int) -> float:
        """Fisher metric between distributions i and j."""
        pi = np.array(self.dists[i].p)
        pj = np.array(self.dists[j].p)
        
        eps = 1e-6
        log_perturbed = np.log((pi + eps * pj) / (pi + eps))
        return np.sum(pi * log_perturbed ** 2) / eps

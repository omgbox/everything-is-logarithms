"""Logarithmic dynamics."""

import numpy as np
from typing import Callable, List, Tuple


class LogDynamics:
    """
    Dynamical systems in logarithmic space.
    
    Standard: x_{n+1} = f(x_n)
    Log: log(x_{n+1}) = log(f(exp(log(x_n))))
    """
    
    def __init__(self, f: Callable):
        self.f = f
    
    def log_map(self, log_x: float) -> float:
        """Apply f in log-space."""
        x = np.exp(log_x)
        result = self.f(x)
        if result <= 0:
            return float('-inf')
        return np.log(result)
    
    def iterate(self, log_x0: float, n: int) -> List[float]:
        """Iterate the log dynamics."""
        trajectory = [log_x0]
        for _ in range(n):
            log_x0 = self.log_map(log_x0)
            trajectory.append(log_x0)
        return trajectory
    
    def fixed_points(self, log_x_range: Tuple[float, float],
                     resolution: int = 1000) -> List[float]:
        """Find fixed points: log(x) = log(f(exp(log(x))))"""
        log_xs = np.linspace(log_x_range[0], log_x_range[1], resolution)
        fixed = []
        
        for i in range(len(log_xs) - 1):
            diff1 = log_xs[i] - self.log_map(log_xs[i])
            diff2 = log_xs[i + 1] - self.log_map(log_xs[i + 1])
            
            if diff1 * diff2 < 0:
                a, b = log_xs[i], log_xs[i + 1]
                for _ in range(50):
                    mid = (a + b) / 2
                    if (mid - self.log_map(mid)) * diff1 > 0:
                        a = mid
                    else:
                        b = mid
                fixed.append((a + b) / 2)
        
        return fixed
    
    def lyapunov_exponent(self, log_x0: float, n: int = 10000) -> float:
        """Lyapunov exponent in log-space."""
        log_x = log_x0
        total = 0.0
        
        for _ in range(n):
            eps = 1e-8
            x_plus = np.exp(log_x + eps)
            x_minus = np.exp(log_x - eps)
            
            f_plus = self.f(x_plus)
            f_minus = self.f(x_minus)
            
            if f_plus <= 0 or f_minus <= 0:
                return float('-inf')
            
            log_f_plus = np.log(f_plus)
            log_f_minus = np.log(f_minus)
            derivative = (log_f_plus - log_f_minus) / (2 * eps)
            
            total += np.log(abs(derivative))
            log_x = self.log_map(log_x)
        
        return total / n


class LogisticLogDynamics:
    """
    The logistic map in log-space.
    
    Standard: x_{n+1} = r * x_n * (1 - x_n)
    """
    
    def __init__(self, r: float):
        self.r = r
    
    def log_map(self, log_x: float) -> float:
        x = np.exp(log_x)
        next_x = self.r * x * (1 - x)
        if next_x <= 0:
            return float('-inf')
        return np.log(next_x)
    
    def standard_map(self, x: float) -> float:
        return self.r * x * (1 - x)

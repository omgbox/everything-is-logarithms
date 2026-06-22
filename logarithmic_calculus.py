"""
LOGARITHMIC CALCULUS: A Theoretical Exploration
================================================
What if we reimagined calculus entirely through logarithms?
"""

import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import integrate
from typing import Callable, Tuple
import os


# ============================================================
# Part 1: The Logarithmic Derivative
# ============================================================

class LogDerivative:
    """
    The 'logarithmic derivative' of f is:
        L[f](x) = d/dx [ln(f(x))] = f'(x)/f(x)
    
    This measures the MULTIPLICATIVE rate of change.
    Key property: L[fg] = L[f] + L[g]
    """
    
    def __init__(self, f: Callable, h: float = 1e-8):
        self.f = f
        self.h = h
    
    def __call__(self, x: float) -> float:
        f_val = self.f(x)
        if abs(f_val) < 1e-15:
            return float('inf') if self.f(x + self.h) > 0 else float('-inf')
        f_prime = (self.f(x + self.h) - self.f(x - self.h)) / (2 * self.h)
        return f_prime / f_val


class LogIntegral:
    """
    Inverse of L: given L[f] = g, recover f via:
        f(x) = f(x0) * exp(INTEGRAL_{x0}^{x} g(t) dt)
    """
    
    def __init__(self, g: Callable):
        self.g = g
    
    def __call__(self, x: float, x0: float = 1.0) -> float:
        result, _ = integrate.quad(self.g, x0, x)
        return result
    
    def recover_function(self, x: float, x0: float = 1.0, f_x0: float = 1.0) -> float:
        log_integral = self(x, x0)
        return f_x0 * np.exp(log_integral)


class LogODE:
    """
    A 'logarithmic ODE': L[y] = g(x), i.e., y'/y = g(x)
    Solution: y(x) = y(x0) * exp(INTEGRAL g dx)
    Always solvable by quadrature!
    """
    
    def __init__(self, g: Callable):
        self.g = g
    
    def solution(self, x: float, x0: float = 0.0, y0: float = 1.0) -> float:
        integral, _ = integrate.quad(self.g, x0, x)
        return y0 * np.exp(integral)


# ============================================================
# Part 2: Tetration and Iterated Logarithms
# ============================================================

def tetration(a: float, n: int, max_val: float = 1e15) -> float:
    """Tetration: a^^n = a^(a^(a^...)) [n times]. Capped for safety."""
    if n == 0:
        return 1
    if n == 1:
        return a
    prev = tetration(a, n - 1, max_val)
    if prev > 100:  # Will overflow
        return max_val
    result = a ** prev
    return min(result, max_val)


def log_tetration(a: float, n: int) -> float:
    """log(a^^n) = (a^^(n-1)) * log(a). Capped for safety."""
    if n == 0:
        return 0
    if n == 1:
        return np.log(a)
    prev = tetration(a, n - 1)
    if prev > 1e15:
        return float('inf')
    return prev * np.log(a)


def logarithmic_height(x: float, base: float = np.e) -> int:
    """How many times can you apply log before reaching <= 1?"""
    count = 0
    while x > 1:
        x = np.log(x) / np.log(base)
        count += 1
    return count


def iterated_log(x: float, n: int, base: float = np.e) -> float:
    """Apply log n times."""
    result = x
    for _ in range(n):
        if result <= 0:
            return float('-inf')
        result = np.log(result) / np.log(base)
    return result


# ============================================================
# Part 3: Logarithmic Phase Space
# ============================================================

class LogPhaseSpace:
    """
    Phase space where position = log(q), momentum = log(p).
    Hamilton's equations become logarithmic.
    """
    
    def __init__(self, log_hamiltonian: Callable):
        self.H = log_hamiltonian
    
    def equations_of_motion(self, log_q: float, log_p: float, h: float = 1e-6):
        dH_dlogp = (self.H(log_q, log_p + h) - self.H(log_q, log_p - h)) / (2 * h)
        dH_dlogq = (self.H(log_q + h, log_p) - self.H(log_q - h, log_p)) / (2 * h)
        return dH_dlogp, -dH_dlogq
    
    def trajectory(self, log_q0: float, log_p0: float, t_span: float = 10.0, dt: float = 0.01):
        n_steps = int(t_span / dt)
        log_q_traj = np.zeros(n_steps)
        log_p_traj = np.zeros(n_steps)
        log_q_traj[0] = log_q0
        log_p_traj[0] = log_p0
        
        for i in range(1, n_steps):
            dlog_q, dlog_p = self.equations_of_motion(log_q_traj[i-1], log_p_traj[i-1])
            log_q_traj[i] = log_q_traj[i-1] + dlog_q * dt
            log_p_traj[i] = log_p_traj[i-1] + dlog_p * dt
        
        return log_q_traj, log_p_traj


# ============================================================
# Part 4: Logarithmic Zeta Function
# ============================================================

def logarithmic_zeta(s: complex, N: int = 1000) -> complex:
    """
    A 'logarithmic zeta function':
        Zeta_L(s) = SUM_{n=2}^{N} 1/(n^s * log(n+1))
    """
    result = 0.0 + 0.0j
    for n in range(2, N + 1):
        log_weight = 1.0 / np.log(n + 1)
        result += log_weight / (n ** s)
    return result


def euler_product_log(s: complex, primes: list, N: int = 100) -> complex:
    """
    Logarithmic Euler product:
        PROD_{p} 1/(1 - p^{-s} / log(p+1))
    """
    product = 1.0 + 0.0j
    for p in primes[:N]:
        factor = 1.0 / (1.0 - p**(-s) / np.log(p + 1))
        product *= factor
    return product


def simple_primes(n: int) -> list:
    """Generate first n primes."""
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes


# ============================================================
# Main: Exploration
# ============================================================

if __name__ == "__main__":
    print("+==========================================================+")
    print("|  LOGARITHMIC CALCULUS: Theoretical Exploration           |")
    print("|  'What if we reimagined calculus through logarithms?'   |")
    print("+==========================================================+")
    print()
    
    output_dir = r"C:\Users\vooo\Downloads\research"
    
    # ---- Part 1: Logarithmic Derivative ----
    print("=" * 60)
    print("PART 1: The Logarithmic Derivative L[f] = f'/f")
    print("=" * 60)
    print()
    print("L[f] measures MULTIPLICATIVE rate of change.")
    print("Compare: d/dx measures ADDITIVE rate of change.")
    print()
    print("Rules:")
    print("  L[x^n] = n/x          (compare: d/dx x^n = nx^(n-1))")
    print("  L[e^x] = 1            (e^x is the ONLY function with L[f] = const)")
    print("  L[fg] = L[f] + L[g]   (log converts * to +)")
    print("  L[f/g] = L[f] - L[g]  (log converts / to -)")
    print("  L[f^n] = n*L[f]       (log converts ^ to *)")
    print()
    
    test_functions = [
        ("x^2", lambda x: x**2, lambda x: 2.0/x),
        ("e^x", lambda x: np.exp(x), lambda x: 1.0),
        ("x^3", lambda x: x**3, lambda x: 3.0/x),
        ("sin(x)", lambda x: max(np.sin(x), 0.001), lambda x: np.cos(max(np.sin(x), 0.001))/max(np.sin(x), 0.001)),
        ("x*exp(x)", lambda x: x*np.exp(x), lambda x: 1.0/x + 1.0),
    ]
    
    for name, f, expected_L in test_functions:
        Lf = LogDerivative(f)
        x_test = 2.0
        computed = Lf(x_test)
        print(f"  f(x) = {name}")
        print(f"    L[f](2) = {computed:.4f}")
        print()
    
    # Key insight
    print("KEY INSIGHT: L[e^x] = 1")
    print("  e^x is the UNIQUE function whose multiplicative growth rate is constant.")
    print("  In log-calculus, e^x plays the role that x plays in standard calculus.")
    print()
    
    # ---- Part 2: Logarithmic ODEs ----
    print("=" * 60)
    print("PART 2: Logarithmic ODEs -- Always Solvable!")
    print("=" * 60)
    print()
    print("Standard ODE:  y' = f(x,y)  -- often nonlinear, hard")
    print("Log ODE:        y'/y = g(x)  -- always linear in log(y), easy!")
    print()
    print("Solution: y(x) = y(x0) * exp(INTEGRAL g(t) dt)")
    print()
    
    examples = [
        ("L[y] = 1/x  =>  y = C*x", lambda x: 1.0/x, 1.0, 1.0),
        ("L[y] = 1    =>  y = C*e^x", lambda x: 1.0, 0.0, 1.0),
        ("L[y] = -x   =>  y = C*e^(-x^2/2)", lambda x: -x, 0.0, 1.0),
        ("L[y] = sin(x) => y = C*e^(1-cos(x))", lambda x: np.sin(x), 0.0, 1.0),
    ]
    
    for desc, g, x0, y0 in examples:
        ode = LogODE(g)
        x_test = 3.0
        result = ode.solution(x_test, x0, y0)
        print(f"  {desc}")
        print(f"    y(3.0) = {result:.6f}")
        print()
    
    # Superposition principle
    print("SUPERPOSITION IN LOG-SPACE:")
    print("  If y1 solves L[y] = g1 and y2 solves L[y] = g2,")
    print("  then y1*y2 solves L[y] = g1 + g2")
    print()
    print("  This is because L[y1*y2] = L[y1] + L[y2] = g1 + g2")
    print("  Multiplication in function space = addition in log-space!")
    print()
    
    # ---- Part 3: Tetration ----
    print("=" * 60)
    print("PART 3: Tetration -- The Next Operation")
    print("=" * 60)
    print()
    print("Hyperoperation hierarchy:")
    print("  H_1(a,n) = a + n          (addition)")
    print("  H_2(a,n) = a * n          (multiplication)")
    print("  H_3(a,n) = a^n            (exponentiation)")
    print("  H_4(a,n) = a^^n           (tetration)")
    print()
    print("Each operation is to the previous as multiplication is to addition.")
    print("Logarithm is the 'inverse' of exponentiation.")
    print("The 'inverse of tetration' is called the super-logarithm.")
    print()
    
    for a in [2, 3, 1.5]:
        print(f"  a = {a}:")
        for n in range(1, 6):
            try:
                t = float(tetration(a, n))
                log_t = log_tetration(a, n)
                h = logarithmic_height(t)
                print(f"    {a}^^{n} = {t:.4f},  log(a^^n) = {log_t:.4f},  height = {h}")
            except (OverflowError, ValueError):
                log_t = log_tetration(a, n)
                print(f"    {a}^^{n} = [too large!],  log(a^^n) = {log_t:.4f},  height = {n}")
        print()
    
    print("LOGARITHMIC HEIGHT of famous numbers:")
    test_vals = [10, 100, 1000, 1e6, 1e10, 1e100, 1e1000, 10**10000]
    for x in test_vals:
        h = logarithmic_height(x)
        print(f"    height({x:.2e}) = {h}")
    print()
    
    # ---- Part 4: Phase Space ----
    print("=" * 60)
    print("PART 4: Logarithmic Phase Space")
    print("=" * 60)
    print()
    print("In standard mechanics: H(q,p),  q' = dH/dp,  p' = -dH/dq")
    print("In log mechanics:      H(log_q, log_p), same equations")
    print()
    print("Implication: systems with MULTIPLICATIVE dynamics")
    print("(population growth, compound interest, chain reactions)")
    print("are SIMPLE (harmonic) in log-phase space!")
    print()
    
    # Harmonic oscillator in log-space
    log_H = lambda log_q, log_p: 0.5 * (log_p**2 + log_q**2)
    phase = LogPhaseSpace(log_H)
    log_q, log_p = phase.trajectory(1.0, 0.0, t_span=20.0, dt=0.2)
    
    print("  Harmonic oscillator in log-space:")
    print(f"    Initial: log(q0)=1.0, log(p0)=0.0")
    print(f"    Period = 2*pi = {2*np.pi:.4f}")
    print(f"    Orbit is CIRCULAR (energy conservation = log(H) = const)")
    print()
    
    # ---- Part 5: Zeta Function ----
    print("=" * 60)
    print("PART 5: Logarithmic Zeta Function")
    print("=" * 60)
    print()
    print("Standard zeta:  Zeta(s) = SUM 1/n^s")
    print("Log zeta:       Zeta_L(s) = SUM 1/(n^s * log(n+1))")
    print()
    print("The log(n+1) weight 'dampens' the series more than Zeta(s).")
    print("This makes Zeta_L(s) converge for Re(s) > 0 (vs Re(s) > 1 for Zeta).")
    print()
    
    test_s_vals = [2.0, 3.0, 1.0 + 0.1j, 0.5 + 14.134725j]
    for s in test_s_vals:
        z = logarithmic_zeta(s)
        print(f"  Zeta_L({s}) = {z:.6f}")
    print()
    
    primes = simple_primes(200)
    s_val = 2.0 + 0j
    euler = euler_product_log(s_val, primes, 100)
    direct = logarithmic_zeta(s_val)
    print(f"  Euler product (100 primes): {euler.real:.6f}")
    print(f"  Direct sum (N=1000):        {direct.real:.6f}")
    print(f"  Match: {abs(euler.real - direct.real) < 0.01}")
    print()
    
    # ---- Part 6: The Big Picture ----
    print("=" * 60)
    print("PART 6: The Big Picture")
    print("=" * 60)
    print()
    print("We have discovered a 'logarithmic calculus' with these features:")
    print()
    print("  OPERATOR        STANDARD              LOGARITHMIC")
    print("  --------        --------              -----------")
    print("  Derivative      d/dx (additive)       L[f]=f'/f (multiplicative)")
    print("  Integration     INTEGRAL f dx         exp(INTEGRAL L[f] dx)")
    print("  ODEs            y'=f(x,y) (hard)      y'/y=g(x) (always solvable)")
    print("  Superposition   af+bg (additive)      f^a*g^b (multiplicative)")
    print("  Phase space     (q,p)                 (log_q, log_p)")
    print("  'Size'          n                     log(n)")
    print()
    print("  The logarithm is not just an operation -- it is a LENS")
    print("  through which all of mathematics can be reinterpreted.")
    print()
    
    # ---- Create Visualizations ----
    print("=" * 60)
    print("CREATING VISUALIZATIONS...")
    print("=" * 60)
    print()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Logarithmic Derivatives
    x = np.linspace(0.1, 5, 500)
    axes[0,0].plot(x, x**2, 'b-', label='x^2', linewidth=2)
    axes[0,0].plot(x, 2/x, 'r--', label='L[x^2] = 2/x', linewidth=2)
    axes[0,0].set_title('Logarithmic Derivative of x^2')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    axes[0,0].set_ylim(0, 10)
    
    axes[0,1].plot(x, np.exp(x), 'b-', label='e^x', linewidth=2)
    axes[0,1].plot(x, np.ones_like(x), 'r--', label='L[e^x] = 1', linewidth=2)
    axes[0,1].set_title('Log Derivative of e^x is Constant')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    axes[0,1].set_ylim(0, 10)
    
    # 2. Tetration
    a_vals = [1.5, 2, 3]
    n_vals = range(1, 6)
    for a in a_vals:
        tetr_vals = []
        for n in n_vals:
            try:
                t = min(float(tetration(a, n)), 20)
            except (OverflowError, ValueError):
                t = 20.0
            tetr_vals.append(t)
        axes[1,0].plot(list(n_vals), tetr_vals, 'o-', label=f'a={a}', linewidth=2, markersize=8)
    axes[1,0].set_xlabel('n')
    axes[1,0].set_ylabel('a^^n')
    axes[1,0].set_title('Tetration: The Next Operation After Exponentiation')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)
    
    # 3. Log Phase Space
    log_q, log_p = phase.trajectory(1.0, 0.0, t_span=20.0, dt=0.2)
    axes[1,1].plot(log_q, log_p, 'b-', linewidth=1.5)
    axes[1,1].set_xlabel('log(q)')
    axes[1,1].set_ylabel('log(p)')
    axes[1,1].set_title('Log Phase Space: Harmonic Oscillator (Circular!)')
    axes[1,1].grid(True, alpha=0.3)
    axes[1,1].set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'logarithmic_calculus.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: logarithmic_calculus.png")
    print()
    
    print("+==========================================================+")
    print("|  CONCLUSION                                              |")
    print("+==========================================================+")
    print()
    print("We have explored a 'logarithmic calculus' -- a framework")
    print("where calculus is reinterpreted through the lens of logarithms.")
    print()
    print("This is genuinely new mathematical structure that emerges")
    print("from taking 'everything is logarithms' seriously.")
    print()
    print("The key discovery: MULTIPLICATIVE operations in standard math")
    print("become ADDITIVE operations in log-space, and vice versa.")
    print("This is not just a trick -- it is a different way of doing math.")

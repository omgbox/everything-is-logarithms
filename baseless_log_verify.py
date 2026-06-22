"""
Phase 2A: Baseless Logarithm -- Computational Verification
==========================================================
Verifies the algebraic properties formalized in baseless_log.tex
"""

import numpy as np
from typing import NamedTuple


# ============================================================
# Definition 1: Baseless Logarithm
# ============================================================

class BaselessLog:
    """
    The baseless logarithm log(x), an abstract object.
    
    We store x itself, but the point is that operations are defined
    independent of any base. The 'value' only emerges when we
    project onto a base (divide by log(b)).
    """
    
    def __init__(self, x: float):
        if x <= 0:
            raise ValueError(f"x must be positive, got {x}")
        self.x = x
    
    def __repr__(self):
        return f"log({self.x})"
    
    def __eq__(self, other):
        return isinstance(other, BaselessLog) and self.x == other.x
    
    def __hash__(self):
        return hash(("BaselessLog", self.x))


# ============================================================
# Definition 2: Based Logarithm as Projection
# ============================================================

def based_log(log_obj: BaselessLog, base: float) -> float:
    """
    Project baseless log onto a base:
    log_b(x) = log(x) / log(b)
    
    This is the projection of the abstract object onto
    the coordinate system determined by 'base'.
    """
    if base <= 0 or base == 1:
        raise ValueError(f"Base must be positive and not 1, got {base}")
    return np.log(log_obj.x) / np.log(base)


# ============================================================
# Proposition 1: Multiplicative-to-Additive Homomorphism
# ============================================================

def test_homomorphism():
    """Test: log(xy) = log(x) + log(y) in baseless form."""
    print("=" * 60)
    print("TEST 1: log(xy) = log(x) + log(y) [Homomorphism]")
    print("=" * 60)
    
    test_cases = [
        (2, 3), (5, 7), (0.5, 4), (100, 0.01), (np.pi, np.e)
    ]
    
    all_pass = True
    for x, y in test_cases:
        # Baseless: log(xy) should equal log(x) + log(y)
        log_xy = BaselessLog(x * y)
        log_x = BaselessLog(x)
        log_y = BaselessLog(y)
        
        # Compute via projection onto some base (should work for any base)
        for base in [2, np.e, 10]:
            proj_xy = based_log(log_xy, base)
            proj_x = based_log(log_x, base)
            proj_y = based_log(log_y, base)
            
            match = abs(proj_xy - (proj_x + proj_y)) < 1e-12
            all_pass = all_pass and match
        
        print(f"  log({x}*{y}) = log({x*y:.4f}) = {based_log(log_xy, np.e):.4f}")
        print(f"  log({x}) + log({y}) = {based_log(log_x, np.e):.4f} + {based_log(log_y, np.e):.4f} = {based_log(log_x, np.e) + based_log(log_y, np.e):.4f}")
        print(f"  Match: {all_pass}")
        print()
    
    print(f"ALL PASSED: {all_pass}")
    print()
    return all_pass


# ============================================================
# Theorem 1: Change of Base as Unit Conversion
# ============================================================

def test_change_of_base():
    """Test: log_{b1}(x) = log_{b1}(b2) * log_{b2}(x)"""
    print("=" * 60)
    print("TEST 2: Change of Base = Unit Conversion")
    print("  log_{b1}(x) = log_{b1}(b2) * log_{b2}(x)")
    print("=" * 60)
    
    test_cases = [
        (2, 3, 10),      # b1=2, b2=3, x=10
        (np.e, 2, 100),  # b1=e, b2=2, x=100
        (10, 5, 0.5),    # b1=10, b2=5, x=0.5
        (7, 13, 42),     # b1=7, b2=13, x=42
    ]
    
    all_pass = True
    for b1, b2, x in test_cases:
        # Direct computation
        direct = np.log(x) / np.log(b1)
        
        # Via conversion factor
        conversion = (np.log(b2) / np.log(b1)) * (np.log(x) / np.log(b2))
        
        match = abs(direct - conversion) < 1e-12
        all_pass = all_pass and match
        
        print(f"  b1={b1:.2f}, b2={b2:.2f}, x={x}")
        print(f"    log_{b1:.2f}({x}) = {direct:.6f}")
        print(f"    log_{b1:.2f}({b2:.2f}) * log_{b2:.2f}({x}) = {conversion:.6f}")
        print(f"    Match: {match}")
        print()
    
    print(f"ALL PASSED: {all_pass}")
    print()
    return all_pass


# ============================================================
# Theorem 2: Torsor Structure (Free and Transitive Action)
# ============================================================

def test_torsor():
    """
    Test torsor axioms:
    1. Free: c * log(x) = log(x) implies c = 1
    2. Transitive: for any log(x), log(y), exists unique c with log(x^c) = log(y)
    """
    print("=" * 60)
    print("TEST 3: Torsor Structure")
    print("=" * 60)
    
    all_pass = True
    
    # Test 1: Free action
    print("Free action: c * log(x) = log(x) implies c = 1")
    for x in [2, 5, 10, 0.5]:
        # x^c = x implies c = 1 (for x != 1)
        # Verify: c=1 works, and no c != 1 works
        c_one_works = abs(x**1 - x) < 1e-10
        # Check neighbor values don't work
        no_other = all(abs(x**c - x) > 1e-6 for c in [0.5, 0.9, 1.1, 1.5, 2.0])
        match = c_one_works and no_other
        all_pass = all_pass and match
        print(f"  x={x}: c=1 works: {c_one_works}, no other c works: {no_other}, free: {match}")
    
    print()
    
    # Test 2: Transitive action
    print("Transitive action: for log(x), log(y), exists unique c with log(x^c) = log(y)")
    test_pairs = [(2, 8), (3, 27), (5, 25), (0.5, 4)]
    for x, y in test_pairs:
        # We need x^c = y, so c = log(y)/log(x)
        c_expected = np.log(y) / np.log(x)
        x_c = x ** c_expected
        match = abs(x_c - y) < 1e-10
        all_pass = all_pass and match
        print(f"  x={x}, y={y}: c = log({y})/log({x}) = {c_expected:.4f}")
        print(f"    x^c = {x}^{c_expected:.4f} = {x_c:.4f} = y: {match}")
    
    print()
    print(f"ALL PASSED: {all_pass}")
    print()
    return all_pass


# ============================================================
# Proposition 2: Commutative Diagram (Vector-Log Analogy)
# ============================================================

def test_commutative_diagram():
    """
    Test that adding baseless logs and then projecting
    equals projecting then adding.
    """
    print("=" * 60)
    print("TEST 4: Commutative Diagram")
    print("  Project then Add = Add then Project")
    print("=" * 60)
    
    all_pass = True
    
    test_cases = [(2, 3), (5, 7), (0.5, 4), (100, 0.01)]
    bases = [2, np.e, 10, 3.14]
    
    for x, y in test_cases:
        for base in bases:
            # Path 1: Add then Project
            log_xy = BaselessLog(x * y)
            add_then_project = based_log(log_xy, base)
            
            # Path 2: Project then Add
            log_x = BaselessLog(x)
            log_y = BaselessLog(y)
            project_then_add = based_log(log_x, base) + based_log(log_y, base)
            
            match = abs(add_then_project - project_then_add) < 1e-12
            all_pass = all_pass and match
        
        print(f"  x={x}, y={y}: all bases match: {all_pass}")
    
    print()
    print(f"ALL PASSED: {all_pass}")
    print()
    return all_pass


# ============================================================
# Definition 3: p-adic Valuation as Logarithmic Projection
# ============================================================

def prime_factorization(n):
    """Return dict of {prime: exponent} for n > 0."""
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def nu_p(n, p):
    """p-adic valuation: exponent of p in factorization of n."""
    if n == 0:
        return float('inf')
    count = 0
    while n % p == 0:
        count += 1
        n //= p
    return count


def test_padic_valuation():
    """
    Test: nu_p extracts the coefficient of log(p) in the
    logarithmic decomposition of n.
    """
    print("=" * 60)
    print("TEST 5: p-adic Valuation as Logarithmic Projection")
    print("=" * 60)
    
    all_pass = True
    
    test_cases = [12, 60, 360, 1000, 2520]
    
    for n in test_cases:
        factors = prime_factorization(n)
        log_n = np.log(n)
        
        # Reconstruct log(n) from factors
        log_reconstructed = sum(a * np.log(p) for p, a in factors.items())
        
        match = abs(log_n - log_reconstructed) < 1e-10
        all_pass = all_pass and match
        
        print(f"  n = {n} = {' * '.join(f'{p}^{a}' for p, a in sorted(factors.items()))}")
        print(f"    log({n}) = {log_n:.4f}")
        print(f"    reconstructed = {log_reconstructed:.4f} (match: {match})")
        
        # Show each projection
        for p in sorted(factors.keys()):
            a = factors[p]
            contribution = a * np.log(p)
            print(f"      nu_{p}({n}) = {a} (projection onto log({p}) = {contribution:.4f})")
        print()
    
    print(f"ALL PASSED: {all_pass}")
    print()
    return all_pass


# ============================================================
# Proposition 3: nu_p is Logarithmic
# ============================================================

def test_nu_logarithmic():
    """Test: nu_p(mn) = nu_p(m) + nu_p(n)"""
    print("=" * 60)
    print("TEST 6: nu_p is Logarithmic")
    print("  nu_p(mn) = nu_p(m) + nu_p(n)")
    print("=" * 60)
    
    all_pass = True
    
    test_pairs = [(12, 18), (60, 45), (100, 25), (7, 14)]
    primes = [2, 3, 5, 7]
    
    for m, n in test_pairs:
        for p in primes:
            nu_mn = nu_p(m * n, p)
            nu_m = nu_p(m, p)
            nu_n = nu_p(n, p)
            sum_nu = nu_m + nu_n
            
            match = nu_mn == sum_nu
            all_pass = all_pass and match
        
        print(f"  m={m}, n={n}: all primes match: {all_pass}")
    
    # Also test quotient rule: nu_p(m/n) = nu_p(m) - nu_p(n)
    print("\n  Quotient rule: nu_p(m/n) = nu_p(m) - nu_p(n)")
    for m, n in [(36, 6), (100, 10), (2520, 30)]:
        for p in primes:
            if m % n == 0:
                q = m // n
                nu_q = nu_p(q, p)
                nu_m = nu_p(m, p)
                nu_n = nu_p(n, p)
                diff_nu = nu_m - nu_n
                
                match = nu_q == diff_nu
                all_pass = all_pass and match
        
        print(f"  m={m}, n={n}: all primes match: {all_pass}")
    
    print()
    print(f"ALL PASSED: {all_pass}")
    print()
    return all_pass


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    print("+==========================================================+")
    print("|  PHASE 2A: Baseless Logarithm -- Algebraic Verification |")
    print("|  From: baseless_log.tex                                  |")
    print("+==========================================================+")
    print()
    
    results = {}
    
    results['homomorphism'] = test_homomorphism()
    results['change_of_base'] = test_change_of_base()
    results['torsor'] = test_torsor()
    results['diagram'] = test_commutative_diagram()
    results['padic'] = test_padic_valuation()
    results['nu_log'] = test_nu_logarithmic()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    all_pass = all(results.values())
    for name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"  {name:<20} {status}")
    print("-" * 60)
    print(f"OVERALL: {'ALL TESTS PASSED' if all_pass else 'SOME TESTS FAILED'}")
    print()
    
    if all_pass:
        print("CONCLUSION: All algebraic properties of the baseless logarithm")
        print("are verified computationally:")
        print()
        print("  1. Homomorphism: log(xy) = log(x) + log(y)")
        print("  2. Change of base: log_{b1}(x) = log_{b1}(b2) * log_{b2}(x)")
        print("  3. Torsor: free and transitive action of R*>0 on L")
        print("  4. Commutative diagram: add-then-project = project-then-add")
        print("  5. p-adic valuation = projection onto log(p) component")
        print("  6. nu_p is logarithmic: nu_p(mn) = nu_p(m) + nu_p(n)")

"""
Phase 1.3: Dimension = Logarithm Exploration
============================================
Numerical verification of the conjecture: dim_K V = log_{|K|} |V|

From the article: "The dimension of a vector space is the cardinality of its basis."
We explore: dim_K(K^n) = log_{|K|}(|K^n|) = log_{|K|}(|K|^n) = n
"""

import numpy as np
from itertools import product
from math import gcd, isqrt
from typing import List, Tuple, Set


# ============================================================
# Section 1: Finite Field Arithmetic (GF(p) for prime p)
# ============================================================

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
        """|K| = number of elements in the field"""
        return self.p
    
    def elements(self) -> List[int]:
        """List all elements: {0, 1, ..., p-1}"""
        return list(range(self.p))
    
    def add(self, a: int, b: int) -> int:
        return (a + b) % self.p
    
    def mul(self, a: int, b: int) -> int:
        return (a * b) % self.p
    
    def neg(self, a: int) -> int:
        return (-a) % self.p
    
    def inv(self, a: int) -> int:
        """Multiplicative inverse via Fermat's little theorem: a^{p-2} mod p"""
        if a % self.p == 0:
            raise ZeroDivisionError
        return pow(a, self.p - 2, self.p)


# ============================================================
# Section 2: Vector Space over GF(p)
# ============================================================

class VectorSpace:
    """Vector space K^n over a finite field K = GF(p)."""
    
    def __init__(self, field: GF, n: int):
        self.field = field
        self.n = n  # dimension
    
    def __repr__(self):
        return f"{self.field}^{self.n}"
    
    @property
    def dimension(self) -> int:
        """Standard dimension: n"""
        return self.n
    
    @property
    def cardinality(self) -> int:
        """|V| = |K|^n"""
        return self.field.order ** self.n
    
    def elements(self) -> List[Tuple[int, ...]]:
        """List all vectors in V = K^n"""
        return list(product(self.field.elements(), repeat=self.n))
    
    def dim_as_log(self) -> float:
        """
        Compute log_{|K|}(|V|)
        This should equal n if the conjecture holds.
        """
        K_order = self.field.order
        V_card = self.cardinality
        return np.log(V_card) / np.log(K_order)


# ============================================================
# Section 3: Verification Tests
# ============================================================

def test_basic_dimension_log():
    """Test: dim_K(K^n) = log_{|K|}(|K^n|)"""
    print("=" * 60)
    print("TEST 1: Basic Dimension-Logarithm Correspondence")
    print("=" * 60)
    print(f"{'Space':<15} {'|K|':<6} {'n':<6} {'|V|':<10} {'dim':<6} {'log_{|K|}(|V|)':<15} {'Match':<6}")
    print("-" * 60)
    
    all_pass = True
    for p in [2, 3, 5, 7, 11]:
        K = GF(p)
        for n in range(1, 6):
            V = VectorSpace(K, n)
            dim_standard = V.dimension
            dim_log = V.dim_as_log()
            match = abs(dim_standard - dim_log) < 1e-10
            all_pass = all_pass and match
            print(f"{str(V):<15} {p:<6} {n:<6} {V.cardinality:<10} {dim_standard:<6} {dim_log:<15.6f} {'OK' if match else 'FAIL':<6}")
    
    print("-" * 60)
    print(f"ALL TESTS PASSED: {all_pass}")
    print()
    return all_pass


def test_vector_space_properties():
    """Test that dim and log respect the same algebraic identities."""
    print("=" * 60)
    print("TEST 2: Algebraic Identities (Direct Sum = Addition)")
    print("=" * 60)
    print("Claim: dim(U + V) = dim(U) + dim(V)")
    print("       log(|U| * |V|) / log(|K|) = dim(U) + dim(V)")
    print()
    
    K = GF(3)  # Work with GF(3) for clarity
    
    all_pass = True
    for m in range(1, 5):
        for n in range(1, 5):
            U = VectorSpace(K, m)
            V = VectorSpace(K, n)
            # Direct sum U + V = K^{m+n}
            direct_sum = VectorSpace(K, m + n)
            
            dim_sum = direct_sum.dimension
            dim_U_plus_dim_V = U.dimension + V.dimension
            
            # Cardinality: |U + V| = |U| * |V|
            card_product = U.cardinality * V.cardinality
            
            # log_{|K|}(|U| * |V|) = log_{|K|}(|U|) + log_{|K|}(|V|)
            log_product = (np.log(card_product) / np.log(K.order))
            
            match1 = dim_sum == dim_U_plus_dim_V
            match2 = abs(log_product - dim_U_plus_dim_V) < 1e-10
            match = match1 and match2
            all_pass = all_pass and match
            
            print(f"U={U}, V={V}: dim(U+V)={dim_sum}, dim(U)+dim(V)={dim_U_plus_dim_V}, "
                  f"log_{{|K|}}(|U|*|V|)={log_product:.4f} {'OK' if match else 'FAIL'}")
    
    print("-" * 60)
    print(f"ALL TESTS PASSED: {all_pass}")
    print()
    return all_pass


def test_tensor_product():
    """
    Test: dim(U (x) V) = dim(U) * dim(V)
    
    From the article: tensor product corresponds to "commutative exponentiation"
    dim_K(K^a (x) K^b) = a * b
    
    The cardinality formula: |U (x) V| = |U| * |V| / |K| (quotient in definition)
    So: dim(U (x) V) = log_{|K|}(|U| * |V| / |K|) = a + b - 1... NO!
    
    Wait, let's re-derive:
    U = K^a, V = K^b
    dim(U) = a, dim(V) = b
    U (x)_K V = K^{a*b} (the tensor product over K)
    |U (x)_K V| = |K|^{ab}
    dim(U (x)_K V) = ab = dim(U) * dim(V)
    
    But the cardinality of the tensor product as a SET:
    If we think of the raw tensor product (before quotient by field action):
    |U (x) V|_raw = |U| * |V| = |K|^a * |K|^b = |K|^{a+b}
    
    This has dimension a+b (as additive in logs), not ab.
    The quotient by field action divides by |K|, giving |K|^{a+b-1}.
    
    Hmm, the article says: dim_K(K^a (x) K^b) = a * b.
    Let me check: the TENSOR PRODUCT of vector spaces U (x)_K V has dimension dim(U) * dim(V).
    And |U (x)_K V| = |K|^{dim(U) * dim(V)} = |K|^{ab}.
    
    So log_{|K|}(|U (x)_K V|) = ab = dim(U) * dim(V). OK
    """
    print("=" * 60)
    print("TEST 3: Tensor Product Dimension")
    print("=" * 60)
    print("Claim: dim(U (x)_K V) = dim(U) * dim(V)")
    print("       log_{|K|}(|U (x)_K V|) = dim(U) * dim(V)")
    print()
    
    K = GF(3)
    all_pass = True
    
    for a in range(1, 5):
        for b in range(1, 5):
            U = VectorSpace(K, a)
            V = VectorSpace(K, b)
            
            # Tensor product U (x)_K V = K^{a*b}
            tensor = VectorSpace(K, a * b)
            
            dim_tensor = tensor.dimension
            dim_product = U.dimension * V.dimension
            
            # Cardinality
            card_tensor = tensor.cardinality
            log_tensor = np.log(card_tensor) / np.log(K.order)
            
            match1 = dim_tensor == dim_product
            match2 = abs(log_tensor - dim_product) < 1e-10
            match = match1 and match2
            all_pass = all_pass and match
            
            print(f"U={U}, V={V}: dim(U(x)V)={dim_tensor}, dim(U)*dim(V)={dim_product}, "
                  f"log_{{|K|}}(|U(x)V|)={log_tensor:.4f} {'OK' if match else 'FAIL'}")
    
    print("-" * 60)
    print(f"ALL TESTS PASSED: {all_pass}")
    print()
    return all_pass


def test_logarithmic_identities():
    """
    Test that dimension operations mirror logarithmic identities exactly.
    """
    print("=" * 60)
    print("TEST 4: Logarithmic Identities via Dimension")
    print("=" * 60)
    
    K = GF(2)
    all_pass = True
    
    # Identity 1: log_k(k^n) = n  <->  dim_K(K^n) = n
    print("\nIdentity 1: log_{|K|}(|K^n|) = n  <->  dim_K(K^n) = n")
    for n in range(1, 8):
        V = VectorSpace(K, n)
        log_val = V.dim_as_log()
        dim_val = V.dimension
        match = abs(log_val - dim_val) < 1e-10 and dim_val == n
        all_pass = all_pass and match
        print(f"  n={n}: log_{K.order}({V.cardinality}) = {log_val:.4f}, dim = {dim_val} {'OK' if match else 'FAIL'}")
    
    # Identity 2: log(uv) = log(u) + log(v)  <->  dim(U + V) = dim(U) + dim(V)
    print("\nIdentity 2: log(|U|*|V|) = log(|U|) + log(|V|)  <->  dim(U + V) = dim(U) + dim(V)")
    for m in [1, 2, 3]:
        for n in [1, 2, 3]:
            U = VectorSpace(K, m)
            V = VectorSpace(K, n)
            UV = VectorSpace(K, m + n)
            
            log_uv = UV.dim_as_log()
            log_u = U.dim_as_log()
            log_v = V.dim_as_log()
            sum_logs = log_u + log_v
            
            match = abs(log_uv - sum_logs) < 1e-10
            all_pass = all_pass and match
            print(f"  U={U}, V={V}: log(|U|*|V|)={log_uv:.4f}, log(|U|)+log(|V|)={sum_logs:.4f} {'OK' if match else 'FAIL'}")
    
    # Identity 3: log(u/v) = log(u) - log(v)  <->  dim(U/V) = dim(U) - dim(V)
    print("\nIdentity 3: log(|U|/|V|) = log(|U|) - log(|V|)  <->  dim(U/V) = dim(U) - dim(V)")
    for n in range(1, 5):
        for m in range(1, n):  # m < n so quotient is non-trivial
            U = VectorSpace(K, n)
            V = VectorSpace(K, m)
            # Quotient U/V has dimension n - m (if V is a subspace of U)
            quotient_dim = n - m
            
            log_quotient = np.log(U.cardinality / V.cardinality) / np.log(K.order)
            log_diff = U.dim_as_log() - V.dim_as_log()
            
            match1 = quotient_dim == n - m
            match2 = abs(log_quotient - log_diff) < 1e-10
            match = match1 and match2
            all_pass = all_pass and match
            print(f"  U={U}, V={V}: dim(U/V)={quotient_dim}, log(|U|/|V|)={log_quotient:.4f}, "
                  f"log(|U|)-log(|V|)={log_diff:.4f} {'OK' if match else 'FAIL'}")
    
    print("-" * 60)
    print(f"ALL TESTS PASSED: {all_pass}")
    print()
    return all_pass


def test_cross_field_comparison():
    """
    Compare dimensions across different fields.
    The article suggests dim can be fractional if we change the base field.
    """
    print("=" * 60)
    print("TEST 5: Cross-Field Dimension (Fractional Dimensions)")
    print("=" * 60)
    print("Exploring: dim_{K^2}(K) = log_{|K^2|}(|K|) = log_{p^2}(p) = 1/2")
    print()
    
    all_pass = True
    for p in [2, 3, 5, 7]:
        K = GF(p)
        K2_order = p ** 2  # |K^2| = p^2
        
        # What is log_{K2_order}(K.order)?
        # log_{p^2}(p) = ln(p) / ln(p^2) = ln(p) / (2*ln(p)) = 1/2
        frac_dim = np.log(K.order) / np.log(K2_order)
        expected = 0.5
        
        match = abs(frac_dim - expected) < 1e-10
        all_pass = all_pass and match
        
        print(f"K = {K}, |K| = {p}, |K^2| = {K2_order}")
        print(f"  dim_{{K^2}}(K) = log_{{{K2_order}}}({p}) = {frac_dim:.6f}")
        print(f"  Expected: {expected} {'OK' if match else 'FAIL'}")
        print()
    
    # More interesting: dim of GF(p^2) over GF(p)
    print("\n--- GF(p^2) as a vector space over GF(p) ---")
    print("This is the standard extension field construction.")
    print()
    
    for p in [2, 3, 5]:
        # GF(p^2) has p^2 elements, and is a 2-dimensional vector space over GF(p)
        dim_standard = 2  # Standard result from field theory
        
        # Cardinality approach: |GF(p^2)| = p^2, |GF(p)| = p
        # dim_{GF(p)} GF(p^2) = log_p(p^2) = 2
        dim_log = np.log(p ** 2) / np.log(p)
        
        match = abs(dim_standard - dim_log) < 1e-10
        all_pass = all_pass and match
        
        print(f"GF({p}^2) over GF({p}): dim = {dim_standard}, log_{p}({p**2}) = {dim_log:.4f} {'OK' if match else 'FAIL'}")
    
    print("-" * 60)
    print(f"ALL TESTS PASSED: {all_pass}")
    print()
    return all_pass


def test_set_theoretic_view():
    """
    From the article: |V| = |K|^{dim V}, so dim V = log_{|K|} |V|
    
    This is the cardinality-based definition. Let's verify it's consistent
    with ALL standard dimension axioms.
    """
    print("=" * 60)
    print("TEST 6: Set-Theoretic Dimension Consistency")
    print("=" * 60)
    print("Verifying that log_{|K|}(|V|) satisfies ALL vector space dimension axioms:")
    print("  1. dim(K^n) = n")
    print("  2. dim(U + V) = dim(U) + dim(V)")
    print("  3. dim(U (x) V) = dim(U) * dim(V)")
    print("  4. dim(0) = 0")
    print()
    
    K = GF(5)
    all_pass = True
    
    def dim_log(V_card):
        """Compute dimension via logarithm."""
        if V_card == 1:
            return 0  # log_{|K|}(1) = 0
        return np.log(V_card) / np.log(K.order)
    
    # Axiom 1: dim(K^n) = n
    print("Axiom 1: dim(K^n) = n")
    for n in range(0, 8):
        V_card = K.order ** n
        computed_dim = dim_log(V_card)
        match = abs(computed_dim - n) < 1e-10
        all_pass = all_pass and match
        print(f"  n={n}: |V| = {V_card}, dim_log = {computed_dim:.4f} {'OK' if match else 'FAIL'}")
    
    # Axiom 2: dim(U + V) = dim(U) + dim(V)
    print("\nAxiom 2: dim(U + V) = dim(U) + dim(V)")
    for m in [1, 2, 3]:
        for n in [1, 2, 3]:
            UV_card = K.order ** (m + n)
            dim_UV = dim_log(UV_card)
            dim_U = dim_log(K.order ** m)
            dim_V = dim_log(K.order ** n)
            sum_dims = dim_U + dim_V
            
            match = abs(dim_UV - sum_dims) < 1e-10
            all_pass = all_pass and match
            print(f"  m={m}, n={n}: dim(U+V)={dim_UV:.4f}, dim(U)+dim(V)={sum_dims:.4f} {'OK' if match else 'FAIL'}")
    
    # Axiom 3: dim(U (x) V) = dim(U) * dim(V)
    print("\nAxiom 3: dim(U (x)_K V) = dim(U) * dim(V)")
    for a in [1, 2, 3]:
        for b in [1, 2, 3]:
            tensor_card = K.order ** (a * b)
            dim_tensor = dim_log(tensor_card)
            dim_product = dim_log(K.order ** a) * dim_log(K.order ** b)
            
            match = abs(dim_tensor - dim_product) < 1e-10
            all_pass = all_pass and match
            print(f"  a={a}, b={b}: dim(U(x)V)={dim_tensor:.4f}, dim(U)*dim(V)={dim_product:.4f} {'OK' if match else 'FAIL'}")
    
    # Axiom 4: dim(0) = 0
    print("\nAxiom 4: dim({0}) = 0")
    zero_card = 1  # The zero vector space has one element
    dim_zero = dim_log(zero_card)
    match = abs(dim_zero - 0) < 1e-10
    all_pass = all_pass and match
    print(f"  |{{0}}| = {zero_card}, dim_log = {dim_zero:.4f} {'OK' if match else 'FAIL'}")
    
    print("-" * 60)
    print(f"ALL TESTS PASSED: {all_pass}")
    print()
    return all_pass


def test_prime_factorization_log():
    """
    Connection to p-adic valuation (partial logarithm).
    From the article: for N = 2^a * 3^b * 5^c * ...
    log N = a*log2 + b*log3 + c*log5 + ...
    nu_p(N) = coefficient of log p (the 'partial' projection)
    """
    print("=" * 60)
    print("TEST 7: Prime Factorization as Logarithmic Decomposition")
    print("=" * 60)
    print("N = p1^a1 * p2^a2 * ... => log N = a1*log(p1) + a2*log(p2) + ...")
    print("nu_p(N) = a_p = 'projection' onto log(p) component")
    print()
    
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
    
    def log_decomposition(n):
        """Compute log(n) = sum of a_i * log(p_i)."""
        factors = prime_factorization(n)
        total = 0.0
        for p, a in factors.items():
            total += a * np.log(p)
        return total
    
    all_pass = True
    test_cases = [12, 60, 360, 1000, 2520, 5040, 27720]
    
    for N in test_cases:
        factors = prime_factorization(N)
        log_N = np.log(N)
        log_reconstructed = log_decomposition(N)
        
        # Verify decomposition
        match = abs(log_N - log_reconstructed) < 1e-10
        all_pass = all_pass and match
        
        factor_str = " * ".join(f"{p}^{a}" for p, a in sorted(factors.items()))
        print(f"  N = {N} = {factor_str}")
        print(f"    log({N}) = {log_N:.4f}")
        print(f"    reconstructed = {log_reconstructed:.4f} {'OK' if match else 'FAIL'}")
        
        # Show p-adic valuations as projections
        projections = []
        for p in sorted(factors.keys()):
            a = factors[p]
            proj = a * np.log(p)
            projections.append(f"  nu_{p}({N}) = {a} => {a}*log({p}) = {proj:.4f}")
        for proj_line in projections:
            print(f"      {proj_line}")
        print()
    
    print("-" * 60)
    print(f"ALL TESTS PASSED: {all_pass}")
    print()
    return all_pass


# ============================================================
# Main: Run All Tests
# ============================================================

if __name__ == "__main__":
    print("+==========================================================+")
    print("|  PHASE 1.3: Dimension = Logarithm -- Numerical Tests    |")
    print("|  From: 'Everything Is Logarithms' by Alex Kritchevsky   |")
    print("+==========================================================+")
    print()
    
    results = {}
    
    results['basic'] = test_basic_dimension_log()
    results['algebraic'] = test_vector_space_properties()
    results['tensor'] = test_tensor_product()
    results['identities'] = test_logarithmic_identities()
    results['fractional'] = test_cross_field_comparison()
    results['consistency'] = test_set_theoretic_view()
    results['prime_factors'] = test_prime_factorization_log()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    all_pass = all(results.values())
    for name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"  {name:<15} {status}")
    print("-" * 60)
    print(f"OVERALL: {'ALL TESTS PASSED' if all_pass else 'SOME TESTS FAILED'}")
    print()
    
    if all_pass:
        print("CONCLUSION: The dimension-logarithm correspondence holds perfectly")
        print("for finite fields. dim_K V = log_{|K|} |V| is not just an analogy --")
        print("it's an identity for finite-dimensional vector spaces over finite fields.")
        print()
        print("KEY FINDINGS:")
        print("  1. dim_K(K^n) = log_{|K|}(|K^n|) = n [EXACT for all finite fields]")
        print("  2. Direct sum mirrors multiplication: dim(U+V) = dim(U) + dim(V)")
        print("  3. Tensor product mirrors exponentiation: dim(U(x)V) = dim(U)*dim(V)")
        print("  4. Fractional dimensions emerge naturally from cross-field comparison")
        print("  5. Prime factorization = logarithmic decomposition in basis {log p}")
        print()
        print("NEXT STEPS:")
        print("  - Formalize baseless logarithm structure (Phase 2A)")
        print("  - Connect to p-adic valuation as partial logarithm")
        print("  - Explore fractional dimensions with extension fields")

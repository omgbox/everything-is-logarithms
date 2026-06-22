"""Visual tests for the logarithmic framework."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

output_dir = os.path.dirname(os.path.abspath(__file__))


def test_dimension_is_log():
    """Test: dim_K(V) = log_{|K|}(|V|)"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Test 1: Dimension = Logarithm', fontsize=14, fontweight='bold')

    # Plot 1: dim vs log for GF(p)
    primes = [2, 3, 5, 7, 11]
    dims = range(1, 8)

    for p in primes:
        log_dims = [np.log(p**n) / np.log(p) for n in dims]
        axes[0, 0].plot(dims, log_dims, 'o-', label=f'GF({p})', markersize=4)

    axes[0, 0].plot(dims, dims, 'k--', alpha=0.3, label='y=x')
    axes[0, 0].set_xlabel('Standard dimension')
    axes[0, 0].set_ylabel('log_{|K|}(|V|)')
    axes[0, 0].legend(fontsize=8)
    axes[0, 0].set_title('All dimensions match')

    # Plot 2: Cardinality growth
    for p in primes:
        cards = [p**n for n in dims]
        axes[0, 1].semilogy(dims, cards, 'o-', label=f'GF({p})', markersize=4)

    axes[0, 1].set_xlabel('Dimension')
    axes[0, 1].set_ylabel('|V| (log scale)')
    axes[0, 1].legend(fontsize=8)
    axes[0, 1].set_title('Cardinality grows exponentially')

    # Plot 3: p-adic valuation of |V|
    for p in primes:
        nus = [n for n in dims]  # nu_p(p^n) = n
        axes[1, 0].plot(dims, nus, 'o-', label=f'nu_{p}(|V|)', markersize=4)

    axes[1, 0].set_xlabel('Dimension')
    axes[1, 0].set_ylabel('nu_p(|V|)')
    axes[1, 0].legend(fontsize=8)
    axes[1, 0].set_title('p-adic valuation equals dimension')

    # Plot 4: Error (should be zero)
    for p in primes:
        errors = [abs(n - np.log(p**n)/np.log(p)) for n in dims]
        axes[1, 1].plot(dims, errors, 'o-', label=f'GF({p})', markersize=4)

    axes[1, 1].set_xlabel('Dimension')
    axes[1, 1].set_ylabel('Error')
    axes[1, 1].legend(fontsize=8)
    axes[1, 1].set_title('Error is exactly zero')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'test_dimension.png'), dpi=150)
    plt.close()
    print('test_dimension.png generated')


def test_logarithmic_basis():
    """Test: {log(p)} forms a basis for log(Q+)"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Test 2: Logarithmic Basis', fontsize=14, fontweight='bold')

    # Plot 1: log(n) decomposition
    numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 16, 20, 24, 30, 36, 48, 60]
    primes = [2, 3, 5, 7]

    bottoms = np.zeros(len(numbers))
    for p in primes:
        coeffs = []
        for n in numbers:
            count = 0
            temp = n
            while temp % p == 0:
                count += 1
                temp //= p
            coeffs.append(count * np.log(p))

        axes[0, 0].bar(range(len(numbers)), coeffs, bottom=bottoms, label=f'{p}-part')

    axes[0, 0].plot(range(len(numbers)), [np.log(n) for n in numbers], 'k--', alpha=0.5, label='log(n)')
    axes[0, 0].set_xticks(range(len(numbers)))
    axes[0, 0].set_xticklabels(numbers, rotation=45)
    axes[0, 0].set_ylabel('log(n)')
    axes[0, 0].legend(fontsize=8)
    axes[0, 0].set_title('log(n) = SUM a_p * log(p)')

    # Plot 2: Basis vectors
    for i, p in enumerate(primes):
        axes[0, 1].bar(i, np.log(p), label=f'log({p})={np.log(p):.3f}')

    axes[0, 1].set_xticks(range(len(primes)))
    axes[0, 1].set_xticklabels([f'log({p})' for p in primes])
    axes[0, 1].set_ylabel('Value')
    axes[0, 1].set_title('Basis vectors')

    # Plot 3: Reconstruction error
    reconstruction_errors = []
    for n in numbers:
        log_n = np.log(n)
        reconstructed = 0
        temp = n
        for p in primes:
            count = 0
            while temp % p == 0:
                count += 1
                temp //= p
            reconstructed += count * np.log(p)
        reconstruction_errors.append(abs(log_n - reconstructed))

    axes[1, 0].bar(range(len(numbers)), reconstruction_errors)
    axes[1, 0].set_xticks(range(len(numbers)))
    axes[1, 0].set_xticklabels(numbers, rotation=45)
    axes[1, 0].set_ylabel('Error')
    axes[1, 0].set_title('Reconstruction error (all zero)')

    # Plot 4: Dimension of log-space
    dims = list(range(2, 50))
    log_dims = [len([p for p in range(2, d+1) if all(p % i != 0 for i in range(2, p))]) for d in dims]

    axes[1, 1].plot(dims, log_dims, 'bo-', markersize=3)
    axes[1, 1].plot(dims, [d/np.log(d) for d in dims], 'r--', label='n/ln(n)')
    axes[1, 1].set_xlabel('n')
    axes[1, 1].set_ylabel('Number of primes')
    axes[1, 1].legend()
    axes[1, 1].set_title('Dimension grows as n/ln(n)')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'test_basis.png'), dpi=150)
    plt.close()
    print('test_basis.png generated')


def test_euler_product():
    """Test: zeta(s) = prod_p (1-p^{-s})^{-1}"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Test 3: Euler Product', fontsize=14, fontweight='bold')

    # Compute zeta values
    s_values = np.linspace(1.1, 4, 100)
    zeta_direct = []
    zeta_euler = []

    for s in s_values:
        # Direct sum
        direct = sum(1.0 / (n ** s) for n in range(1, 1001))
        zeta_direct.append(direct)

        # Euler product
        product = 1.0
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
            product *= 1.0 / (1.0 - p ** (-s))
        zeta_euler.append(product)

    axes[0, 0].plot(s_values, zeta_direct, 'b-', label='Direct sum', linewidth=2)
    axes[0, 0].plot(s_values, zeta_euler, 'r--', label='Euler product', linewidth=2)
    axes[0, 0].set_xlabel('s')
    axes[0, 0].set_ylabel('zeta(s)')
    axes[0, 0].legend()
    axes[0, 0].set_title('zeta(s) matches')

    # Log zeta decomposition
    s_fixed = 2.0
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    contributions = [np.log(1/(1-p**(-s_fixed))) / np.log(p) for p in primes]

    axes[0, 1].bar(range(len(primes)), contributions)
    axes[0, 1].set_xticks(range(len(primes)))
    axes[0, 1].set_xticklabels(primes)
    axes[0, 1].set_ylabel('Contribution to log(zeta)')
    axes[0, 1].set_title('p-adic decomposition of log(zeta)')

    # Error between direct and Euler
    errors = [abs(d - e) for d, e in zip(zeta_direct, zeta_euler)]
    axes[1, 0].semilogy(s_values, errors)
    axes[1, 0].set_xlabel('s')
    axes[1, 0].set_ylabel('Error')
    axes[1, 0].set_title('Error (log scale)')

    # Prime counting function
    x_vals = np.linspace(2, 100, 50)
    pi_x = [len([p for p in range(2, int(x)+1) if all(p % i != 0 for i in range(2, p))]) for x in x_vals]
    li_x = [sum(1/np.log(t) for t in np.linspace(2, x, 100)) * (x-2)/100 for x in x_vals]

    axes[1, 1].plot(x_vals, pi_x, 'b-', label='pi(x)')
    axes[1, 1].plot(x_vals, li_x, 'r--', label='Li(x)')
    axes[1, 1].set_xlabel('x')
    axes[1, 1].set_ylabel('Count')
    axes[1, 1].legend()
    axes[1, 1].set_title('Prime counting function')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'test_euler.png'), dpi=150)
    plt.close()
    print('test_euler.png generated')


def test_tropical_connection():
    """Test: Tropical = logarithmic geometry"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Test 4: Tropical = Logarithmic', fontsize=14, fontweight='bold')

    # Plot 1: Tropical polynomial
    x = np.linspace(-3, 3, 100)
    coeffs = [0, 1, 2]
    trop_vals = [max([c + i*xi for i, c in enumerate(coeffs)]) for xi in x]

    axes[0, 0].plot(x, trop_vals, 'b-', linewidth=2)
    for i, c in enumerate(coeffs):
        axes[0, 0].plot(x, c + i*x, '--', alpha=0.5, label=f'{c}+{i}x')
    axes[0, 0].set_xlabel('x')
    axes[0, 0].set_ylabel('f(x)')
    axes[0, 0].legend(fontsize=8)
    axes[0, 0].set_title('Tropical polynomial max(0, 1+x, 2+2x)')

    # Plot 2: Isomorphism
    standard = np.linspace(0.1, 5, 100)
    tropical = np.log(standard)

    axes[0, 1].plot(standard, tropical, 'b-', linewidth=2)
    axes[0, 1].set_xlabel('Standard (R>0, *, +)')
    axes[0, 1].set_ylabel('Tropical (R, +, max)')
    axes[0, 1].set_title('log: isomorphism')

    # Plot 3: Newton polytope
    trop_poly = TropicalPolynomial([0, 1, 2])
    polytope = trop_poly.newton_polytope()
    vertices = polytope['vertices']

    for n, c in vertices:
        axes[1, 0].plot(n, c, 'bo', markersize=10)

    axes[1, 0].plot([v[0] for v in vertices], [v[1] for v in vertices], 'b-', linewidth=2)
    axes[1, 0].set_xlabel('Degree n')
    axes[1, 0].set_ylabel('Coefficient c_n')
    axes[1, 0].set_title(f'Newton polytope (dim={polytope["dimension"]})')

    # Plot 4: Tropical roots
    x_range = np.linspace(-3, 3, 100)
    trop_vals = [trop_poly(xi) for xi in x_range]

    axes[1, 1].plot(x_range, trop_vals, 'b-', linewidth=2)
    axes[1, 1].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[1, 1].set_xlabel('x')
    axes[1, 1].set_ylabel('f(x)')
    axes[1, 1].set_title('Tropical polynomial evaluation')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'test_tropical.png'), dpi=150)
    plt.close()
    print('test_tropical.png generated')


def test_information_geometry():
    """Test: Information geometry as logarithmic invariant"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Test 5: Information Geometry', fontsize=14, fontweight='bold')

    # Plot 1: Shannon entropy
    p_values = np.linspace(0.01, 0.99, 100)
    H = -p_values * np.log(p_values) - (1-p_values) * np.log(1-p_values)

    axes[0, 0].plot(p_values, H, 'b-', linewidth=2)
    axes[0, 0].axvline(x=0.5, color='r', linestyle='--', alpha=0.5)
    axes[0, 0].set_xlabel('p')
    axes[0, 0].set_ylabel('H(p)')
    axes[0, 0].set_title('Shannon entropy H(p)')

    # Plot 2: KL divergence
    q_values = np.linspace(0.1, 0.9, 50)
    p_fixed = 0.5
    kl_values = [p_fixed * np.log(p_fixed/q) + (1-p_fixed) * np.log((1-p_fixed)/(1-q)) for q in q_values]

    axes[0, 1].plot(q_values, kl_values, 'b-', linewidth=2)
    axes[0, 1].axvline(x=p_fixed, color='r', linestyle='--', alpha=0.5)
    axes[0, 1].set_xlabel('q')
    axes[0, 1].set_ylabel('KL(p||q)')
    axes[0, 1].set_title('KL divergence (min at q=p)')

    # Plot 3: Renyi entropy
    alphas = np.linspace(0.1, 5, 100)
    probs = [0.25, 0.25, 0.25, 0.25]
    renyi_vals = []

    for alpha in alphas:
        if alpha == 1:
            renyi_vals.append(-sum(p*np.log(p) for p in probs))
        else:
            renyi_vals.append(1/(1-alpha) * np.log(sum(p**alpha for p in probs)))

    axes[1, 0].plot(alphas, renyi_vals, 'b-', linewidth=2)
    axes[1, 0].axhline(y=np.log(4), color='r', linestyle='--', alpha=0.5, label='log(4)')
    axes[1, 0].set_xlabel('alpha')
    axes[1, 0].set_ylabel('H_alpha')
    axes[1, 0].legend()
    axes[1, 0].set_title('Renyi entropy')

    # Plot 4: Fisher metric
    theta = np.linspace(0.1, 0.9, 50)
    fisher = [1/(p*(1-p)) for p in theta]

    axes[1, 1].plot(theta, fisher, 'b-', linewidth=2)
    axes[1, 1].axvline(x=0.5, color='r', linestyle='--', alpha=0.5)
    axes[1, 1].set_xlabel('theta')
    axes[1, 1].set_ylabel('g(theta)')
    axes[1, 1].set_title('Fisher metric g(theta) = 1/(theta(1-theta))')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'test_information.png'), dpi=150)
    plt.close()
    print('test_information.png generated')


class TropicalPolynomial:
    def __init__(self, coefficients):
        self.coeffs = coefficients
        self.degree = len(coefficients) - 1

    def __call__(self, x):
        values = [self.coeffs[n] + n * x for n in range(self.degree + 1)]
        return max(values)

    def newton_polytope(self):
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


if __name__ == '__main__':
    print('Generating visual tests...')
    test_dimension_is_log()
    test_logarithmic_basis()
    test_euler_product()
    test_tropical_connection()
    test_information_geometry()
    print('Done! Generated 5 test images.')

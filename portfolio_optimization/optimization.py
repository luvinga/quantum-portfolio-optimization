# portfolio.py
"""
Quantum/Classical Portfolio Optimization Example
- Classical portfolio optimization (maximize Sharpe ratio using SciPy)
- Efficient frontier sampling (random portfolios)
- Hybrid variational-quantum approach (PennyLane qnode -> classical optimizer)
Dataset: AAPL, AMZN, MSFT
Author: Adapted for user (Dr. Haydock example)
"""

import numpy as np
import pennylane as qml
from pennylane import numpy as pnp
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------
# Historical / optional data (example)
# ---------------------------
expected_returns = np.array([
    0.252301,  # AAPL  0.2387279121  normal historical returns, switch them when running the code
    1.734270,  # AMZN   0.2109370274
    2.186572   # MSFT   0.2461092841
])
tickers = ["AAPL", "AMZN", "MSFT"]

# Covariance matrix (replace zeros with real covariances if available)
cov_matrix = np.array([
    [0.3270924763**2, 0.002, 0.001],
    [0.002, 0.3575668869**2, 0.0015],
    [0.001, 0.0015, 0.2981741969**2]
])

num_assets = len(expected_returns)
print(f"Using {num_assets} assets: {tickers}")

# ---------------------------
# Utility functions
# ---------------------------
def portfolio_return(weights, returns):
    return np.dot(weights, returns)

def portfolio_risk(weights, cov):
    return np.sqrt(np.dot(weights.T, np.dot(cov, weights)))

def asset_std_contribution(weights, cov):
    contributions = weights * np.dot(cov, weights)
    return np.sqrt(contributions), np.sqrt(np.dot(weights.T, np.dot(cov, weights)))

def sharpe_ratio(weights, returns, cov, risk_free=0.0):
    port_r = portfolio_return(weights, returns)
    port_sd = portfolio_risk(weights, cov)
    if port_sd == 0:
        return 0.0
    return (port_r - risk_free) / port_sd

# ---------------------------
# Classical optimization (maximize Sharpe)
# ---------------------------
def classical_optimize_max_sharpe(returns, cov):
    cons = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    bounds = tuple((0, 1) for _ in range(len(returns)))
    x0 = np.ones(len(returns)) / len(returns)

    def neg_sharpe(w):
        return -sharpe_ratio(w, returns, cov)

    res = minimize(neg_sharpe, x0, method='SLSQP', bounds=bounds, constraints=cons)
    if not res.success:
        print("Classical optimization failed:", res.message)
    w_opt = res.x
    return w_opt, sharpe_ratio(w_opt, returns, cov), portfolio_return(w_opt, returns), portfolio_risk(w_opt, cov)

w_classical, sr_classical, r_classical, sd_classical = classical_optimize_max_sharpe(expected_returns, cov_matrix)
asset_std_classical, total_std_classical = asset_std_contribution(w_classical, cov_matrix)

print("\nClassical optimization (max Sharpe) results:")
for i, t in enumerate(tickers):
    print(f"  {t}: weight = {w_classical[i]:.4f}, contribution to risk = {asset_std_classical[i]:.6f}")
print(f"  Portfolio return = {r_classical:.6f}, risk (std) = {total_std_classical:.6f}, Sharpe = {sr_classical:.6f}")

# ---------------------------
# Random portfolio sampling (efficient frontier)
# ---------------------------
def sample_random_portfolios(returns, cov, n_portfolios=10000, seed=42):
    rng = np.random.default_rng(seed)
    n = len(returns)
    results = np.zeros((n_portfolios, 3))  # return, risk, sharpe
    weights_record = np.zeros((n_portfolios, n))
    for i in range(n_portfolios):
        w = rng.random(n)
        w /= np.sum(w)
        weights_record[i] = w
        r = portfolio_return(w, returns)
        sd = portfolio_risk(w, cov)
        sr = r / sd if sd > 0 else 0.0
        results[i] = [r, sd, sr]
    return results, weights_record

results, weights_record = sample_random_portfolios(expected_returns, cov_matrix)
best_idx = np.argmax(results[:, 2])
best_weights_random = weights_record[best_idx]
best_return_random, best_risk_random, best_sharpe_random = results[best_idx]
asset_std_random, total_std_random = asset_std_contribution(best_weights_random, cov_matrix)

print("\nBest random-sampled portfolio (by Sharpe):")
for i, t in enumerate(tickers):
    print(f"  {t}: weight = {best_weights_random[i]:.4f}, contribution to risk = {asset_std_random[i]:.6f}")
print(f"  Return = {best_return_random:.6f}, risk (std) = {total_std_random:.6f}, Sharpe = {best_sharpe_random:.6f}")

# Plot efficient frontier
plt.figure(figsize=(8, 5))
sc = plt.scatter(results[:, 1], results[:, 0], c=results[:, 2], cmap="viridis", s=6)
plt.colorbar(sc, label="Sharpe Ratio")
plt.scatter([sd_classical], [r_classical], color="red", marker="*", s=120, label="Classical opt")
plt.scatter([best_risk_random], [best_return_random], color="orange", marker="D", s=80, label="Random best")
plt.xlabel("Risk (Std Dev)")
plt.ylabel("Return")
plt.title("Efficient Frontier (random sampling)")
plt.legend()
plt.tight_layout()
plt.show()

# ---------------------------
# Quantum variational approach (PennyLane)
# ---------------------------
dev = qml.device("default.qubit", wires=num_assets)

def variational_layer(gammas, betas):
    for i in range(num_assets):
        qml.RX(gammas[i], wires=i)
    for i in range(num_assets - 1):
        qml.CNOT(wires=[i, i+1])
        qml.RZ(gammas[i] * gammas[i+1], wires=i+1)
        qml.CNOT(wires=[i, i+1])
    for i in range(num_assets):
        qml.RY(betas[i], wires=i)

@qml.qnode(dev, interface='autograd')
def qnode(params):
    gammas = params[:num_assets]
    betas = params[num_assets:]
    for i in range(num_assets):
        qml.Hadamard(wires=i)
    variational_layer(gammas, betas)
    return [qml.expval(qml.PauliZ(i)) for i in range(num_assets)]

def qnode_probs_from_params(params):
    z_expect = pnp.array(qnode(params))
    probs = (1.0 - z_expect) / 2.0
    probs = pnp.clip(probs, 1e-8, None)
    probs = probs / pnp.sum(probs)
    return probs

def quantum_cost(params, returns=expected_returns, cov=cov_matrix, lam=1.0):
    probs = qnode_probs_from_params(params)
    port_r = pnp.dot(probs, returns)
    port_var = pnp.dot(probs.T, pnp.dot(cov, probs))
    return port_var - lam * port_r

# Initialize variational params
init_params = 0.1 * np.random.randn(2 * num_assets)
params = pnp.array(init_params, requires_grad=True)
opt = qml.AdamOptimizer(stepsize=0.2)
n_steps = 500
lam = 1.0

print("\nStarting hybrid quantum-classical optimization...")
for step in range(n_steps):
    params, cost_val = opt.step_and_cost(lambda v: quantum_cost(v, lam=lam), params)
    if (step + 1) % 50 == 0 or step == 0:
        probs = np.array(qnode_probs_from_params(params))
        r = portfolio_return(probs, expected_returns)
        sd = portfolio_risk(probs, cov_matrix)
        sr = r / sd if sd > 0 else 0.0
        print(f"Step {step+1:3d}: cost={cost_val:.6f}, return={r:.6f}, risk={sd:.6f}, sharpe={sr:.6f}")

final_probs = np.array(qnode_probs_from_params(params))
final_return = portfolio_return(final_probs, expected_returns)
final_risk = portfolio_risk(final_probs, cov_matrix)
final_sharpe = final_return / final_risk if final_risk > 0 else 0.0
asset_std_quantum, total_std_quantum = asset_std_contribution(final_probs, cov_matrix)

print("\nQuantum variational portfolio result:")
for i, t in enumerate(tickers):
    print(f"  {t}: weight = {final_probs[i]:.4f}, contribution to risk = {asset_std_quantum[i]:.6f}")
print(f"  Portfolio return = {final_return:.6f}, risk (std) = {total_std_quantum:.6f}, Sharpe = {final_sharpe:.6f}")

# Comparison
print("\nComparison summary (Classical vs Random vs Quantum):")
for i, t in enumerate(tickers):
    print(f"  {t} | classical = {w_classical[i]:.4f}  | random = {best_weights_random[i]:.4f}  | quantum = {final_probs[i]:.4f}")
print(f"\nPortfolio risk (std) | Classical = {total_std_classical:.6f}, Random = {total_std_random:.6f}, Quantum = {total_std_quantum:.6f}")

# ---------------------------
# Plot asset-level risk contributions
# ---------------------------
x = np.arange(len(tickers))  # asset positions
width = 0.25  # width of bars

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(x - width, asset_std_classical, width, label='Classical', color='skyblue')
ax.bar(x, asset_std_random, width, label='Random', color='orange')
ax.bar(x + width, asset_std_quantum, width, label='Quantum', color='lightgreen')

ax.set_xticks(x)
ax.set_xticklabels(tickers)
ax.set_ylabel("Risk Contribution (Std Dev)")
ax.set_title("Asset-level Risk Contributions by Portfolio Type")
ax.legend()
plt.tight_layout()
plt.show()

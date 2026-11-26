# monte_carlo_MSFT_updated.py
import pennylane as qml
from pennylane import numpy as np
import numpy as onp
import matplotlib.pyplot as plt

# -------------------------
# 1) Market / simulation parameters
# -------------------------
S0 = 12.80789905      # MSFT initial price
mu = 0.2461092841
sigma = 0.2981741969

T = 1.0
N = 252
dt = T / N
n_sims = 10000
r = 0.05
discount_per_step = onp.exp(-r * dt)
K = 15.0               # strike

# -------------------------
# 2) Classical GBM Monte Carlo
# -------------------------
prices = onp.zeros((n_sims, N+1))
prices[:, 0] = S0
rng = onp.random.default_rng(42)

for t in range(1, N+1):
    Z = rng.normal(size=n_sims)
    prices[:, t] = prices[:, t-1] * onp.exp((mu - 0.5 * sigma**2)*dt + sigma * onp.sqrt(dt) * Z)

# -------------------------
# 3) American put payoff and Longstaff-Schwartz
# -------------------------
def american_put_payoff(S, K):
    return onp.maximum(K - S, 0.0)

def price_american_option_LS(paths, strike, discount_per_step):
    sims, steps_plus1 = paths.shape
    steps = steps_plus1 - 1
    cashflows = american_put_payoff(paths[:, -1], strike)

    for t in range(steps-1, 0, -1):
        itm_idx = onp.where(american_put_payoff(paths[:, t], strike) > 0)[0]
        if len(itm_idx) == 0:
            cashflows *= discount_per_step
            continue

        X = paths[itm_idx, t]
        Y = cashflows[itm_idx] * discount_per_step

        # linear regression using lstsq for stability
        A = onp.vstack([X, onp.ones_like(X)]).T
        coeff, _, _, _ = onp.linalg.lstsq(A, Y, rcond=None)
        continuation = coeff[0] * X + coeff[1]

        immediate = american_put_payoff(X, strike)
        exercise_mask = immediate > continuation

        cashflows[itm_idx[exercise_mask]] = immediate[exercise_mask]
        cashflows[itm_idx[~exercise_mask]] *= discount_per_step

        not_itm = onp.setdiff1d(onp.arange(sims), itm_idx)
        if len(not_itm) > 0:
            cashflows[not_itm] *= discount_per_step

    return onp.mean(cashflows) * discount_per_step

classical_price = price_american_option_LS(prices, K, discount_per_step)

# -------------------------
# 4) Quantum-inspired estimator (toy)
# -------------------------
def payoff_to_theta(p_norm):
    p = onp.clip(p_norm, 0.0, 1.0)
    return 2.0 * onp.arcsin(onp.sqrt(p))

def quantum_estimate_mean_payoff(payoffs, shots_per_payoff=1000):
    p_min, p_max = payoffs.min(), payoffs.max()
    if p_max == p_min:
        return payoffs[0] * onp.exp(-r*T)
    p_norm = (payoffs - p_min)/(p_max - p_min)
    dev = qml.device("default.qubit", wires=1, shots=shots_per_payoff)

    @qml.qnode(dev)
    def ancilla(theta):
        qml.RY(theta, wires=0)
        return qml.sample(qml.PauliZ(0))

    probs = []
    for pn in p_norm:
        theta = payoff_to_theta(pn)
        samples = ancilla(theta)
        prob_one = onp.mean((1 - samples)/2.0)
        probs.append(prob_one)

    payoff_estimates = p_min + onp.array(probs)*(p_max - p_min)
    mean_payoff = onp.mean(payoff_estimates)
    return mean_payoff * onp.exp(-r*T)

payoff_at_maturity = american_put_payoff(prices[:, -1], K)
quantum_price = quantum_estimate_mean_payoff(payoff_at_maturity, shots_per_payoff=1000)

# -------------------------
# 5) Results
# -------------------------
print("MSFT American Put Price:")
print(f"  Classical LS: {classical_price:.6f}")
print(f"  Quantum-inspired: {quantum_price:.6f}")

# Monte Carlo paths plot
plt.figure(figsize=(10,5))
for i in range(10):
    plt.plot(prices[i, :], alpha=0.6)
plt.title("Monte Carlo Sample Paths for MSFT")
plt.xlabel("Time Step")
plt.ylabel("Price")
plt.grid(alpha=0.3)
plt.show()

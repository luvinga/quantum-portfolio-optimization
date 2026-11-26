
# Quantum Option Pricing & Portfolio Optimization

## Overview

This research project explores the application of quantum computing to financial derivative pricing and portfolio optimization.

The project compares classical computational methods with quantum-inspired and hybrid quantum-classical approaches using three major technology stocks: Apple (AAPL), Amazon (AMZN), and Microsoft (MSFT).

Completed as a Quantum Computing research project at St. Olaf College in Fall 2025.

## Research Objectives

- Model American put options using Monte Carlo simulations.
- Explore quantum-inspired methods for estimating option payoffs.
- Compare classical and variational quantum portfolio optimization.
- Investigate the effects of input scaling on portfolio allocation.
- Evaluate the limitations of quantum computing in financial applications.

## Technologies

- Python
- PennyLane
- NumPy
- SciPy
- Matplotlib

## Methodology

### 1. Option Pricing

- Geometric Brownian Motion (GBM)
- Longstaff-Schwartz Monte Carlo
- 10,000 simulated price paths per asset
- 252 simulation time steps
- Single-qubit payoff encoding and sampling

### 2. Portfolio Optimization

- Classical Sharpe ratio maximization using SciPy
- Random sampling of 10,000 portfolios
- Hybrid variational quantum circuits
- Adam optimization over 500 iterations
- Risk and return analysis

## Experimental Results

### Option Pricing

| Asset | Classical Estimate | Quantum-Inspired Estimate |
|-------|-------------------:|---------------------------:|
| AAPL  | 0.2523 | 0.2061 |
| AMZN  | 1.7343 | 1.3177 |
| MSFT  | 2.1866 | 1.1788 |

### Portfolio Allocation

Historical-return experiment:

| Asset | Classical | Random Sampling | Quantum Variational |
|-------|----------:|----------------:|--------------------:|
| AAPL  | 33.60% | 34.02% | 35.17% |
| AMZN  | 24.45% | 24.34% | 18.12% |
| MSFT  | 41.95% | 41.64% | 46.71% |

## Key Findings

- Classical and quantum-inspired methods produced different payoff estimates.
- Historical return inputs resulted in more diversified experimental portfolios.
- Using unscaled option prices as return inputs caused excessive portfolio concentration.
- Input selection and normalization significantly influenced optimization results.

## Limitations

This project is an exploratory academic study.

- Quantum circuits were executed on classical simulators rather than physical quantum hardware.
- The payoff estimator uses quantum circuit sampling rather than full Quantum Amplitude Estimation.
- The quantum-inspired payoff estimator evaluates maturity payoffs without modeling early exercise.
- Some covariance inputs are illustrative.
- The pricing scripts use experimental initial values rather than verified underlying stock prices.
- Classical and variational optimizers use different objective functions.
- No computational quantum advantage is claimed.

The results are reported from the original research paper and are not intended as financial advice.

## Acknowledgments

This project was completed as part of the Quantum Computing course at St. Olaf College.

The portfolio optimization implementation was adapted from instructional examples provided by Dr. Michael Haydock.

## Author

Luvinga Kahise

Computer Science & Quantitative Economics
St. Olaf College

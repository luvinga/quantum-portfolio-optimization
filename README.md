
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

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| PennyLane | Quantum circuit simulation and optimization |
| NumPy | Numerical computing and matrix operations |
| SciPy | Classical portfolio optimization |
| Matplotlib | Data visualization |
| Pandas | Imported data analysis library |

## Repository Structure

```
quantum-portfolio-optimization/
├── option_pricing/
│   ├── monte_carlo_aapl.py
│   ├── monte_carlo_amzn.py
│   └── monte_carlo_msft.py
├── portfolio_optimization/
│   └── optimization.py
├── research/
│   └── Quantum_Pricing_and_Optimization_Paper.pdf
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Usage

### Prerequisites

- Python 3
- Git
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/luvinga/quantum-portfolio-optimization.git
cd quantum-portfolio-optimization
```

### 2. Create a Virtual Environment

For macOS and Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

For Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run Option Pricing Simulations

Apple (AAPL):

```bash
python option_pricing/monte_carlo_aapl.py
```

Amazon (AMZN):

```bash
python option_pricing/monte_carlo_amzn.py
```

Microsoft (MSFT):

```bash
python option_pricing/monte_carlo_msft.py
```

Each simulation generates stock price paths, calculates classical and quantum-inspired payoff estimates, and displays Monte Carlo simulation visualizations.

The quantum-inspired sampling process may take several minutes depending on the computing environment.

### 5. Run Portfolio Optimization

```bash
python portfolio_optimization/optimization.py
```

The optimization script generates:

- Classical portfolio allocations
- Randomly sampled portfolio allocations
- Quantum variational portfolio allocations
- Risk and return estimates
- Sharpe ratio comparisons
- Risk-return visualizations
- Asset-level risk visualizations

The original optimization script defaults to option-price inputs. Historical expected returns can be substituted using the values documented in the source code.

## Dataset

The original research uses historical daily adjusted closing prices for three technology stocks:

| Company | Ticker |
|---------|--------|
| Apple | AAPL |
| Amazon | AMZN |
| Microsoft | MSFT |

Historical data period: January 1, 2020 – October 31, 2025.

The historical data was used to derive expected returns, volatility, and other financial parameters.

### Historical Asset Parameters

| Asset | Expected Return | Volatility |
|-------|----------------:|-----------:|
| AAPL | 0.2387 | 0.3271 |
| AMZN | 0.2109 | 0.3576 |
| MSFT | 0.2461 | 0.2982 |

The supplied Python scripts use predefined numerical parameters rather than loading the original historical dataset directly.

## Methodology

### 1. Classical Option Pricing

The classical option pricing component uses Geometric Brownian Motion (GBM) to simulate potential future asset price movements.

The Longstaff-Schwartz Monte Carlo algorithm estimates American put option values by comparing immediate exercise payoffs with estimated continuation values.

Simulation configuration:

| Parameter | Value |
|-----------|------:|
| Number of assets | 3 |
| Simulated paths per asset | 10,000 |
| Total simulated price paths | 30,000 |
| Time steps per path | 252 |
| Simulation horizon | 1 year |
| Experimental strike price | 15.0 |
| Discount rate | 5% |
| Random seed | 42 |

### 2. Quantum-Inspired Option Pricing

The quantum-inspired component uses PennyLane to estimate expected maturity payoffs through simulated quantum circuits.

The implementation includes:

- Payoff normalization
- Single-qubit amplitude encoding
- RY rotation gates
- Pauli-Z measurements
- Repeated quantum circuit sampling
- Discounted expected payoff estimation

The estimator uses 1,000 measurement shots per payoff when the payoff distribution is nonconstant.

This implementation demonstrates quantum-inspired payoff estimation rather than a complete Quantum Amplitude Estimation (QAE) algorithm.

### 3. Classical Portfolio Optimization

Classical portfolio optimization is implemented using SciPy's Sequential Least Squares Programming (SLSQP) optimizer.

The objective is to maximize the portfolio Sharpe ratio while maintaining the following constraints:

- Portfolio weights must sum to one.
- Individual asset weights must remain between zero and one.
- Short selling is not included.

The implementation evaluates expected portfolio returns, volatility, and asset-level risk.

### 4. Random Portfolio Sampling

A total of 10,000 randomly generated portfolios are evaluated to explore the portfolio risk-return space.

Each portfolio is evaluated using:

- Expected return
- Portfolio volatility
- Sharpe ratio
- Asset allocation weights

The results provide a visual comparison with the classical optimization solution.

### 5. Hybrid Quantum-Classical Optimization

The variational quantum optimization component uses PennyLane's quantum simulator to generate portfolio allocation weights.

The implementation includes:

- Three-qubit quantum circuits
- Hadamard gates
- RX, RY, and RZ rotation gates
- CNOT entangling gates
- Pauli-Z expectation values
- Mean-variance cost function
- Adam optimization

The variational circuit is optimized over 500 iterations to explore portfolio allocations that balance expected returns and risk.

## Experimental Results

The following results are reported from the original Fall 2025 research paper.

### 1. Option Pricing Results

| Asset | Classical Estimate | Quantum-Inspired Estimate |
|-------|-------------------:|---------------------------:|
| AAPL | 0.2523 | 0.2061 |
| AMZN | 1.7343 | 1.3177 |
| MSFT | 2.1866 | 1.1788 |

The classical and quantum-inspired methods produced different payoff estimates.

An important distinction is that the classical Longstaff-Schwartz implementation accounts for early exercise, while the quantum-inspired estimator evaluates maturity payoffs.

Consequently, the two methods do not estimate identical exercise conditions.

### 2. Portfolio Allocation Using Historical Returns

| Asset | Classical | Random Sampling | Quantum Variational |
|-------|----------:|----------------:|--------------------:|
| AAPL | 33.60% | 34.02% | 35.17% |
| AMZN | 24.45% | 24.34% | 18.12% |
| MSFT | 41.95% | 41.64% | 46.71% |

The historical-return experiment produced diversified allocations across all three assets.

Reported quantum variational portfolio metrics:

| Metric | Approximate Result |
|--------|-------------------:|
| Expected return | 0.237 |
| Portfolio volatility | 0.194 |
| Sharpe ratio | 1.22 |

### 3. Portfolio Allocation Using Option-Price Inputs

| Asset | Classical | Random Sampling | Quantum Variational |
|-------|----------:|----------------:|--------------------:|
| AAPL | 4.76% | 5.05% | 0.00% |
| AMZN | 33.55% | 32.91% | 0.00% |
| MSFT | 61.69% | 62.04% | 100.00% |

Using raw option prices as return inputs produced significantly more concentrated allocations.

The variational optimizer allocated the entire experimental portfolio to Microsoft under this configuration.

This experiment highlights the importance of consistent financial inputs, appropriate objective functions, and input scaling.

Raw option prices should not be interpreted as expected investment returns.

## Visualizations

The Python scripts generate several research visualizations:

- Monte Carlo simulated price paths for AAPL
- Monte Carlo simulated price paths for AMZN
- Monte Carlo simulated price paths for MSFT
- Random portfolio risk-return distributions
- Classical and random portfolio optimization comparisons
- Asset-level risk comparisons

Additional visualizations are available in the full research paper.

## Key Findings

- Classical and quantum-inspired methods produced different payoff estimates.
- Historical expected returns resulted in more diversified experimental portfolios.
- Using unscaled option prices as return inputs caused excessive portfolio concentration.
- Input selection, scaling, and optimization objectives significantly influenced portfolio allocations.
- Variational quantum circuits provided an alternative approach to exploring portfolio weights.
- Quantum computing offers interesting research opportunities in financial modeling, although practical advantages require further investigation.

## Limitations

This project is an exploratory academic study and is not intended to serve as a production-ready financial modeling system.

The following limitations should be considered:

- Quantum circuits were executed on classical simulators rather than physical quantum hardware.
- The payoff estimator uses quantum circuit sampling rather than full Quantum Amplitude Estimation.
- The quantum-inspired estimator evaluates maturity payoffs without modeling early exercise.
- The portfolio optimization implementation uses continuous variational weights rather than an explicit binary QUBO formulation.
- Some covariance matrix inputs are illustrative rather than directly estimated from the original dataset.
- The pricing scripts use experimental initial values that are not verified underlying stock prices.
- The price simulations use historical expected returns rather than risk-neutral drift.
- Classical and variational optimizers use different objective functions.
- The original historical dataset is not included in the current repository.
- Variational circuit initialization and quantum measurement sampling are not fully seeded, so some results may vary between executions.
- The analysis is limited to three technology stocks.
- No computational quantum advantage is claimed.

The reported results should be interpreted within the assumptions and limitations of the original academic experiment.

This project is intended for educational and research purposes only and does not constitute financial advice.

## Future Improvements

Potential extensions of this research include:

- Implementing full Quantum Amplitude Estimation.
- Developing an explicit QUBO-based portfolio optimization model.
- Exploring the Quantum Approximate Optimization Algorithm (QAOA).
- Integrating automated historical market data collection.
- Using empirically estimated covariance matrices.
- Implementing risk-neutral option pricing.
- Comparing option pricing methods under identical exercise conditions.
- Using consistent optimization objectives across classical and quantum methods.
- Expanding the number of assets.
- Evaluating computational runtime and convergence.
- Adding automated unit tests.
- Improving experimental reproducibility.
- Exploring execution on physical quantum hardware.

## Research Paper

The complete research paper provides theoretical background, mathematical formulations, experimental methodology, results, visualizations, and conclusions.

**Title:** Quantum Computing in Pricing and Optimization of Stocks: Amazon, Apple, and Microsoft

**Author:** Luvinga Kahise

**Institution:** St. Olaf College

**Completed:** Fall 2025

[Read the Full Research Paper (PDF)](research/Quantum_Pricing_and_Optimization_Paper.pdf)

## References

- Preskill, J. (2018). Quantum Computing in the NISQ Era and Beyond.
- Rebentrost, P., et al. (2018). Quantum Computational Finance: Monte Carlo Pricing of Financial Derivatives.
- Stamatopoulos, N., et al. (2020). Option Pricing Using Quantum Computers.
- Haydock, M. (2025). Quantum Optimization and Monte Carlo. Course instructional materials.
- Additional references are available in the original research paper.

## Acknowledgments

This research project was completed as part of the Quantum Computing course at St. Olaf College.

The portfolio optimization implementation was adapted from instructional examples provided by Dr. Michael Haydock.

The project also used AI-assisted development and research support, as acknowledged in the original research paper.

## Author

**Luvinga Kahise**

Computer Science & Quantitative Economics

St. Olaf College

- GitHub: [github.com/luvinga](https://github.com/luvinga)
- LinkedIn: [linkedin.com/in/luvinga-kahise](https://www.linkedin.com/in/luvinga-kahise)

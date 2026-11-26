
## Repository Structure

```text
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

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 4. Run Option Pricing Simulations

Apple (AAPL):

```bash
python3 option_pricing/monte_carlo_aapl.py
```

Amazon (AMZN):

```bash
python3 option_pricing/monte_carlo_amzn.py
```

Microsoft (MSFT):

```bash
python3 option_pricing/monte_carlo_msft.py
```

Each simulation generates stock price paths, calculates
classical and quantum-inspired payoff estimates, and
displays simulation visualizations.

### 5. Run Portfolio Optimization

```bash
python3 portfolio_optimization/optimization.py
```

The optimization script compares:

- Classical Sharpe ratio maximization
- Random portfolio sampling
- Hybrid variational quantum optimization
- Portfolio weights and risk contributions

The original script defaults to option-price inputs.
Historical expected returns can be substituted using
the values documented in the source code.

## Research Paper

The complete research paper provides theoretical
background, methodology, experimental results,
visualizations, and conclusions.

[Read the Full Research Paper (PDF)](research/Quantum_Pricing_and_Optimization_Paper.pdf)

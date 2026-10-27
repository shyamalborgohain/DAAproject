# Optimal Transmitter Placement - DAA Project Problem 10

An implementation of the transmitter placement problem on a circular network. The objective is to cover every checkpost while minimizing interference, defined as the number of checkposts covered by two or more selected transmitters.

Refer to DAA_Problem10 for the full problem statement.

## Requirements

- Python 3.10+
- No external libraries required.&#x20;

## Project Structure

```text
├── Pb10/
│   ├── Pb10.py
│   ├── run_Pb10.py
│   └── samples_Pb10.py
├── optimized_Pb10/
│   ├── optimized_Pb10.py
│   ├── run_optimized_Pb10.py
│   └── samples_optimized_Pb10.py
├── .gitignore
├── DAA_Problem10.pdf
└── README.md
```

## Setup

```bash
git clone https://github.com/shyamalborgohain/DAAproject.git
cd DAAproject
```

## Usage

Run commands from the repository root.

**Original algorithm**

```bash
python Pb10/run_Pb10.py
python Pb10/samples_Pb10.py
```

**Optimized algorithm**

```bash
python optimized_Pb10/run_optimized_Pb10.py
python optimized_Pb10/samples_optimized_Pb10.py
```

The `run_*.py` files use manually specified inputs. Edit them to test your own values.

The `samples_*.py` files generate random test cases. Customize `TESTS`, `L1`/`L2` (circumference), `p1`/`p2` (number of checkposts), `c1`/`c2` (number of candidates), and `R` (coverage radius) to change the tests.

## Input Parameters

- `posts`: Checkpost positions.
- `L`: Circle circumference.
- `candidates`: Possible transmitter locations.
- `r`: Transmitter coverage radius (default: `250`).

## Output

Returns the minimum interference cost and selected transmitter locations. If no feasible configuration exists, the algorithm indicates that no solution is available.

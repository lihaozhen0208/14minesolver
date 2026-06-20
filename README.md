# Minesweeper Solver

A constraint satisfaction solver for Minesweeper that finds the next safe cell to click based on logical deduction.

## Features

- **Constraint Propagation**: Automatically deduces safe cells using logical reasoning
- **Hypothesis Testing**: Uses assumption testing to find cells that lead to contradictions
- **Interactive Mode**: Click-by-click solving with user input
- **Demo Mode**: Pre-configured examples to test the solver
- **Efficient Algorithm**: Combines constraint propagation with intelligent backtracking

## Usage

### Input Format

Each cell can be represented as:
- `x` - Confirmed mine
- `y` or `0` - Zero mines in the 8 neighbors (all neighbors are safe)
- `1-8` or multi-digit numbers like `10`, `11`, etc. - Number of mines in the 8 neighbors
- `?` - Unknown cell

For `map.txt`, use spaces to separate cells and newlines to separate rows. This is required when a number has more than one digit.

Optionally, the last non-empty line may specify the remaining mine count by starting with `#` followed by the number (e.g. `# 2` or `#2`). This line will be ignored as a board row and treated as the global remaining mines value.

Example:
```
y 1 ?
1 1 ?
? ? ?
```

### Interactive Mode

```bash
python main.py
```

Then enter each row of the board, pressing Enter after each row. Press Enter again to finish.

Example:
```
> y1?
> 11?
> ???
>
```

### Demo Mode

```bash
python main.py --demo
```

Shows several pre-configured examples.

### Programmatic Usage

```python
from solver import MinesweeperSolver

board = [
    "y1?",
    "11?",
    "???"
]

solver = MinesweeperSolver(board)
solver = MinesweeperSolver(board)
# Use the 1-based API to get coordinates in (row, col) starting from 1
result = solver.solve_one_based()

if result:
    row, col = result
    print(f"Safe cell at: ({row}, {col})")
```

## Algorithm

1. **Constraint Propagation Phase**
   - For each numbered cell, count confirmed mines and unknown neighbors
   - If confirmed mines == required mines: mark all unknown neighbors as safe
   - If confirmed mines + unknown neighbors == required mines: mark all unknown as mines
   - Repeat until no changes occur

2. **Hypothesis Testing Phase** (if needed)
   - For each unknown cell, test if assuming it's a mine leads to contradiction
   - If contradiction found, the cell must be safe
   - Returns the first safe cell found

## Files

- `solver.py` - Core solver implementation
- `main.py` - Interactive and demo modes
- `test_solver.py` - Test cases
- `minesolver.py` - Alternative implementation (reference)

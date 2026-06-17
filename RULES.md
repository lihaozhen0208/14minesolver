# Minesweeper Solver with Rule Support

A constraint satisfaction solver for Minesweeper that supports multiple rule sets.

## 📋 Rules

### Rule V - Standard Minesweeper (默认)
Standard minesweeper rules where each number indicates the exact count of mines in 8 neighbors.

### Rule M - Multi-mine with Checkerboard Coloring 
Cells are colored in a checkerboard pattern (black/white). Top-left (0,0) is a colored (black) cell. 
**Rule: Colored cells count mines as double.**

- Colored cell: `(r + c) % 2 == 0` (top-left is colored)
- A number "n" on a colored cell actually means "2n" mines nearby
- A number "n" on a non-colored cell means "n" mines nearby

Example:
```
Rule M board:
2??
???
???

(0,0) is colored, "2" = 4 mines nearby
(0,1) is not colored, "?" = unknown
```

## 📁 Files

- `config.txt` - Rule specification (one per line, e.g., "V", "M")
- `map.txt` - Current minesweeper board state
- `solver.py` - Core algorithm supporting rule-based constraint propagation
- `map_solver.py` - Main program to read config and map, output next safe cell

## 🚀 Usage

1. Edit `config.txt` to specify rules (default: V)
   ```
   V
   ```
   or
   ```
   M
   ```

2. Edit `map.txt` with current board
   ```
   y??
   ???
   ???
   ```

3. Run:
   ```bash
   python map_solver.py
   ```

## 🧪 Testing

```bash
python test_rules.py
```

## 🔧 Implementation Details

- Rules are read as a list of strings from config.txt
- Multiple rules can be combined (each on a separate line)
- The solver applies all active rules when computing mine requirements
- Currently supports: V (standard), M (multi-mine)

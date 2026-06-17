#!/usr/bin/env python3
"""
Interactive Minesweeper Solver
Finds the next safe cell to click based on constraint satisfaction
"""

from solver import MinesweeperSolver, format_output


def interactive_mode():
    """Interactive mode for solving minesweeper."""
    print("=" * 70)
    print("Interactive Minesweeper Solver")
    print("=" * 70)
    print()
    print("Format:")
    print("  'x' = confirmed mine")
    print("  'y' = 0 mines nearby (or '0')")
    print("  '1'-'8' = number of mines in 8 neighbors")
    print("  '?' = unknown cell")
    print()
    print("Example:")
    print("  y1?")
    print("  11?")
    print("  ???")
    print()
    
    while True:
        board_lines = []
        print("Enter board (empty line to finish, or 'q' to quit):")
        
        try:
            while True:
                line = input("> ").strip()
                if line.lower() == 'q':
                    return
                if not line:
                    break
                board_lines.append(line)
            
            if not board_lines:
                print("No board provided, please try again.\n")
                continue
            
            # Validate board
            if not all(len(line) == len(board_lines[0]) for line in board_lines):
                print("Error: All rows must have the same length.\n")
                continue
            
            # Solve
            solver = MinesweeperSolver(board_lines)
            result = solver.solve()
            
            print()
            print("Board:")
            for i, line in enumerate(board_lines):
                print(f"  {line}")
            print()
            print(format_output(result))
            print()
            
        except KeyboardInterrupt:
            print("\nExiting...")
            return
        except Exception as e:
            print(f"Error: {e}\n")


def demo_mode():
    """Run demo with predefined examples."""
    examples = [
        {
            "name": "Simple case - y marks 0 mines",
            "board": ["y?", "??"]
        },
        {
            "name": "Corner with numbers",
            "board": ["11?", "1?1", "???"]
        },
        {
            "name": "With confirmed mine",
            "board": ["x1?", "1?1", "???"]
        },
        {
            "name": "Larger board",
            "board": [
                "11y11",
                "1?1?1",
                "1?1?1",
                "11y11",
                "?????"
            ]
        }
    ]
    
    print("=" * 70)
    print("Minesweeper Solver - Demo")
    print("=" * 70)
    print()
    
    for i, example in enumerate(examples, 1):
        print(f"Example {i}: {example['name']}")
        print("-" * 70)
        board = example["board"]
        print("Board:")
        for line in board:
            print(f"  {line}")
        
        solver = MinesweeperSolver(board)
        result = solver.solve()
        print(format_output(result))
        print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_mode()
    else:
        interactive_mode()

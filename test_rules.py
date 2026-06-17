#!/usr/bin/env python3
"""Test rule M (multi-mine with checkerboard coloring)"""

from map_solver import MapSolver
import os


def test_rule(name, config_content, map_content, expected_msg=""):
    """Test a specific rule."""
    print(f"\n{'=' * 70}")
    print(f"Test: {name}")
    print('=' * 70)
    
    # Write test files
    with open('config.txt', 'w') as f:
        f.write(config_content)
    with open('map.txt', 'w') as f:
        f.write(map_content)
    
    # Solve
    solver = MapSolver()
    solver.analyze()


def main():
    """Run all rule tests."""
    print("Testing Rules: V (standard) and M (multi-mine)")
    
    # Test V rule (standard)
    test_rule(
        "V rule - standard Minesweeper",
        "V",
        "y??\n???\n???"
    )
    
    # Test M rule - simple checkerboard
    test_rule(
        "M rule - checkerboard coloring",
        "M",
        "2??\n???\n???"
    )
    
    # Test M rule - with safe cells
    test_rule(
        "M rule - with y (0 mines)",
        "M",
        "y??\n?1?\n???"
    )
    
    print(f"\n{'=' * 70}")
    print("Test completed!")
    print('=' * 70)
    print("\nNote: In rule M, colored cells (black in checkerboard) have doubled mine counts.")
    print("Checkerboard: (0,0) is colored, (r+c) even = colored")


if __name__ == "__main__":
    main()

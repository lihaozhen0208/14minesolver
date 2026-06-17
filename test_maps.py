#!/usr/bin/env python3
"""
Test different map scenarios
"""

import os
from map_solver import MapSolver


def test_map(name, content):
    """Test a specific map."""
    print(f"\n{'=' * 70}")
    print(f"Test: {name}")
    print('=' * 70)
    
    # Write test map
    with open('map.txt', 'w') as f:
        f.write(content)
    
    # Solve
    solver = MapSolver('map.txt')
    solver.analyze()


def main():
    """Run all tests."""
    tests = [
        (
            "Safe corner (0 mines around)",
            "y??\n???\n???"
        ),
        (
            "With confirmed mine",
            "x1?\n1?1\n???"
        ),
        (
            "Multiple safe areas",
            "11y11\n1?1?1\n1?1?1\n11y11\n?????"
        ),
        (
            "All numbered cells",
            "111\n1?1\n111"
        ),
        (
            "Single confirmed mine",
            "x??\n???\n???"
        ),
    ]
    
    for name, content in tests:
        test_map(name, content)
    
    print(f"\n{'=' * 70}")
    print("All tests completed!")
    print('=' * 70)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Test remaining mines with different rules"""

from map_solver import MapSolver


def test_scenario(name, config, map_content):
    """Test a specific scenario."""
    print(f"\n{'=' * 70}")
    print(f"Test: {name}")
    print('=' * 70)
    
    with open('config.txt', 'w') as f:
        f.write(config)
    with open('map.txt', 'w') as f:
        f.write(map_content)
    
    solver = MapSolver()
    solver.analyze()


def main():
    print("Testing Remaining Mines with Rules V and M")
    
    # Test V rule with remaining mines
    test_scenario(
        "V rule - with remaining mines count",
        "V",
        "y??\n?1?\n???\n2"
    )
    
    # Test M rule with remaining mines
    # In M rule, the remaining mines count should NOT be doubled
    test_scenario(
        "M rule - remaining mines (NOT doubled)",
        "M",
        "2??\n?1?\n???\n2"
    )
    
    # Test with more mines remaining
    test_scenario(
        "V rule - 4 remaining mines",
        "V",
        "x??\n?1?\n???\n4"
    )
    
    print(f"\n{'=' * 70}")
    print("Note: Remaining mines count is treated as literal (not affected by M rule)")
    print('=' * 70)


if __name__ == "__main__":
    main()

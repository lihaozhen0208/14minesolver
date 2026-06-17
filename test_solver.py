"""
Test cases for the minesweeper solver
"""

from solver import MinesweeperSolver, format_output


def test_case_1():
    """Simple case: number tells us neighbors are safe"""
    board = [
        "y?",
        "??"
    ]
    solver = MinesweeperSolver(board)
    result = solver.solve()
    print("Test 1 - y (0 mines) should make neighbors safe:")
    print(f"Board:\n{chr(10).join(board)}")
    print(f"Result: {format_output(result)}")
    print()


def test_case_2():
    """Number at corner"""
    board = [
        "1?",
        "??"
    ]
    solver = MinesweeperSolver(board)
    result = solver.solve()
    print("Test 2 - 1 mine around 1:")
    print(f"Board:\n{chr(10).join(board)}")
    print(f"Result: {format_output(result)}")
    print()


def test_case_3():
    """All neighbors must be mines"""
    board = [
        "??",
        "2?"
    ]
    solver = MinesweeperSolver(board)
    result = solver.solve()
    print("Test 3 - 2 mines around bottom-left 2:")
    print(f"Board:\n{chr(10).join(board)}")
    print(f"Result: {format_output(result)}")
    print()


def test_case_4():
    """More complex scenario"""
    board = [
        "11?",
        "1?1",
        "???"
    ]
    solver = MinesweeperSolver(board)
    result = solver.solve()
    print("Test 4 - Complex 3x3 board:")
    print(f"Board:\n{chr(10).join(board)}")
    print(f"Result: {format_output(result)}")
    print()


def test_case_5():
    """Mix of confirmed mines and unknowns"""
    board = [
        "x1?",
        "1?1",
        "???"
    ]
    solver = MinesweeperSolver(board)
    result = solver.solve()
    print("Test 5 - With confirmed mine:")
    print(f"Board:\n{chr(10).join(board)}")
    print(f"Result: {format_output(result)}")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Minesweeper Solver - Test Cases")
    print("=" * 60)
    print()
    
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    test_case_5()

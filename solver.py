"""
Minesweeper Solver - finds the next safe cell to click
"""

from typing import List, Tuple, Set, Optional, Dict
from copy import deepcopy
from itertools import combinations


class MinesweeperSolver:
    def __init__(self, board: List[str]):
        """
        Initialize solver with board state.
        
        'x' = confirmed mine
        'y' = 0 mines nearby (safe, all 8 neighbors are safe)
        '0'-'8' = number of mines in 8 neighbors
        '?' or other = unknown cell
        """
        self.board = [list(row) for row in board]
        self.rows = len(self.board)
        self.cols = len(self.board[0]) if self.board else 0
        
        # Track possible states for unknown cells
        self.possible = {}
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == '?':
                    self.possible[(r, c)] = {'mine', 'safe'}
    
    def get_neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        """Get all 8 neighbors."""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbors.append((nr, nc))
        return neighbors
    
    def propagate_constraints(self) -> bool:
        """
        Apply constraint propagation.
        Returns False if contradiction found, True otherwise.
        """
        changed = True
        iterations = 0
        max_iterations = 1000
        
        while changed and iterations < max_iterations:
            iterations += 1
            changed = False
            
            # For each numbered cell, apply constraints
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.board[r][c]
                    
                    # Skip non-numbered cells
                    if cell not in '0123456789y':
                        continue
                    
                    required_mines = 0 if cell == 'y' else int(cell)
                    neighbors = self.get_neighbors(r, c)
                    
                    confirmed_mines = 0
                    unknown_neighbors = []
                    safe_neighbors = []
                    
                    for nr, nc in neighbors:
                        if self.board[nr][nc] == 'x':
                            confirmed_mines += 1
                        elif (nr, nc) in self.possible:
                            unknown_neighbors.append((nr, nc))
                        elif self.board[nr][nc] == '?':
                            unknown_neighbors.append((nr, nc))
                    
                    # If all required mines are confirmed, rest must be safe
                    if confirmed_mines == required_mines:
                        for nr, nc in unknown_neighbors:
                            if (nr, nc) in self.possible:
                                if 'mine' in self.possible[(nr, nc)]:
                                    self.possible[(nr, nc)].remove('mine')
                                    if not self.possible[(nr, nc)]:
                                        return False
                                    changed = True
                    
                    # If confirmed mines + unknown cells == required mines, all unknown are mines
                    elif confirmed_mines + len(unknown_neighbors) == required_mines:
                        for nr, nc in unknown_neighbors:
                            if (nr, nc) in self.possible:
                                if 'safe' in self.possible[(nr, nc)]:
                                    self.possible[(nr, nc)].remove('safe')
                                    if not self.possible[(nr, nc)]:
                                        return False
                                    changed = True
        
        return True
    
    def find_definite_safe(self) -> Set[Tuple[int, int]]:
        """Find cells that are definitely safe using constraint propagation."""
        # First propagate constraints
        if not self.propagate_constraints():
            return set()
        
        definite_safe = set()
        for cell, states in self.possible.items():
            if len(states) == 1 and 'safe' in states:
                definite_safe.add(cell)
        
        return definite_safe
    
    def find_safe_by_hypothesis(self) -> Optional[Tuple[int, int]]:
        """
        Use hypothesis testing to find safe cells.
        For each unknown cell, check if assuming it's a mine leads to a unique solution.
        If yes, try assuming it's safe - if that fails, it must be safe.
        """
        unknown_cells = list(self.possible.keys())
        
        for cell in unknown_cells:
            # Try assuming this cell is a mine
            if not self.can_have_solution_with_assumption(cell, 'mine'):
                # No valid solution if this is a mine, so it must be safe
                return cell
            
            # Try assuming this cell is safe
            if not self.can_have_solution_with_assumption(cell, 'safe'):
                # No valid solution if this is safe, so it must be a mine
                # But we want safe cells, so skip this
                continue
        
        return None
    
    def can_have_solution_with_assumption(self, cell: Tuple[int, int], state: str) -> bool:
        """
        Check if there's a valid solution assuming cell has the given state.
        state can be 'mine' or 'safe'
        """
        test_possible = deepcopy(self.possible)
        test_board = [row[:] for row in self.board]
        
        # Set the assumption
        if state == 'mine':
            test_possible[cell] = {'mine'}
            test_board[cell[0]][cell[1]] = 'x'
        else:
            test_possible[cell] = {'safe'}
            test_board[cell[0]][cell[1]] = 'S'
        
        # Try to propagate constraints with this assumption
        return self.propagate_with_board(test_board, test_possible)
    
    def propagate_with_board(self, board: List[List[str]], possible: Dict[Tuple[int, int], Set[str]]) -> bool:
        """Propagate constraints with a specific board state."""
        changed = True
        iterations = 0
        max_iterations = 1000
        
        while changed and iterations < max_iterations:
            iterations += 1
            changed = False
            
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = board[r][c]
                    
                    if cell not in '0123456789y':
                        continue
                    
                    required_mines = 0 if cell == 'y' else int(cell)
                    neighbors = self.get_neighbors(r, c)
                    
                    confirmed_mines = 0
                    unknown_neighbors = []
                    
                    for nr, nc in neighbors:
                        if board[nr][nc] == 'x':
                            confirmed_mines += 1
                        elif (nr, nc) in possible:
                            unknown_neighbors.append((nr, nc))
                        elif board[nr][nc] == '?':
                            unknown_neighbors.append((nr, nc))
                    
                    # If all required mines are confirmed, rest must be safe
                    if confirmed_mines == required_mines:
                        for nr, nc in unknown_neighbors:
                            if (nr, nc) in possible and 'mine' in possible[(nr, nc)]:
                                possible[(nr, nc)].remove('mine')
                                if not possible[(nr, nc)]:
                                    return False
                                changed = True
                    
                    # If confirmed mines + unknown = required mines, all unknown are mines
                    elif confirmed_mines + len(unknown_neighbors) == required_mines:
                        for nr, nc in unknown_neighbors:
                            if (nr, nc) in possible and 'safe' in possible[(nr, nc)]:
                                possible[(nr, nc)].remove('safe')
                                if not possible[(nr, nc)]:
                                    return False
                                changed = True
        
        return True
    
    def is_valid_assignment(self, possible: Dict[Tuple[int, int], Set[str]]) -> bool:
        """Check if an assignment of possibilities is valid."""
        # Create a test board
        test_board = [row[:] for row in self.board]
        
        for (r, c), states in possible.items():
            if len(states) == 1:
                if 'mine' in states:
                    test_board[r][c] = 'x'
                else:
                    test_board[r][c] = 'S'  # marker for safe
        
        # Check all constraints
        for r in range(self.rows):
            for c in range(self.cols):
                cell = test_board[r][c]
                
                if cell not in '0123456789y':
                    continue
                
                required_mines = 0 if cell == 'y' else int(cell)
                neighbors = self.get_neighbors(r, c)
                
                confirmed_mines = 0
                unknown_count = 0
                
                for nr, nc in neighbors:
                    if test_board[nr][nc] == 'x':
                        confirmed_mines += 1
                    elif test_board[nr][nc] not in 'Sxy0123456789':
                        unknown_count += 1
                
                # Constraint violation checks
                if confirmed_mines > required_mines:
                    return False
                if confirmed_mines + unknown_count < required_mines:
                    return False
        
        return True
    
    def solve(self) -> Optional[Tuple[int, int]]:
        """Find the next safe cell to click."""
        # First try constraint propagation
        safe = self.find_definite_safe()
        if safe:
            return next(iter(safe))
        
        # If not found, try hypothesis testing
        return self.find_safe_by_hypothesis()


def parse_input(text: str) -> List[str]:
    """Parse board from text."""
    lines = text.strip().split('\n')
    return [line.strip() for line in lines if line.strip()]


def format_output(result: Optional[Tuple[int, int]]) -> str:
    """Format the solution."""
    if result is None:
        return "No safe cell found (unexpected - problem should have a solution)"
    return f"Safe cell: row {result[0]}, col {result[1]} (0-indexed)"


def main():
    """Main function for interactive use."""
    print("Minesweeper Solver")
    print("=" * 60)
    print("Input format:")
    print("  'x' = confirmed mine")
    print("  'y' = 0 mines nearby")
    print("  '0'-'8' = number of nearby mines")
    print("  '?' = unknown cell")
    print()
    
    # Read board from user
    print("Enter the board (empty line to finish):")
    board_lines = []
    while True:
        line = input()
        if not line:
            break
        board_lines.append(line)
    
    if not board_lines:
        print("No board provided")
        return
    
    solver = MinesweeperSolver(board_lines)
    result = solver.solve()
    print()
    print(format_output(result))


if __name__ == "__main__":
    main()

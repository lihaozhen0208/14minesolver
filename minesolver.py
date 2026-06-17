"""
Minesweeper Solver
Finds the next safe cell to click based on the current board state.
"""

from itertools import combinations
from typing import List, Tuple, Set, Optional, Dict
from copy import deepcopy


class MinesweeperSolver:
    def __init__(self, board: List[str]):
        """
        Initialize the solver with a board.
        
        Args:
            board: List of strings representing the minesweeper board
                   'x' = mine
                   'y' = 0 mines around (safe)
                   '0'-'8' = number of mines around
                   '?' or other = unknown cell
        """
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0]) if board else 0
        self.unknown_cells = set()
        self.mines = set()
        self.safe_cells = set()
        
        # Parse the board
        for r in range(self.rows):
            for c in range(self.cols):
                cell = board[r][c]
                if cell == 'x':
                    self.mines.add((r, c))
                elif cell == '?':
                    self.unknown_cells.add((r, c))
                elif cell not in 'y0123456789':
                    self.unknown_cells.add((r, c))
    
    def get_neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        """Get all 8 neighbors of a cell."""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbors.append((nr, nc))
        return neighbors
    
    def get_constraint_cells(self, r: int, c: int) -> Tuple[List[Tuple[int, int]], int]:
        """
        Get unknown cells around a numbered cell and the required mine count.
        Returns: (unknown_neighbors, required_mines)
        """
        cell = self.board[r][c]
        if cell == 'x' or cell == '?':
            return [], 0
        
        if cell == 'y':
            required_mines = 0
        else:
            try:
                required_mines = int(cell)
            except ValueError:
                return [], 0
        
        neighbors = self.get_neighbors(r, c)
        unknown_neighbors = []
        known_mines = 0
        
        for nr, nc in neighbors:
            if (nr, nc) in self.mines:
                known_mines += 1
            elif self.board[nr][nc] == '?':
                unknown_neighbors.append((nr, nc))
            elif self.board[nr][nc] not in 'xy0123456789':
                unknown_neighbors.append((nr, nc))
        
        # Adjust required mines based on already found mines
        required_mines -= known_mines
        
        return unknown_neighbors, required_mines
    
    def is_valid_assignment(self, assignment: dict) -> bool:
        """Check if an assignment satisfies all constraints."""
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.board[r][c]
                if cell not in 'y0123456789':
                    continue
                
                neighbors = self.get_neighbors(r, c)
                required_mines = 0 if cell == 'y' else int(cell)
                
                mine_count = 0
                unknown_count = 0
                
                for nr, nc in neighbors:
                    if (nr, nc) in self.mines:
                        mine_count += 1
                    elif (nr, nc) in assignment:
                        if assignment[(nr, nc)]:
                            mine_count += 1
                    elif (nr, nc) in self.unknown_cells:
                        unknown_count += 1
                
                # Check if constraint is violated
                if mine_count > required_mines:
                    return False
                if mine_count + unknown_count < required_mines:
                    return False
        
        return True
    
    def deduce_safe_cells(self) -> Set[Tuple[int, int]]:
        """Use constraint propagation and backtracking to find safe cells."""
        safe = set()
        
        # Try each unknown cell
        for unknown_cell in self.unknown_cells:
            # Try assigning it as NOT a mine
            possible_as_safe = True
            
            # Use backtracking to check if this cell can be safe
            test_assignment = {}
            if not self.can_be_safe(unknown_cell, test_assignment):
                possible_as_safe = False
            
            # Try assigning it as a mine
            possible_as_mine = True
            test_assignment = {}
            if not self.can_be_mine(unknown_cell, test_assignment):
                possible_as_mine = False
            
            # If it can only be safe, it's definitely safe
            if possible_as_safe and not possible_as_mine:
                safe.add(unknown_cell)
        
        return safe
    
    def can_be_safe(self, cell: Tuple[int, int], assignment: dict) -> bool:
        """Check if a cell can be NOT a mine using backtracking."""
        # Create a test scenario where this cell is not a mine
        test_unknown = self.unknown_cells - {cell}
        return self.backtrack(assignment, test_unknown, {cell})
    
    def can_be_mine(self, cell: Tuple[int, int], assignment: dict) -> bool:
        """Check if a cell can be a mine using backtracking."""
        # Create a test scenario where this cell is a mine
        test_unknown = self.unknown_cells - {cell}
        return self.backtrack(assignment, test_unknown, set(), {cell})
    
    def backtrack(self, assignment: dict, unknown: set, safe_assumption: set = None, mine_assumption: set = None) -> bool:
        """
        Backtracking search to find valid assignment.
        
        Args:
            assignment: Current partial assignment
            unknown: Cells that haven't been assigned yet
            safe_assumption: Cells assumed to be safe (not mines)
            mine_assumption: Cells assumed to be mines
        """
        if safe_assumption is None:
            safe_assumption = set()
        if mine_assumption is None:
            mine_assumption = set()
        
        # Apply assumptions
        test_mines = self.mines | mine_assumption
        test_assignment = assignment.copy()
        for cell in safe_assumption:
            test_assignment[cell] = False
        for cell in mine_assumption:
            test_assignment[cell] = True
        
        if not self.is_valid_assignment_with_mines(test_assignment, test_mines, unknown):
            return False
        
        if not unknown:
            return True
        
        # Pick a cell to branch on
        cell = next(iter(unknown))
        new_unknown = unknown - {cell}
        
        # Try as safe (False)
        new_assignment = test_assignment.copy()
        new_assignment[cell] = False
        if self.backtrack(new_assignment, new_unknown):
            return True
        
        # Try as mine (True)
        new_assignment = test_assignment.copy()
        new_assignment[cell] = True
        if self.backtrack(new_assignment, new_unknown):
            return True
        
        return False
    
    def is_valid_assignment_with_mines(self, assignment: dict, all_mines: set, unknown: set) -> bool:
        """Check if assignment is valid with given mine set."""
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.board[r][c]
                if cell not in 'y0123456789':
                    continue
                
                neighbors = self.get_neighbors(r, c)
                required_mines = 0 if cell == 'y' else int(cell)
                
                mine_count = 0
                unknown_count = 0
                
                for nr, nc in neighbors:
                    if (nr, nc) in all_mines:
                        mine_count += 1
                    elif (nr, nc) in assignment:
                        if assignment[(nr, nc)]:
                            mine_count += 1
                    elif (nr, nc) in unknown:
                        unknown_count += 1
                
                if mine_count > required_mines:
                    return False
                if mine_count + unknown_count < required_mines:
                    return False
        
        return True
    
    def solve(self) -> Optional[Tuple[int, int]]:
        """Find the next safe cell to click."""
        safe_cells = self.deduce_safe_cells()
        
        if safe_cells:
            # Return the first safe cell found
            return next(iter(safe_cells))
        
        return None


def parse_board(text: str) -> List[str]:
    """Parse board from text input."""
    lines = text.strip().split('\n')
    return [line.strip() for line in lines if line.strip()]


def main():
    """Main function for testing."""
    # Example input
    example_board = [
        "y1?",
        "11?",
        "???"
    ]
    
    print("Minesweeper Solver")
    print("=" * 50)
    print("Input board:")
    for row in example_board:
        print(row)
    
    solver = MinesweeperSolver(example_board)
    result = solver.solve()
    
    if result:
        print(f"\nNext safe cell to click: ({result[0]}, {result[1]})")
    else:
        print("\nCould not determine a safe cell to click.")


if __name__ == "__main__":
    main()

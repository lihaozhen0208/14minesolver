"""
Minesweeper Solver - Constraint satisfaction algorithm
"""

from typing import List, Tuple, Set, Optional, Dict
from copy import deepcopy


class MinesweeperSolver:
    def __init__(self, board: List[str], rules: Optional[List[str]] = None, remaining_mines: Optional[int] = None):
        """Initialize solver with board state and rules.

        Args:
            board: list of string rows
            rules: list of single-letter rule identifiers (e.g. ['V', 'M'])
            remaining_mines: total remaining mines count (optional, not affected by M rule)
        """
        self.board = [list(row) for row in board]
        self.rows = len(self.board)
        self.cols = len(self.board[0]) if self.board else 0
        # Rules: default to ['V'] (the existing Minesweeper rules)
        self.rules = rules if rules else ['V']
        self.remaining_mines = remaining_mines  # Global constraint: total mines left

        # Currently only rule 'V' (standard propagation) is supported.
        self.possible = {}
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == '?':
                    self.possible[(r, c)] = {'mine', 'safe'}
    
    def is_colored_cell(self, r: int, c: int) -> bool:
        """Check if cell is colored (black) in checkerboard pattern.
        Top-left (0,0) is colored. (r+c) % 2 == 0 means colored."""
        return (r + c) % 2 == 0
    
    def get_required_mines(self, r: int, c: int, base_value: int) -> int:
        """Get the required mine count after applying rules.
        
        Args:
            r, c: cell position
            base_value: number shown on cell (0-8)
            
        Returns:
            adjusted required mine count based on rules
        """
        required = base_value
        
        # Rule M: colored (black) cells count as double
        if 'M' in self.rules and self.is_colored_cell(r, c):
            required *= 2
        
        return required
    
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
        """Apply constraint propagation."""
        changed = True
        iterations = 0
        
        while changed and iterations < 1000:
            iterations += 1
            changed = False
            
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.board[r][c]
                    if cell not in '0123456789y':
                        continue
                    
                    base_value = 0 if cell == 'y' else int(cell)
                    required_mines = self.get_required_mines(r, c, base_value)
                    neighbors = self.get_neighbors(r, c)
                    
                    confirmed_mines = 0
                    unknown_neighbors = []
                    
                    for nr, nc in neighbors:
                        if self.board[nr][nc] == 'x':
                            confirmed_mines += 1
                        elif (nr, nc) in self.possible:
                            unknown_neighbors.append((nr, nc))
                    
                    if confirmed_mines == required_mines:
                        for nr, nc in unknown_neighbors:
                            if 'mine' in self.possible[(nr, nc)]:
                                self.possible[(nr, nc)].remove('mine')
                                if not self.possible[(nr, nc)]:
                                    return False
                                changed = True
                    
                    elif confirmed_mines + len(unknown_neighbors) == required_mines:
                        for nr, nc in unknown_neighbors:
                            if 'safe' in self.possible[(nr, nc)]:
                                self.possible[(nr, nc)].remove('safe')
                                if not self.possible[(nr, nc)]:
                                    return False
                                changed = True
        
        # Apply remaining mines constraint (if specified)
        if self.remaining_mines is not None:
            confirmed_mines = sum(1 for r in range(self.rows) for c in range(self.cols) 
                                if self.board[r][c] == 'x')
            
            # Count cells that must be mines or could be mines
            possible_mines = sum(1 for states in self.possible.values() 
                               if 'mine' in states)
            
            # If confirmed + possible >= remaining, we have enough potential
            if confirmed_mines > self.remaining_mines:
                return False  # Contradiction
            
            # If confirmed + possible == remaining, mark rest as safe
            if confirmed_mines + possible_mines == self.remaining_mines:
                for cell, states in self.possible.items():
                    if 'safe' in states and len(states) > 1:
                        self.possible[cell] = {'safe'}
                        changed = True
        
        return True
    
    def find_definite_safe(self) -> Set[Tuple[int, int]]:
        """Find cells that are definitely safe."""
        if not self.propagate_constraints():
            return set()
        
        return {cell for cell, states in self.possible.items() 
                if len(states) == 1 and 'safe' in states}
    
    def can_have_solution_with_assumption(self, cell: Tuple[int, int], state: str) -> bool:
        """Check if there's a valid solution with assumption."""
        test_possible = deepcopy(self.possible)
        test_board = [row[:] for row in self.board]
        
        if state == 'mine':
            test_possible[cell] = {'mine'}
            test_board[cell[0]][cell[1]] = 'x'
        else:
            test_possible[cell] = {'safe'}
            test_board[cell[0]][cell[1]] = 'S'
        
        return self._propagate_with_board(test_board, test_possible)
    
    def _propagate_with_board(self, board: List[List[str]], possible: Dict[Tuple[int, int], Set[str]]) -> bool:
        """Propagate constraints with specific board state."""
        changed = True
        iterations = 0
        
        while changed and iterations < 1000:
            iterations += 1
            changed = False
            
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = board[r][c]
                    if cell not in '0123456789y':
                        continue
                    
                    base_value = 0 if cell == 'y' else int(cell)
                    required_mines = self.get_required_mines(r, c, base_value)
                    neighbors = self.get_neighbors(r, c)
                    
                    confirmed_mines = 0
                    unknown_neighbors = []
                    
                    for nr, nc in neighbors:
                        if board[nr][nc] == 'x':
                            confirmed_mines += 1
                        elif (nr, nc) in possible:
                            unknown_neighbors.append((nr, nc))
                    
                    if confirmed_mines == required_mines:
                        for nr, nc in unknown_neighbors:
                            if (nr, nc) in possible and 'mine' in possible[(nr, nc)]:
                                possible[(nr, nc)].remove('mine')
                                if not possible[(nr, nc)]:
                                    return False
                                changed = True
                    
                    elif confirmed_mines + len(unknown_neighbors) == required_mines:
                        for nr, nc in unknown_neighbors:
                            if (nr, nc) in possible and 'safe' in possible[(nr, nc)]:
                                possible[(nr, nc)].remove('safe')
                                if not possible[(nr, nc)]:
                                    return False
                                changed = True
        
        return True
    
    def solve(self) -> Optional[Tuple[int, int]]:
        """Find the next safe cell to click."""
        safe = self.find_definite_safe()
        if safe:
            return next(iter(safe))
        
        # Try hypothesis testing
        unknown_cells = list(self.possible.keys())
        for cell in unknown_cells:
            if not self.can_have_solution_with_assumption(cell, 'mine'):
                return cell
        
        return None

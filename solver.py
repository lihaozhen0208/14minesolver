"""
Minesweeper Solver - Constraint satisfaction algorithm
"""

from typing import List, Tuple, Set, Optional, Dict
from copy import deepcopy


class MinesweeperSolver:
    def __init__(self, board: List[str]):
        """Initialize solver with board state."""
        self.board = [list(row) for row in board]
        self.rows = len(self.board)
        self.cols = len(self.board[0]) if self.board else 0
        
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
                    
                    required_mines = 0 if cell == 'y' else int(cell)
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
                    
                    required_mines = 0 if cell == 'y' else int(cell)
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

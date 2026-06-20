"""
Minesweeper Solver - Constraint satisfaction algorithm
"""

from typing import List, Tuple, Set, Optional, Dict, Union
from copy import deepcopy


class MinesweeperSolver:
    def __init__(self, board: List[Union[str, List[str]]], rules: Optional[List[str]] = None, remaining_mines: Optional[int] = None):
        """Initialize solver with board state and rules.

        Args:
            board: list of rows, where each row is either a string or a list of cell tokens
            rules: list of single-letter rule identifiers (e.g. ['V', 'M'])
            remaining_mines: total remaining mines count (optional, not affected by M rule)
        """
        self.board = []
        for row in board:
            if isinstance(row, str):
                self.board.append(list(row))
            else:
                self.board.append(list(row))

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
        """Check if cell is colored (checkerboard pattern).
        Uses 1-based parity semantics: cells where (row+col) is even when
        counted from 1 are "colored" (e.g. (1,1), (2,2), (3,3)).
        For rule `M` a mine on a colored cell contributes 1, on other
        cells contributes 2.
        """
        # Convert to 1-based coordinates and check parity; equivalent
        # to (r + c) % 2 == 0 but kept explicit for clarity.
        return ((r + 1) + (c + 1)) % 2 == 0
    
    def get_required_mines(self, r: int, c: int, base_value: int) -> int:
        """Get the required mine count after applying rules.
        
        Args:
            r, c: cell position
            base_value: number shown on cell (0-8)
            
        Returns:
            adjusted required mine count based on rules
        """
        # The displayed number is the required total contribution from
        # neighboring mines. Do not modify it here; neighbour mines will
        # be counted with weights (2 for colored neighbours, 1 otherwise).
        return base_value
    
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
                    if cell == 'y':
                        base_value = 0
                    elif isinstance(cell, str) and cell.isdigit():
                        base_value = int(cell)
                    else:
                        continue

                    required = self.get_required_mines(r, c, base_value)
                    neighbors = self.get_neighbors(r, c)

                    # confirmed contribution from known mines, and unknown neighbors with weights
                    confirmed_contrib = 0
                    unknown_neighbors = []  # list of (nr, nc, weight)

                    for nr, nc in neighbors:
                        # weight: with updated M rule a mine on a colored cell contributes 1,
                        # otherwise contributes 2. When M is not enabled, each mine contributes 1.
                        if 'M' in self.rules:
                            weight = 1 if self.is_colored_cell(nr, nc) else 2
                        else:
                            weight = 1

                        if self.board[nr][nc] == 'x':
                            confirmed_contrib += weight
                        elif (nr, nc) in self.possible:
                            # unknown cell possible states
                            unknown_neighbors.append((nr, nc, weight))

                    # Contradiction checks using contribution ranges
                    max_possible = confirmed_contrib + sum(w for (_, _, w) in unknown_neighbors)
                    min_possible = confirmed_contrib
                    if confirmed_contrib > required:
                        return False
                    if max_possible < required:
                        return False

                    # If minimum equals required => all unknown neighbors safe
                    if min_possible == required:
                        for nr, nc, _ in unknown_neighbors:
                            if 'mine' in self.possible[(nr, nc)]:
                                self.possible[(nr, nc)].remove('mine')
                                if not self.possible[(nr, nc)]:
                                    return False
                                changed = True

                    # If maximum equals required => all unknown neighbors must be mines
                    elif max_possible == required:
                        for nr, nc, _ in unknown_neighbors:
                            if 'safe' in self.possible[(nr, nc)]:
                                self.possible[(nr, nc)].remove('safe')
                                if not self.possible[(nr, nc)]:
                                    return False
                                changed = True
        
        # Apply remaining mines constraint (if specified)
        if self.remaining_mines is not None:
            confirmed_mines = sum(1 for r in range(self.rows) for c in range(self.cols)
                                if self.board[r][c] == 'x')

            possible_mines = sum(1 for states in self.possible.values() if 'mine' in states)

            # Contradiction: too many confirmed mines or not enough possible cells
            if confirmed_mines > self.remaining_mines:
                return False
            if confirmed_mines + possible_mines < self.remaining_mines:
                return False

            # If we've already reached remaining mines, mark all other unknowns safe
            if confirmed_mines == self.remaining_mines:
                for cell, states in list(self.possible.items()):
                    if 'safe' in states and len(states) > 1:
                        self.possible[cell] = {'safe'}
                        changed = True

            # If confirmed + possible == remaining, all possible must be mines
            if confirmed_mines + possible_mines == self.remaining_mines:
                for cell, states in list(self.possible.items()):
                    if 'mine' in states and len(states) > 1:
                        self.possible[cell] = {'mine'}
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
        
        # Use recursive search with propagation to determine whether the
        # assumption can lead to any valid full assignment.
        return self._search_with_board(test_board, test_possible)

    def _search_with_board(self, board: List[List[str]], possible: Dict[Tuple[int, int], Set[str]]) -> bool:
        """Recursive search with propagation. Returns True if some completion
        exists for the given board/possible state."""
        # First, propagate constraints
        if not self._propagate_with_board(board, possible):
            return False

        # Find unresolved variables (more than one possible state)
        unresolved = [cell for cell, states in possible.items() if len(states) > 1]
        if not unresolved:
            # All variables resolved; verify remaining_mines if present and
            # numeric constraints explicitly
            if self.remaining_mines is not None:
                confirmed_mines = sum(1 for rr in range(self.rows) for cc in range(self.cols)
                                      if board[rr][cc] == 'x')
                if confirmed_mines != self.remaining_mines:
                    return False

            # Verify all number cells exactly match contribution
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = board[r][c]
                    if cell == 'y':
                        base_value = 0
                    elif isinstance(cell, str) and cell.isdigit():
                        base_value = int(cell)
                    else:
                        continue
                    contrib = 0
                    for nr, nc in self.get_neighbors(r, c):
                        if board[nr][nc] == 'x':
                            if 'M' in self.rules:
                                weight = 1 if self.is_colored_cell(nr, nc) else 2
                            else:
                                weight = 1
                            contrib += weight
                    if contrib != base_value:
                        return False
            return True

        # Choose a variable with smallest domain for branching
        unresolved.sort(key=lambda c: len(possible[c]))
        cell = unresolved[0]
        states = list(possible[cell])

        for st in states:
            new_board = [row[:] for row in board]
            new_possible = deepcopy(possible)
            if st == 'mine':
                new_possible[cell] = {'mine'}
                new_board[cell[0]][cell[1]] = 'x'
            else:
                new_possible[cell] = {'safe'}
                new_board[cell[0]][cell[1]] = 'S'

            if self._search_with_board(new_board, new_possible):
                return True

        return False
    
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
                    if cell == 'y':
                        base_value = 0
                    elif isinstance(cell, str) and cell.isdigit():
                        base_value = int(cell)
                    else:
                        continue
                    required = self.get_required_mines(r, c, base_value)
                    neighbors = self.get_neighbors(r, c)

                    confirmed_contrib = 0
                    unknown_neighbors = []

                    for nr, nc in neighbors:
                        if 'M' in self.rules:
                            weight = 1 if self.is_colored_cell(nr, nc) else 2
                        else:
                            weight = 1

                        if board[nr][nc] == 'x':
                            confirmed_contrib += weight
                        elif (nr, nc) in possible:
                            unknown_neighbors.append((nr, nc, weight))

                    max_possible = confirmed_contrib + sum(w for (_, _, w) in unknown_neighbors)
                    min_possible = confirmed_contrib
                    if confirmed_contrib > required:
                        return False
                    if max_possible < required:
                        return False

                    if min_possible == required:
                        for nr, nc, _ in unknown_neighbors:
                            if (nr, nc) in possible and 'mine' in possible[(nr, nc)]:
                                possible[(nr, nc)].remove('mine')
                                if not possible[(nr, nc)]:
                                    return False
                                changed = True

                    elif max_possible == required:
                        for nr, nc, _ in unknown_neighbors:
                            if (nr, nc) in possible and 'safe' in possible[(nr, nc)]:
                                possible[(nr, nc)].remove('safe')
                                if not possible[(nr, nc)]:
                                    return False
                                changed = True
            # Apply remaining mines constraint (if specified) within this propagated context
            if self.remaining_mines is not None:
                confirmed_mines = sum(1 for rr in range(self.rows) for cc in range(self.cols)
                                      if board[rr][cc] == 'x')

                possible_mines = sum(1 for states in possible.values() if 'mine' in states)

                if confirmed_mines > self.remaining_mines:
                    return False
                if confirmed_mines + possible_mines < self.remaining_mines:
                    return False

                if confirmed_mines == self.remaining_mines:
                    for cell, states in list(possible.items()):
                        if 'safe' in states and len(states) > 1:
                            possible[cell] = {'safe'}
                            changed = True

                if confirmed_mines + possible_mines == self.remaining_mines:
                    for cell, states in list(possible.items()):
                        if 'mine' in states and len(states) > 1:
                            possible[cell] = {'mine'}
                            changed = True

        return True
    
    def solve(self) -> Optional[Tuple[int, int]]:
        """Find the next safe cell to click."""
        safe = self.find_definite_safe()
        if safe:
            return next(iter(safe))
        
        # Try hypothesis testing
        unknown_cells = list(self.possible.keys())
        # Heuristic: test cells that touch more numbered clues first
        def adj_number_count(cell):
            r, c = cell
            cnt = 0
            for nr, nc in self.get_neighbors(r, c):
                v = self.board[nr][nc]
                if v == 'y' or (isinstance(v, str) and v.isdigit()):
                    cnt += 1
            return cnt

        unknown_cells.sort(key=adj_number_count, reverse=True)
        for cell in unknown_cells:
            if not self.can_have_solution_with_assumption(cell, 'mine'):
                return cell
        
        return None

#!/usr/bin/env python3
"""
Map-based Minesweeper Solver
Reads map.txt and outputs the next move or detected mines
"""

from solver import MinesweeperSolver
import os
from pathlib import Path


class MapSolver:
    def __init__(self, map_file='map.txt'):
        """Initialize with map file."""
        self.map_file = map_file
        self.board = None
    
    def load_map(self) -> bool:
        """Load board from map.txt file."""
        if not os.path.exists(self.map_file):
            print(f"Error: {self.map_file} not found!")
            return False
        
        try:
            with open(self.map_file, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            
            if not lines:
                print("Error: map.txt is empty!")
                return False
            
            # Validate board
            first_len = len(lines[0])
            if not all(len(line) == first_len for line in lines):
                print("Error: All rows in map must have the same length!")
                return False
            
            self.board = lines
            return True
        except Exception as e:
            print(f"Error reading map.txt: {e}")
            return False
    
    def print_board(self):
        """Print the current board."""
        if not self.board:
            return
        
        print("Current board:")
        for i, row in enumerate(self.board):
            print(f"  {row}  (row {i})")
        print()
    
    def find_next_move(self):
        """Find the next safe cell to click."""
        solver = MinesweeperSolver(self.board)
        return solver.solve()
    
    def find_all_confirmed_mines(self):
        """Find all confirmed mines."""
        mines = []
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if self.board[r][c] == 'x':
                    mines.append((r, c))
        return mines
    
    def analyze(self):
        """Analyze the board and output results."""
        print("=" * 70)
        print("Minesweeper Map Solver")
        print("=" * 70)
        print()
        
        if not self.load_map():
            return False
        
        self.print_board()
        
        # Find confirmed mines
        confirmed_mines = self.find_all_confirmed_mines()
        if confirmed_mines:
            print("Confirmed mines:")
            for r, c in confirmed_mines:
                print(f"  Position ({r}, {c})")
            print()
        
        # Find next move
        next_move = self.find_next_move()
        
        if next_move:
            r, c = next_move
            print(f"Next safe cell to click: ({r}, {c})")
            print(f"  Row {r}, Column {c}")
        else:
            print("Could not determine a safe cell to click.")
            if not confirmed_mines:
                print("Hint: Try clicking any cell as a starting point.")
        
        print()
        return True


def main():
    """Main entry point."""
    solver = MapSolver('map.txt')
    solver.analyze()


if __name__ == "__main__":
    main()

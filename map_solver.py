#!/usr/bin/env python3
"""Map-based Minesweeper Solver - reads map.txt and outputs next move"""

from solver import MinesweeperSolver
import os


class MapSolver:
    def __init__(self, map_file='map.txt'):
        self.map_file = map_file
        self.board = None
        self.config_file = 'config.txt'
        self.remaining_mines = None
    
    def load_map(self) -> bool:
        """Load board from map.txt file. Last line can be remaining mines count."""
        if not os.path.exists(self.map_file):
            print(f"Error: {self.map_file} not found!")
            return False
        
        try:
            with open(self.map_file, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            
            if not lines:
                print("Error: map.txt is empty!")
                return False
            
            # Check if last non-empty line specifies remaining mines.
            # Preferred format: '# N' or '#N'. Keep bare digit as backward compatibility.
            self.remaining_mines = None
            board_lines = lines
            last = lines[-1].strip()
            if last.startswith('#'):
                rem_text = last[1:].strip()
                try:
                    self.remaining_mines = int(rem_text)
                    board_lines = lines[:-1]
                except Exception:
                    # not a valid remaining count -> treat as board line
                    board_lines = lines
            elif last.isdigit():
                # backward compatibility: a bare number on last line
                self.remaining_mines = int(last)
                board_lines = lines[:-1]
            
            if not board_lines:
                print("Error: no board data in map.txt!")
                return False

            parsed_board = []
            for line in board_lines:
                tokens = line.split()
                if len(tokens) == 1 and len(line) > 1:
                    # No spaces present, treat each character as one cell
                    parsed_board.append(list(line))
                else:
                    parsed_board.append(tokens)

            if not all(len(row) == len(parsed_board[0]) for row in parsed_board):
                print("Error: All board rows must have the same number of cells!")
                return False

            self.board = parsed_board
            return True
        except Exception as e:
            print(f"Error reading map.txt: {e}")
            return False
    
    def find_confirmed_mines(self):
        """Find all confirmed mines."""
        return [(r, c) for r in range(len(self.board)) 
                for c in range(len(self.board[0])) 
                if self.board[r][c] == 'x']
    
    def find_next_move(self):
        """Find the next safe cell to click."""
        # Pass rules and remaining mines to solver
        rules = getattr(self, 'rules', None)
        remaining = getattr(self, 'remaining_mines', None)
        return MinesweeperSolver(self.board, rules=rules, remaining_mines=remaining).solve()

    def load_config(self) -> None:
        """Load rule lines from config file into self.rules."""
        self.rules = ['V']
        if not os.path.exists(self.config_file):
            return
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                lines = [ln.strip() for ln in f.readlines() if ln.strip()]
            # Each non-empty line is a rule identifier (letters)
            parsed = []
            for ln in lines:
                # split composite rules (continuous letters) into tokens
                # e.g. "V" or "AB" -> ['V'], ['AB'] — keep as lines for now
                parsed.append(ln)
            if parsed:
                self.rules = parsed
        except Exception:
            # keep defaults on error
            pass
    
    def analyze(self):
        """Analyze and output results."""
        print("=" * 70)
        print("Minesweeper Solver")
        print("=" * 70)
        print()
        
        if not self.load_map():
            return False

        # load config (rules)
        self.load_config()

        print(f"Rules: {self.rules}")
        
        if self.remaining_mines is not None:
            print(f"Remaining mines: {self.remaining_mines}")
        
        print("Board:")
        for i, row in enumerate(self.board):
            print(f"  {' '.join(row)}  (row {i})")
        print()
        
        mines = self.find_confirmed_mines()
        if mines:
            print("Confirmed mines:")
            for r, c in mines:
                print(f"  ({r}, {c})")
            print()
        
        next_move = self.find_next_move()
        if next_move:
            r, c = next_move
            print(f"Safe cell: ({r}, {c})")
        else:
            print("Could not find safe cell.")
        
        print()
        return True


if __name__ == "__main__":
    MapSolver().analyze()

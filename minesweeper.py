import random
import re

class Board:
    def __init__(self, dim_size=10, bombs=10):
        self.dim_size = dim_size            # Size of the board (10x10 by default)
        self.bombs = bombs                  # The number of bombs
        self.dug = set()                    # Set containing spots that player already dug (stored as e.g. (0, 0))
        self.board = self.make_new_board()
        
        self.assign_values()

    def make_new_board(self):
    # Create a new board and plant the bombs in random spots.
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        bombs_planted = 0

        while bombs_planted < self.bombs:
            random_spot = random.randint(0, self.dim_size ** 2 - 1) # Select a random spot on the board
            row = random_spot // self.dim_size      # Get the row
            col = random_spot % self.dim_size    # Get the column

            if board[row][col] == "*":  # Skip if there is a bomb planted here already
                continue

            board[row][col] = "*"
            bombs_planted += 1
        
        return board

    def assign_values(self):
    # Assign values to the board that tell the player how many bombs is around the spot.
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if self.board[row][col] == "*": # If there is a bomb at this spot, we don't want to change it
                    continue
                num_neighboring_bombs = 0
                # Here we need to make sure that we don't go out of bounds of the list.
                # That's why we need to use max and min functions as below.
                for r in range(max(0, row-1), min(self.dim_size-1, row+1) + 1):
                    for c in range(max(0, col-1), min(self.dim_size-1, col+1) + 1):
                        if r == row and c == col:   # This is the spot around which we want to search
                            continue
                        if self.board[r][c] == "*":
                            num_neighboring_bombs += 1
                self.board[row][col] = num_neighboring_bombs    # Finally, assign the value to that spot
    
    def dig(self, row, col):
    # Dig at selected location.
    # Returns False if a bomb is encountered and True otherwise.
        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0:
            self.dug.add((row, col))
            return True
        # Case where self.board[row][col] == 0:
        self.dug.add((row, col))
        # Dig recursively in the neighboring spots
        for r in range(max(0, row-1), min(self.dim_size-1, row+1) + 1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1) + 1):
                if (r, c) in self.dug:
                    continue    # Don't dug in the same place twice
                self.dig(r, c)
        return True

    def check_first_move(self, row, col):
        # Ensures that first move is not a bomb
        while self.board[row][col] == "*":
            self.board = self.make_new_board()
            self.assign_values()
    
    def __str__(self):
        str_rep = " "
        # Column indices
        for (i, col) in enumerate(self.board):
            str_rep += "   "
            str_rep += str(i)   
        horizontal_bar_length = len(str_rep) + 2
        str_rep += '\n'
        # Horizontal bar
        for _ in range(horizontal_bar_length):
            str_rep += "-"
        str_rep += '\n'
        # Row indices
        for i,r in enumerate(self.board):
            str_rep += f"{i} "
            # Row content
            for j,c in enumerate(r):
                # Number represents a dug spot
                if (i, j) in self.dug:
                    if c == " ":
                        str_rep += f"| 0 "
                    else:
                        str_rep += f"| {str(c)} "
                # Space represents spots that were not dug
                else:
                    str_rep += f"|   "
            str_rep += "|\n"
        # Horizontal bar
        for _ in range(horizontal_bar_length):
            str_rep += "-"
        return str_rep
    
def play(dim_size=10, bombs=10):
    board = Board(dim_size, bombs)
    bomb_dug = False

    while len(board.dug) < board.dim_size**2 - board.bombs and not bomb_dug:
        print(board)
        user_input = re.split('(\\s)+', input("Where would you like to dig? (format: row col): "))
        # Bounds check
        try:
            if int(user_input[0]) < 0 or int(user_input[0]) >= board.dim_size or int(user_input[-1]) < 0 or int(user_input[-1]) >= board.dim_size:
                print("Wrong input. Try again.")
                continue
        except ValueError:
            print("Wrong input. Try again.")
            continue
        row = int(user_input[0])
        col = int(user_input[-1])
        # First dig cannot be a bomb
        if board.dug == set():
            board.check_first_move(row, col)
        # Check if bomb dug
        if not board.dig(int(user_input[0]), int(user_input[-1])):
            bomb_dug = True
    
    # Reveal the board
    for r in range(len(board.board)):
        for c in range(len(board.board)):
            board.dug.add((r,c))
    print(board)
    if bomb_dug:
        print("*BANG!* You lost.")
    else:
        print("Victory!")

        
if __name__ == "__main__":
    play()
    

import random
import re
# create a board object to represent the minesweeper game
# allows us to just say 'create a new board object', or
# 'dig here' or 'render this game for this object'

class Board:
    def __init__(self, dim_size, num_bombs):
        # need to keep track of these parameters for the game to work
        self.dim_size = dim_size
        self.num_bombs = num_bombs
    
        # use a set to keep track of which locations we've uncovered
        # can't use an array because that can accept duplicate values, don't want to input a location we've already dug out
        # save (row, col) tuples into this set
   
        # make the board

        self.board = self.make_new_board()  # use a method here to plant the bombs
        self.assign_values_to_squares()

        self.dug = set()    # digging at (0, 0) means that self.dug = {(0, 0)}


    def make_new_board(self):
        # constructs a board based on dim size and number of bombs
        
        # generate a new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # now plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:

            location = random.randint(0, self.dim_size**2 - 1)  # returns a random integer s.t. a <= N <= b

            row = location // self.dim_size # want the no. of times dim_size goes into location to tell us which row to plant the bomb
            col = location % self.dim_size # want the remainder to tell us which index in the row the bomb should be planted in

            if board[row][col] == '*':
                continue    # means we've already planted a bomb here

            board[row][col] = '*'
            bombs_planted += 1

        return board
    
    def assign_values_to_squares(self):
        # planted the bombs, now need to assign a number from 0 - 8 for all the empty spaces
        # numbers shown on a square represent how many neighbouring squares have bombs on them
         
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    continue
                self.board[r][c] = self.get_num_neighbouring_bombs(r, c)

    def get_num_neighbouring_bombs(self, row, col):
        # iterate through each of the neighbouring positions and sum the number of bombs
        num_neighbouring_bombs = 0

        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                
                # don't need to check the square we're passing through the function
                if r == row and c == col:
                    continue
                

                if self.board[r][c] == "*":
                    num_neighbouring_bombs += 1

        return num_neighbouring_bombs
    
    def dig(self, row, col):
        # dig at the location
        # return True if successful, False if a bomb is found

        # few scenarios:
            # hit a bomb -> game over
            # dig at a location with neighbouring bombs -> finish dig
            # dig at a location with no neighbouring bombs -> recursively dig neighbours

        self.dug.add((row, col))    # keep track of which squares have been dug

        if self.board[row][col] == '*':
            return False

        elif self.board[row][col] > 0:
            return True
        
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):

                if (r, c) in self.dug:
                    continue

                self.dig(r, c)

        return True
    
    def __str__(self):  # copy-pasted, idk what this does
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return a string that shows the board to the player

        # first let's create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


# call this function to play the game
def play(dim_size = 10, num_bombs = 10):
    # 1. create the board and plant the bombs
    board = Board(dim_size, num_bombs)

    # 2. show the user the board and ask them where they want to dig
    # 3. when the user says where they want to dig:
        # 3a. if the location is a bomb, show the game over message 
        #     and end the game
        # 3b. if the location isn't a bomb, dig recursively until 
        #     each square is at least next to a bomb
    # 4. repeats steps 2 and 3 until there are no more places to dig, then the game is won
    safe = True

    while len(board.dug) < board.dim_size**2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as 'row, column':    "))

        row, col = int(user_input[0]), int(user_input[-1])

        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print("Invalid location, try again")
            continue
        
        # if its safe, we dig
        safe = board.dig(row, col)
        if not safe:
            break   # game over

    if safe:
        print("You Win!")
    else:
        print("Game Over!")
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__':
    play()
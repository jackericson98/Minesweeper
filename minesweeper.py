# Code by: Jack Ericson
# Date: 02/22/2022
# GSU DSCI 1302 Assignment 2

# Imports
import numpy as np


# Define the game class
class Minesweeper:
    # Initialize with rows, columns, and difficulty
    def __init__(self, rows=10, cols=6, difficulty=1):
        # row and col used to manage the row/col currently being explored
        self.row = None
        self.col = None
        # Holds the number of rows and columns in the game
        self.rows = rows
        self.cols = cols
        # Builds the board for the game and stores which values are mines
        self.boardArray = np.random.normal(1, 1, size=(rows, cols))
        # Stores which cells have been checked
        self.boardList = [['▢'] * cols for i in range(rows)]

        # Variable to shut down the game if a bomb is found
        self.playing = True
        # Create the game
        self.initiate()
        # Formula for converting difficulties (1-5) to a difficulty that makes sens mathematically
        self.difficulty = 1 / difficulty + 0.5

    def initiate(self):
        """Used to start the game and change settings"""

        # Defining a mean which will work as a difficulty scale from
        print("Welcome to Minesweeper! \n")
        start = input("Would you like to play?\n")

        # When the user says yes to playing, build the board and then play the game
        if start.lower() == 'y':
            self.build_board()
            self.play()

        # If the user selects no then end the game
        elif start.lower() == 'n':
            print("Ok ... Goodbye!")

        # Give an error if the user inputs something other then y or n and then restart initiate method
        else:
            print("That is not a valid answer. Please enter Y or N")
            self.initiate()

    # Main playing method
    def play(self):
        # Keep repeating the loop until the game ends
        while self.playing:
            # Print board
            print('\n'.join([''.join(['{:5}'.format(item) for item in row]) for row in self.boardList]))

            # Go through entire board to check if the user has won
            bombs = 0
            checked = 0
            for row in range(len(self.boardList)):
                for col in range(len(self.boardList[row])):
                    # If the cell is not checked and the value is a bomb add a bomb
                    if self.boardList[row][col] == '▢' and self.boardArray[row][col] < 0:
                        bombs += 1
                    # Count the number of checked cells
                    elif self.boardList[row][col] != '▢':
                        checked += 1
            # If the number of bombs and checked cells adds up to the total number of cells the user wins
            if bombs + checked == len(self.boardList) * len(self.boardList[0]):
                self.you_win()

            # Ask the user for the row and column they want to check next
            row = int(input("Choose a row:\n")) - 1
            col = int(input("Choose a column:\n")) - 1

            # If the cell has been checked already give an error and restart
            if self.boardList[row][col] != '▢':
                print('This square has already been chosen. Please choose another.')
                self.play()
            # If the inputs are outside of the range of columns and rows give an error and restart
            elif row >= len(self.boardList) or col >= len(self.boardList):
                print("This row or column is of our board's range")
                self.play()
            # Otherwise set the current column and row
            else:
                self.row = row
                self.col = col
            # Check the current column and row
            self.check()

        # When the game ends thank the user
        print("Thanks for playing!")

    # Method for checking the current row and column
    def check(self):
        #
        if not self.boardList[self.row][self.col] == '▢' and not self.boardArray[self.row][self.col] > 0:
            self.you_win()
        # If the row/col is a bomb run you_lose
        if self.boardArray[self.row][self.col] < 0:
            self.you_lose()
        # Continuing the game
        else:
            self.update_board()

    # Method for building the board
    def build_board(self):
        # If the user wants to adjust the game parameters they can here
        changes = input("Do you want to adjust the number of rows, number of columns or difficulty? (Default: "
                        "rows = 10, columns = 6, difficulty = easy)\n")
        # Making changes
        if changes.lower() == 'y':
            # Ask for a difficulty rating between 1 and 5
            self.difficulty = input("Choose a difficulty level between 1 and 5:\n")
            # Ask fof rows and columns
            self.rows = int(input("How many rows?\n"))
            self.cols = int(input("How many columns?\n"))
        # If no changes are requested go with the default settings
        elif changes.lower() == 'n':
            self.difficulty = 1
            self.rows = 10
            self.cols = 6
        # Error for the user inputting a non valid input
        else:
            print("\"{}\" is not a valid input. Please try again.".format(changes))
            self.build_board()

        # Set up the board and playing
        mean = 1 / float(self.difficulty) + 0.5
        self.boardArray = np.random.normal(mean, 1, size=(self.rows, self.cols))
        self.boardList = [['▢'] * self.cols for i in range(self.rows)]

    # Method for updating the board everytime there is a new cell to check
    def update_board(self):
        """A tool used to
         update the users board"""
        cell_num = 0
        row_range = col_range = range(3)

        # Creating new ranges to cover our edge cases
        if self.row == 0:
            row_range = range(1, 3)
        if self.col == 0:
            col_range = range(1, 3)
        if self.row == len(self.boardArray) - 1:
            row_range = range(2)
        if self.col == len(self.boardArray[0]) - 1:
            col_range = range(2)

        # Check all surrounding cells in our ranges
        for i in row_range:
            for j in col_range:
                # This covers our row and column case
                if i == 1 and j == 1:
                    pass
                # For the
                elif self.boardArray[self.row + i - 1][self.col + j - 1] < 0:
                    cell_num += 1
        self.boardList[self.row][self.col] = str(cell_num)

    # Method to indicate to the user that they have lost
    def you_lose(self):

        # You hit a bomb
        print("""
                        ██████╗░░█████╗░░█████╗░███╗░░░███╗██╗
                        ██╔══██╗██╔══██╗██╔══██╗████╗░████║██║
                        ██████╦╝██║░░██║██║░░██║██╔████╔██║██║
                        ██╔══██╗██║░░██║██║░░██║██║╚██╔╝██║╚═╝
                        ██████╦╝╚█████╔╝╚█████╔╝██║░╚═╝░██║██╗
                        ╚═════╝░░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝
                        \n\n                        You lose! \n\n""")
        # Give the user the option to play again
        play_again = input("Would you like to play again?\n")
        if play_again.lower() == 'y':
            # Play again
            self.build_board()
            self.play()
        else:
            self.playing = False
    # Method to let the user know they have won
    def you_win(self):
        print("""
                ██╗░░░██╗░█████╗░██╗░░░██╗
                ╚██╗░██╔╝██╔══██╗██║░░░██║
                ░╚████╔╝░██║░░██║██║░░░██║
                ░░╚██╔╝░░██║░░██║██║░░░██║
                ░░░██║░░░╚█████╔╝╚██████╔╝
                ░░░╚═╝░░░░╚════╝░░╚═════╝░
                ░██╗░░░░░░░██╗██╗███╗░░██╗██╗
                ░██║░░██╗░░██║██║████╗░██║██║
                ░╚██╗████╗██╔╝██║██╔██╗██║██║
                ░░████╔═████║░██║██║╚████║╚═╝
                ░░╚██╔╝░╚██╔╝░██║██║░╚███║██╗
                ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝╚═╝\n""")
        # Give the user the option to play again
        play_again = input("Would you like to play again?")
        # Play again
        if play_again.lower() == 'y':
            self.initiate()
        else:
            self.playing = False


x = Minesweeper()

"""
File:  frogger.py
Author:  Bliss Phinehas
Date:    11/29/2024
Section: 49
E-mail:  blissp1@umbc.edu
Description:
  This program simulates an internet with servers, allowing you to ping,
  traceroute, and connect servers while handling basic IPv4 validation.
"""
import os

# Constants
SAFE_ROW = '_'
CAR = 'X'
FROG_SYMBOL = '\U0001318F'  # Egyptian hieroglyphic frog
MOVES = {'W': (-1, 0), 'A': (0, -1), 'S': (1, 0), 'D': (0, 1)}



def select_game_file():
    """
    Displays available .frog files and allows the user to select one by index.

    Returns:
        str: The selected filename.
    """
    root, directories, files = next(os.walk('../PROJECT1'))

    # Filter the list to only include files with the .frog extension
    frog_files = [f for f in files if f.endswith('.frog')]

    if not frog_files:
        print("No .frog files found. Please add one to the directory.")
        exit()

    for i, f in enumerate(frog_files, 1):
        print(f"[{i}]  {f}")

    while True:
        choice = input("Enter an option: ")
        if choice.isdigit() and 1 <= int(choice) <= len(frog_files):
            return frog_files[int(choice) - 1]
        print("Invalid choice. Try again.")

def load_game(file_name):
    """
    Loads the game data from a specified file.

    Args:
        file_name (str): The name of the file to load.

    Returns:
        tuple: Dimensions (rows, cols, jumps), speeds, and the game board.
    """
    try:
        with open(file_name, 'r') as f:
            lines = f.read().strip().split('\n')
        dimensions = list(map(int, lines[0].split()))
        speeds = list(map(int, lines[1].split()))
        board = [list(row) for row in lines[2:]]
        return dimensions, speeds, board
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit()
    except (ValueError, IndexError):
        print("Error: Invalid file format. Ensure it contains valid game data.")
        exit()

def display_board(board, frog_position):
    """
    Displays the game board with the frog's position.

    Args:
        board (list): The game board.
        frog_position (tuple): The frog's current position (row, col).
    """
    print("\nCurrent Board:")
    for r, row in enumerate(board):
        for c, char in enumerate(row):
            if (r, c) == frog_position:
                print(FROG_SYMBOL, end='')
            else:
                print(char, end='')
        print()

def is_valid_position(board, position):
    """
    Checks if a position is valid on the board.

    Args:
        board (list): The game board.
        position (tuple): The position to check.

    Returns:
        bool: True if valid, False otherwise.
    """
    rows, cols = len(board), len(board[0])
    row, col = position
    return 0 <= row < rows and 0 <= col < cols

def move_frog(frog_position, move, board):
    """
    Updates the frog's position based on user input.

    Args:
        frog_position (tuple): Current position (row, col).
        move (str): The user input for movement.
        board (list): The game board.

    Returns:
        tuple: The new position of the frog.
    """
    if move.upper() == 'J':
        try:
            _, new_row, new_col = input("Enter jump position (row col): ").split()
            new_pos = (int(new_row), int(new_col))
        except ValueError:
            print("Invalid jump command.")
            return frog_position
    else:
        dr, dc = MOVES.get(move.upper(), (0, 0))
        new_pos = (frog_position[0] + dr, frog_position[1] + dc)

    if is_valid_position(board, new_pos):
        if board[new_pos[0]][new_pos[1]] == SAFE_ROW:
            return new_pos
        print("Collision! You lose.")
        exit()
    print("Invalid move. Stay within bounds.")
    return frog_position

def rotate_cars(board, speeds):
    """
    Rotates each row of cars based on their speed.

    Args:
        board (list): The game board.
        speeds (list): List of speeds for each row.
    """
    for i, speed in enumerate(speeds):
        if CAR in board[i]:
            board[i] = board[i][-speed:] + board[i][:-speed]

def play_turn(board, frog_position, speeds):
    """
    Handles a single turn in the game.
    Updates the board, frog position, and checks for game status.

    Args:
        board (list): The game board.
        frog_position (tuple): The frog's current position.
        speeds (list): Speeds for each row.

    Returns:
        tuple: Updated frog position and a boolean indicating win status.
    """
    display_board(board, frog_position)
    move = input("Enter movement (WASD for directions, J for jump): ").strip().upper()

    if move not in MOVES and move != 'J':
        print("Invalid input. Use W, A, S, D, or J.")
        return frog_position, False

    new_position = move_frog(frog_position, move, board)

    if new_position[0] == len(board) - 1:
        return new_position, True

    rotate_cars(board, speeds)
    return new_position, False

def frogger_game(file_name):
    """
    Main game loop for Frogger.

    Args:
        file_name (str): The name of the game file to load.
    """
    dimensions, speeds, board = load_game(file_name)
    _, cols, _ = dimensions
    frog_position = (0, cols // 2)
    game_running = True

    print("Welcome to Frogger!")
    while game_running:
        try:
            frog_position, has_won = play_turn(board, frog_position, speeds)
            if has_won:
                print("Congratulations! The frog safely crossed the road.")
                game_running = False
        except Exception as e:
            print(f"An error occurred: {e}")
            game_running = False

if __name__ == '__main__':
    try:
        selected_game_file = select_game_file()
        frogger_game(selected_game_file)
    except Exception as e:
        print(f"Game could not start: {e}")

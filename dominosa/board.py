def load_board(path: str) -> list[list[int]]:
    """
    Load a Dominosa board from a text file.

    Each line in the file represents one row of the board and contains whitespace-separated integers.
    The resulting board is returned as a list of lists (2D array).
    """
    board = []
    with open(path, 'r') as file:
        for line in file:
            row = [int(x) for x in line.split()]
            board.append(row)
    return board

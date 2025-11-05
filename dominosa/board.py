def load_board(path: str) -> list[list[int]]:
    board = []
    with open(path, 'r') as file:
        for line in file:
            row = [int(x) for x in line.split()]
            board.append(row)
    return board


if __name__ == "__main__":
    board = load_board("../puzzles/dom03.txt")
    print(board)

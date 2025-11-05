from board import load_board


def generate_dominos(board: list[list[int]]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    dominos = []
    rows, cols = len(board), len(board[0])

    for row in range(rows):
        for col in range(cols):
            if col + 1 < cols:  # right neighbor cell
                dominos.append(((row, col), (row, col + 1)))
            if row + 1 < rows:  # bottom neighbor cell
                dominos.append(((row, col), (row + 1, col)))

    return dominos


def create_pair_map(dominos: list[tuple[tuple[int, int], tuple[int, int]]]) -> dict[tuple[int, int], list[tuple[tuple[int, int], tuple[int, int]]]]:
    pair_to_dominos = {}
    for x in range(len(board[0])):
        for y in range(x, len(board[0])):
            pair_to_dominos[(x, y)] = []

    for domino in dominos:
        (r1, c1), (r2, c2) = domino
        val1, val2 = board[r1][c1], board[r2][c2]
        pair = tuple(sorted((val1, val2)))
        pair_to_dominos[pair].append(domino)

    return pair_to_dominos


def create_cell_map(dominos: list[tuple[tuple[int, int], tuple[int, int]]]) -> dict[tuple[int, int], list[tuple[tuple[int, int], tuple[int, int]]]]:
    cell_to_dominos = {}
    for row in range(len(board)):
        for col in range(len(board[0])):
            cell_to_dominos[(row, col)] = []

    for domino in dominos:
        cell_to_dominos[domino[0]].append(domino)
        cell_to_dominos[domino[1]].append(domino)

    return cell_to_dominos


if __name__ == "__main__":
    board = load_board("../puzzles/dom03.txt")
    print(board)
    print("")
    dominos = generate_dominos(board)
    print(dominos)
    print("")
    pair_map = create_pair_map(dominos)
    print(pair_map)
    print("")
    cell_map = create_cell_map(dominos)
    print(cell_map)

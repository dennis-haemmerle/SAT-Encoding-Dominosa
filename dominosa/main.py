from board import load_board
from generator import generate_board
from constraints import generate_dominos, create_pair_map, create_cell_map
from clauses import create_clauses, solve, check_solution


def run_solver(n: int | None = None, path: str | None = None, error: bool = False, verbose: bool = False):
    # argument validation
    if (n is None) == (path is None):
        raise ValueError("Exactly one of 'n' or 'path' must be provided.")

    # load or generate board
    if path is not None:
        board = load_board(path)
    if n is not None:
        board = generate_board(n, error)
    if verbose:
        print("Board generated!")

    # constraints
    dominos = generate_dominos(board)
    pair_map = create_pair_map(dominos, board)
    cell_map = create_cell_map(dominos, board)
    if verbose:
        print("Constraints created!")

    # clauses
    clauses = create_clauses(dominos, pair_map, cell_map)
    if verbose:
        print("Clauses created!")

    # SAT solver
    assignment = solve(clauses)
    if verbose:
        print("Solved!")

    # checker
    if assignment:
        check = check_solution(assignment, dominos, pair_map, cell_map)
        if verbose:
            print(f"Check: {check}")
    elif verbose:
        print("No solution!")


if __name__ == "__main__":
    run_solver(path="puzzles/dom03.txt")
    run_solver(n=30, verbose=True)
    print()
    run_solver(n=30, error=True, verbose=True)

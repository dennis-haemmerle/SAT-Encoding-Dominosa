from board import load_board
import constraints
from pysat.card import CardEnc  # Encoder
from pysat.formula import IDPool  # Variables
from pysat.solvers import Solver  # Solver

Domino = tuple[tuple[int, int], tuple[int, int]]


def create_clauses(dominos: list[Domino], pair_map: dict[tuple[int, int], list[Domino]], cell_map: dict[tuple[int, int], list[Domino]]) -> list[list[int]]:
    """
    Generate CNF clauses encoding the Dominosa constraints.

    - Each value pair appears in exactly one domino.
    - Each board cell is covered by exactly one domino.
    """
    vpool = IDPool()
    clauses = []

    for d in dominos:
        vpool.id(d)

    for pair, dominos in pair_map.items():
        lits = [vpool.id(domino) for domino in dominos]
        if len(lits) == 1:
            clauses.append(lits)
        else:
            block = CardEnc.equals(lits=lits, vpool=vpool, encoding=0)  # exactly one, pairwise encoding
            clauses.extend(block.clauses)

    for cell, dominos in cell_map.items():
        lits = [vpool.id(domino) for domino in dominos]
        if len(lits) == 1:
            clauses.append(lits)
        else:
            block = CardEnc.equals(lits=lits, vpool=vpool, encoding=0,)  # exactly one, pairwise encoding
            clauses.extend(block.clauses)

    return clauses


def solve(clauses: list[list[int]]):
    """Solve a CNF formula (list of clauses) using a SAT solver."""
    solver = Solver(name="Cadical195")

    for clause in clauses:
        solver.add_clause(clause)

    result = solver.solve()

    print("SAT:", result)

    if result:
        model = solver.get_model()
        print("Model:", model)
        return model


def check_solution(assignment, dominos: list[Domino], pair_map: dict[tuple[int, int], list[Domino]], cell_map: dict[tuple[int, int], list[Domino]]) -> bool:
    """
    Verify that a given SAT assignment satisfies all Dominosa constraints.

    Checks that each value pair and each board cell is covered by exactly one selected domino.
    """
    vpool = IDPool()

    for d in dominos:
        vpool.id(d)

    for pair, dominos in pair_map.items():
        assigned = [d for d in dominos if vpool.id(d) in assignment]
        if len(assigned) != 1:
            return False

    for cell, dominos in cell_map.items():
        assigned = [d for d in dominos if vpool.id(d) in assignment]
        if len(assigned) != 1:
            return False

    return True


if __name__ == "__main__":
    board = load_board("../puzzles/dom02.txt")
    dominos = constraints.generate_dominos(board)
    pair_map = constraints.create_pair_map(dominos, board)
    cell_map = constraints.create_cell_map(dominos, board)

    clauses = create_clauses(dominos, pair_map, cell_map)
    print(clauses)
    print("")
    assignment = solve(clauses)
    check = check_solution(assignment, dominos, pair_map, cell_map)
    print(f"Check: {check}")

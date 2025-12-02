from board import load_board
import constraints
from pysat.card import CardEnc  # Encoder
from pysat.formula import IDPool  # Variables
from pysat.solvers import Solver  # Solver

Domino = tuple[tuple[int, int], tuple[int, int]]


def create_clauses(dominos: list[Domino], pair_map: dict[tuple[int, int], list[Domino]], cell_map: dict[tuple[int, int], list[Domino]]) -> list[list[int]]:
    vpool = IDPool()
    clauses = []

    for d in dominos:
        vpool.id(d)

    for pair, dominos in pair_map.items():
        lits = [vpool.id(domino) for domino in dominos]
        if len(lits) == 1:
            clauses.append(lits)
        else:
            # block = CardEnc.equals(lits=lits, vpool=vpool, encoding=0)  # exactly one, pairwise encoding
            # clauses.extend(block.clauses)
            block = CardEnc.atmost(lits=lits, bound=1, vpool=vpool, encoding=0)
            clauses.extend(block.clauses)
            block = CardEnc.atleast(lits=lits, vpool=vpool, bound=1)
            clauses.extend(block.clauses)

    for cell, dominos in cell_map.items():
        lits = [vpool.id(domino) for domino in dominos]
        if len(lits) == 1:
            clauses.append(lits)
        else:
            # block = CardEnc.equals(lits=lits, vpool=vpool, encoding=0,)  # exactly one, pairwise encoding
            block = CardEnc.atmost(lits=lits, bound=1, vpool=vpool, encoding=0)
            clauses.extend(block.clauses)
            block = CardEnc.atleast(lits=lits, bound=1, vpool=vpool)
            clauses.extend(block.clauses)

    return clauses


def solve(clauses: list[list[int]]):
    solver = Solver(name="Cadical195")

    for clause in clauses:
        solver.add_clause(clause)

    result = solver.solve()

    print("SAT:", result)

    if result:
        model = solver.get_model()
        print("Model:", model)


if __name__ == "__main__":
    board = load_board("../puzzles/dom02.txt")
    dominos = constraints.generate_dominos(board)
    pair_map = constraints.create_pair_map(dominos, board)
    cell_map = constraints.create_cell_map(dominos, board)

    clauses = create_clauses(dominos, pair_map, cell_map)
    print(clauses)
    print("")
    solve(clauses)

import networkx as nx
import random

Domino = tuple[tuple[int, int], tuple[int, int]]


def generate_board(n: int) -> list[list[int]]:
    """Generate a complete Dominosa board of size n x (n+1)"""
    dominos = minimum_weight_perfect_matching(n)
    board = assign_dominos(n, dominos)
    return board


def minimum_weight_perfect_matching(n: int) -> list[Domino]:
    """
    Compute a minimum-weight perfect matching on an n x (n+1) bipartite grid
    using a min-cost max-flow approach with random edge weights.
    Each matched edge corresponds to one domino placement.
    """
    G = nx.DiGraph()

    G.add_node("S")  # Source
    G.add_node("T")  # Sink

    # Add edges from source to black cells and from white cells to sink
    for row in range(n):
        for col in range(n + 1):
            if is_black(row, col):
                # Source "S" -> black cell "b"
                G.add_edge("S", ("b", row, col), capacity=1, weight=0)
            else:
                # white cell "w" -> Sink "T"
                G.add_edge(("w", row, col), "T", capacity=1, weight=0)

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Black -> white edges represent possible domino placements
    for row in range(n):
        for col in range(n + 1):
            if not is_black(row, col):
                continue

            for drow, dcol in directions:
                nrow, ncol = row + drow, col + dcol
                if 0 <= nrow < n and 0 <= ncol < n + 1:
                    if not is_black(nrow, ncol):
                        # black cell "b" -> white cell "w"
                        weight = random.randint(1, 1000)
                        G.add_edge(("b", row, col), ("w", nrow, ncol), capacity=1, weight=weight)

    # Number of dominos
    N = n * (n + 1) // 2

    # Enforce maximum flow through node demands
    G.nodes["S"]["demand"] = -N
    G.nodes["T"]["demand"] = N

    for node in G.nodes:
        if node not in ("S", "T"):
            G.nodes[node]["demand"] = 0

    # Solve min-cost max-flow
    flow_dict = nx.min_cost_flow(G)

    dominos = []

    # Extract the matching
    for row in range(n):
        for col in range(n + 1):
            if not is_black(row, col):
                continue

            for edge, flow in flow_dict[("b", row, col)].items():
                if flow == 1 and edge[0] == "w":
                    dominos.append(((row, col), (edge[1], edge[2])))

    assert len(dominos) == N

    # Initialize grid for ilustration
    grid = [['.' for _ in range(n + 1)] for _ in range(n)]

    # Place dominos on the grid
    x = 0
    for domino in dominos:
        (r1, c1), (r2, c2) = domino
        grid[r1][c1] = str(x)
        grid[r2][c2] = str(x)
        x += 1

    # Print grid
    for row in range(n):
        print(' '.join(grid[row]))

    return dominos


def assign_dominos(n: int, dominos: list[Domino]) -> list[list[int]]:
    """Assign domino values to the given domino placements and build the board"""
    board = [[-1 for _ in range(n + 1)] for _ in range(n)]
    domino_values = [(x, y) for x in range(n) for y in range(x, n)]
    random.shuffle(domino_values)
    random.shuffle(dominos)

    for domino, value in zip(dominos, domino_values):
        (r1, c1), (r2, c2) = domino
        a, b = value

        if random.random() < 0.5:
            a, b = b, a

        board[r1][c1] = a
        board[r2][c2] = b

    return board


def is_black(row: int, col: int) -> bool:
    """Chessboard coloring to obtain a bipartite grid"""
    return (row + col) % 2 == 0


if __name__ == "__main__":
    board = generate_board(3)
    for row in board:
        print(row)

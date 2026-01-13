import time
import random
import statistics
import matplotlib.pyplot as plt

from main import run_solver
from generator import generate_board
from constraints import generate_dominos, create_pair_map, create_cell_map
from clauses import create_clauses, solve


def benchmark(max_n: int, step: int = 1, seeds: list[int] = [42, 43, 44]):
    ns = range(2, max_n + 1, step)
    median_total_times = []
    median_generator_times = []
    median_solver_times = []

    for n in ns:
        total_times = []
        generator_times = []
        solver_times = []

        for seed in seeds:
            random.seed(seed)

            # === Full process ===
            t_start = time.perf_counter()

            # --- Generator only ---
            t_generator_start = time.perf_counter()
            board = generate_board(n)
            t_generator_end = time.perf_counter()
            # ----------------------

            # Encoding
            dominos = generate_dominos(board)
            pair_map = create_pair_map(dominos, board)
            cell_map = create_cell_map(dominos, board)
            clauses = create_clauses(dominos, pair_map, cell_map)

            # --- Solver only ---
            t_solver_start = time.perf_counter()
            solve(clauses)
            t_solver_end = time.perf_counter()
            # -------------------

            t_end = time.perf_counter()
            # ====================

            generator_times.append(t_generator_end - t_generator_start)
            solver_times.append(t_solver_end - t_solver_start)
            total_times.append(t_end - t_start)

        # compute medians across seeds
        median_total = statistics.median(total_times)
        median_generator = statistics.median(generator_times)
        median_solver = statistics.median(solver_times)

        median_total_times.append(median_total)
        median_generator_times.append(median_generator)
        median_solver_times.append(median_solver)

        print(f"{n}, {median_total:.6f}, {median_generator:.6f}, {median_solver:.6f}")

    plt.plot(ns, median_total_times, label="Full Process")
    plt.plot(ns, median_generator_times, label="Generator only")
    plt.plot(ns, median_solver_times, label="Solver only")
    plt.xlabel("n")
    plt.ylabel("Time (s)")
    # plt.yscale("log")
    plt.legend()
    plt.title(f"Benchmark medians over seeds={seeds}")
    plt.show()


def benchmark_generator(max_n: int, step: int = 1, seeds: list[int] = [42, 43, 44]):
    ns = range(2, max_n + 1, step)
    median_times = []

    for n in ns:
        generator_times = []

        for seed in seeds:
            random.seed(seed)

            # --- Generator only ---
            t_start = time.perf_counter()
            generate_board(n)
            t_end = time.perf_counter()
            generator_times.append(t_end - t_start)
            # ----------------------

        # compute medians across seeds
        median_generator = statistics.median(generator_times)
        median_times.append(median_generator)

        print(f"{n}, {median_generator:.6f}")

    plt.plot(ns, median_times)
    plt.xlabel("n")
    plt.ylabel("Time (s)")
    # plt.yscale("log")
    plt.title(f"Benchmark Generator medians over seeds={seeds}")
    plt.show()


if __name__ == "__main__":
    # benchmark(max_n=55, step=1, seeds=[1, 10, 100])
    benchmark_generator(max_n=100, step=1, seeds=[1, 10, 100])

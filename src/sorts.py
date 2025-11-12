
import random
import time
import os
import argparse
from typing import List, Tuple

# Matplotlib (no styles/colors specified)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def insertion_sort(arr: List[int]) -> List[int]:
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def merge_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left: List[int], right: List[int]) -> List[int]:
    i = j = 0
    result = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:]); result.extend(right[j:])
    return result

def benchmark(sizes=None, trials: int = 5, vary_per_trial: bool = False, seed: int = None):
    if seed is not None:
        random.seed(seed)
    if sizes is None:
        sizes = [200, 400, 800, 1600, 3200, 6400]
    results = []
    for n in sizes:
        base_data = [random.randint(0, 10_000_000) for _ in range(n)]
        t0 = 0.0
        t1 = 0.0
        for _ in range(trials):
            if vary_per_trial:
                data = [random.randint(0, 10_000_000) for _ in range(n)]
            else:
                data = base_data
            d = data[:]
            start = time.perf_counter()
            insertion_sort(d)
            t0 += (time.perf_counter() - start)
            d = data[:]
            start = time.perf_counter()
            merge_sort(d)
            t1 += (time.perf_counter() - start)
        t0 /= trials
        t1 /= trials
        results.append((n, t0, t1))
    return results

def write_csv(path: str, rows):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("n,insertion,merge\n")
        for n, ti, tm in rows:
            f.write(f"{int(n)},{ti:.6f},{tm:.6f}\n")

def save_png(rows, out_path: str, dpi: int = 200, grid: bool = False):
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    xs = [n for (n, _, _) in rows]
    ys0 = [ti for (_, ti, _) in rows]
    ys1 = [tm for (_, _, tm) in rows]
    plt.figure()
    plt.plot(xs, ys0, marker="o", label="Insertion Sort")
    plt.plot(xs, ys1, marker="o", label="Merge Sort")
    plt.xlabel("n (tamaño de la lista)")
    plt.ylabel("Tiempo promedio (s)")
    plt.title("Insertion vs Merge — Tiempos promedio")
    if grid:
        plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=dpi)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark Insertion vs Merge (CSV y PNG).")
    parser.add_argument("--out", type=str, default="", help="Ruta del CSV de salida (p.ej., data/sort_benchmark.csv)")
    parser.add_argument("--trials", type=int, default=5, help="Corridas por tamaño para promediar")
    parser.add_argument("--sizes", type=int, nargs="*", default=[200,400,800,1600,3200,6400], help="Tamaños n a evaluar")
    parser.add_argument("--png", type=str, default="", help="Ruta del PNG (p.ej., figs/fig_sort_tiempos.png).")
    parser.add_argument("--dpi", type=int, default=200, help="Resolución del PNG")
    parser.add_argument("--grid", action="store_true", help="Mostrar grilla en el gráfico")
    parser.add_argument("--seed", type=int, default=None, help="Semilla para aleatoriedad (reproducible)")
    parser.add_argument("--vary-per-trial", action="store_true", help="Usar datos nuevos en cada trial")
    args = parser.parse_args()

    res = benchmark(sizes=args.sizes, trials=args.trials, vary_per_trial=args.vary_per_trial, seed=args.seed)

    for n, ti, tm in res:
        print(f"{n},{ti:.6f},{tm:.6f}")

    if args.out:
        write_csv(args.out, res)

    if args.png:
        save_png(res, args.png, dpi=args.dpi, grid=args.grid)


import random
import time
import os
import argparse
from typing import List, Tuple

# Matplotlib (no styles/colors specified)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def dp_knapsack(values: List[int], weights: List[int], W: int) -> int:
    n = len(values)
    dp = [0] * (W + 1)
    for i in range(n):
        w = weights[i]
        v = values[i]
        for cap in range(W, w - 1, -1):
            cand = dp[cap - w] + v
            if cand > dp[cap]:
                dp[cap] = cand
    return dp[W]

def greedy_knapsack(values: List[int], weights: List[int], W: int) -> int:
    items = list(range(len(values)))
    items.sort(key=lambda i: values[i] / weights[i], reverse=True)
    total = 0
    cap = 0
    for i in items:
        if cap + weights[i] <= W:
            cap += weights[i]
            total += values[i]
    return total

def random_instance(n: int, w_low=1, w_high=50, v_low=1, v_high=100):
    weights = [random.randint(w_low, w_high) for _ in range(n)]
    values = [random.randint(v_low, v_high) for _ in range(n)]
    return values, weights

def runtime_vs_n(W=1000, trials=5, ns=None, seed=None, same_instance_per_n=False, w_low=1, w_high=50, v_low=1, v_high=100):
    if seed is not None:
        random.seed(seed)
    if ns is None:
        ns = [20, 30, 40, 50, 60, 70]
    rows = []
    for n in ns:
        t_dp = 0.0
        t_gr = 0.0
        if same_instance_per_n:
            base_v, base_w = random_instance(n, w_low, w_high, v_low, v_high)
        for _ in range(trials):
            if same_instance_per_n:
                v, w = base_v, base_w
            else:
                v, w = random_instance(n, w_low, w_high, v_low, v_high)
            start = time.perf_counter()
            _ = dp_knapsack(v, w, W)
            t_dp += (time.perf_counter() - start)
            start = time.perf_counter()
            _ = greedy_knapsack(v, w, W)
            t_gr += (time.perf_counter() - start)
        rows.append((n, t_dp / trials, t_gr / trials))
    return rows

def runtime_dp_vs_W(n=50, Ws=None, seed=None, w_low=1, w_high=50, v_low=1, v_high=100, same_instance_across_W=True):
    if seed is not None:
        random.seed(seed)
    if Ws is None:
        Ws = [100, 200, 400, 800, 1200]
    if same_instance_across_W:
        v, w = random_instance(n, w_low, w_high, v_low, v_high)
    rows = []
    for W in Ws:
        if not same_instance_across_W:
            v, w = random_instance(n, w_low, w_high, v_low, v_high)
        start = time.perf_counter()
        _ = dp_knapsack(v, w, W)
        t = time.perf_counter() - start
        rows.append((W, t))
    return rows

def quality_greedy(W=800, ns=None, trials=20, seed=None, w_low=1, w_high=50, v_low=1, v_high=100, same_instance_per_n=False):
    if seed is not None:
        random.seed(seed)
    if ns is None:
        ns = [20, 30, 40, 50]
    rows = []
    for n in ns:
        ratios = []
        if same_instance_per_n:
            base_v, base_w = random_instance(n, w_low, w_high, v_low, v_high)
        for _ in range(trials):
            if same_instance_per_n:
                v, w = base_v, base_w
            else:
                v, w = random_instance(n, w_low, w_high, v_low, v_high)
            opt = dp_knapsack(v, w, W)
            gr = greedy_knapsack(v, w, W)
            if opt > 0:
                ratios.append(gr / opt)
        rows.append((n, sum(ratios) / len(ratios)))
    return rows

def write_csv(path: str, header: str, rows):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + "\n")
        for t in rows:
            f.write(",".join([str(x if not isinstance(x, float) else f"{x:.6f}") for x in t]) + "\n")

def plot_n(rows, out_path: str, dpi: int = 200, grid: bool = False):
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    xs = [n for (n, _, _) in rows]
    ys_dp = [tdp for (_, tdp, _) in rows]
    ys_gr = [tgr for (_, _, tgr) in rows]
    plt.figure()
    plt.plot(xs, ys_dp, marker="o", label="DP (óptimo)")
    plt.plot(xs, ys_gr, marker="o", label="Greedy (aprox.)")
    plt.xlabel("n (cantidad de ítems)")
    plt.ylabel("Tiempo promedio (s)")
    plt.title("Mochila 0/1 — Tiempo vs n (W=1000)")
    if grid:
        plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=dpi)
    plt.close()

def plot_w(rows, out_path: str, dpi: int = 200, grid: bool = False):
    parent = os.path.dirname(out_path)
    if parent:
        os.path.exists(parent) or os.makedirs(parent, exist_ok=True)
    xs = [W for (W, _) in rows]
    ys = [t for (_, t) in rows]
    plt.figure()
    plt.plot(xs, ys, marker="o", label="DP (óptimo)")
    plt.xlabel("W (capacidad)")
    plt.ylabel("Tiempo (s)")
    plt.title("Mochila 0/1 — Tiempo DP vs W (n=50)")
    if grid:
        plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=dpi)
    plt.close()

def plot_q(rows, out_path: str, dpi: int = 200, grid: bool = False):
    parent = os.path.dirname(out_path)
    if parent:
        os.path.exists(parent) or os.makedirs(parent, exist_ok=True)
    xs = [n for (n, _) in rows]
    ys = [r for (_, r) in rows]
    plt.figure()
    plt.plot(xs, ys, marker="o", label="Greedy/Óptimo (promedio)")
    plt.xlabel("n (cantidad de ítems)")
    plt.ylabel("Ratio Greedy/Óptimo")
    plt.title("Mochila 0/1 — Calidad Greedy respecto del óptimo (W=800)")
    if grid:
        plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.ylim(0.9970, 1.0002)
    plt.savefig(out_path, dpi=dpi)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mochila 0/1 (DP vs Greedy) — CSV y PNG opcional, con control de semilla y rangos.")
    parser.add_argument("mode", nargs="?", default="n", choices=["n", "w", "q"], help="Modo: n (tiempo vs n), w (tiempo DP vs W), q (calidad Greedy/Óptimo)")
    parser.add_argument("--out", type=str, default="", help="Ruta del CSV de salida (opcional).")
    parser.add_argument("--png", type=str, default="", help="Ruta del PNG de salida (opcional).")
    parser.add_argument("--dpi", type=int, default=200, help="Resolución del PNG")
    parser.add_argument("--grid", action="store_true", help="Mostrar grilla en el gráfico")

    # Parámetros de distribución y semilla
    parser.add_argument("--seed", type=int, default=None, help="Semilla para aleatoriedad (reproducible)")
    parser.add_argument("--w-range", type=str, default="1:50", help="Rango de pesos w_low:w_high (ej. 1:50)")
    parser.add_argument("--v-range", type=str, default="1:100", help="Rango de valores v_low:v_high (ej. 1:100)")

    # Específicos por modo
    parser.add_argument("--W", type=int, default=1000, help="[n] Capacidad fija para tiempo vs n")
    parser.add_argument("--ns", type=int, nargs="*", default=None, help="[n,q] Lista de n a evaluar")
    parser.add_argument("--trials", type=int, default=None, help="[n,q] Repeticiones para promediar")
    parser.add_argument("--same-instance-per-n", action="store_true", help="[n,q] Reusar la MISMA instancia en todos los trials de cada n")
    parser.add_argument("--n", type=int, default=50, help="[w] Número de ítems para tiempo vs W")
    parser.add_argument("--Ws", type=int, nargs="*", default=None, help="[w] Lista de capacidades W a evaluar")
    parser.add_argument("--same-instance-across-W", action="store_true", default=True, help="[w] (por defecto True) Reusar la MISMA instancia para todos los W")

    # Específicos de q
    parser.add_argument("--Wq", type=int, default=800, help="[q] Capacidad fija para calidad Greedy/Óptimo")

    args = parser.parse_args()

    # Parsear rangos
    w_low, w_high = [int(x) for x in args.w_range.split(":")]
    v_low, v_high = [int(x) for x in args.v_range.split(":")]

    if args.mode == "n":
        trials = args.trials if args.trials is not None else 5
        ns = args.ns if args.ns is not None else [20, 30, 40, 50, 60, 70]
        rows = runtime_vs_n(W=args.W, trials=trials, ns=ns, seed=args.seed, same_instance_per_n=args.same_instance_per_n, w_low=w_low, w_high=w_high, v_low=v_low, v_high=v_high)
        for n, tdp, tgr in rows:
            print(f"{n},{tdp:.6f},{tgr:.6f}")
        if args.out:
            write_csv(args.out, "n,tdp,tgreedy", rows)
        if args.png:
            plot_n(rows, args.png, dpi=args.dpi, grid=args.grid)

    elif args.mode == "w":
        Ws = args.Ws if args.Ws is not None else [100, 200, 400, 800, 1200]
        rows = runtime_dp_vs_W(n=args.n, Ws=Ws, seed=args.seed, w_low=w_low, w_high=w_high, v_low=v_low, v_high=v_high, same_instance_across_W=args.same_instance_across_W)
        for W, t in rows:
            print(f"{W},{t:.6f}")
        if args.out:
            write_csv(args.out, "W,tdp", rows)
        if args.png:
            plot_w(rows, args.png, dpi=args.dpi, grid=args.grid)

    elif args.mode == "q":
        trials = args.trials if args.trials is not None else 20
        ns = args.ns if args.ns is not None else [20, 30, 40, 50]
        rows = quality_greedy(W=args.Wq, ns=ns, trials=trials, seed=args.seed, w_low=w_low, w_high=w_high, v_low=v_low, v_high=v_high, same_instance_per_n=args.same_instance_per_n)
        for n, r in rows:
            print(f"{n},{r:.6f}")
        if args.out:
            write_csv(args.out, "n,ratio_greedy_optimo", rows)
        if args.png:
            plot_q(rows, args.png, dpi=args.dpi, grid=args.grid)

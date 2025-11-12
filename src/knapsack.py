import random  # Módulo para generar números aleatorios (instancias de prueba)
import time    # Módulo para medir tiempos de ejecución
from typing import List, Tuple  # Anotaciones de tipos (listas y tuplas)

def dp_knapsack(values: List[int], weights: List[int], W: int) -> int:  # Función: mochila 0/1 con Programación Dinámica (óptimo)
    n = len(values)  # Cantidad de ítems
    # DP de tamaño (n+1) x (W+1)
    dp = [0] * (W + 1)  # Arreglo 1D de DP: dp[cap] = mejor valor alcanzable con capacidad 'cap'
    for i in range(n):  # Itera sobre cada ítem
        w = weights[i]  # Peso del ítem i
        v = values[i]   # Valor del ítem i
        for cap in range(W, w - 1, -1):  # Recorre capacidades de W hacia w (reversa) para no sobreescribir decisiones del mismo ítem
            cand = dp[cap - w] + v  # Candidato: tomar el ítem i si cabe → valor previo en (cap - w) + v
            if cand > dp[cap]:      # Si conviene tomar el ítem (mejor valor)
                dp[cap] = cand      # Actualiza el mejor valor para esta capacidad
    return dp[W]  # Devuelve el mejor valor con capacidad total W

def greedy_knapsack(values: List[int], weights: List[int], W: int) -> int:  # Heurística Greedy por razón valor/peso (aproximada)
    items = list(range(len(values)))  # Índices de ítems [0, 1, ..., n-1]
    # Ordenar por razón valor/peso
    items.sort(key=lambda i: values[i] / weights[i], reverse=True)  # Ordena desc. por eficiencia (valor por unidad de peso)
    total = 0  # Valor total acumulado
    cap = 0    # Peso usado (capacidad ocupada)
    for i in items:  # Recorre ítems en orden greedy
        if cap + weights[i] <= W:  # Si el ítem i cabe en la capacidad restante
            cap += weights[i]      # Suma su peso a la capacidad usada
            total += values[i]     # Suma su valor al total
    return total  # Retorna el valor total conseguido por la heurística

def random_instance(n: int, w_low=1, w_high=50, v_low=1, v_high=100):  # Genera una instancia aleatoria de n ítems
    weights = [random.randint(w_low, w_high) for _ in range(n)]  # Pesos aleatorios en [w_low, w_high]
    values = [random.randint(v_low, v_high) for _ in range(n)]   # Valores aleatorios en [v_low, v_high]
    return values, weights  # Devuelve tuplas (valores, pesos)

def runtime_vs_n():  # Mide tiempos DP vs Greedy variando n (con W fijo)
    # Comparar tiempos DP vs Greedy con W fijo
    W = 1000  # Capacidad fija para la prueba
    trials = 5  # Número de repeticiones por tamaño (promedio para reducir ruido)
    ns = [20, 30, 40, 50, 60, 70]  # DP crece ~O(n*W)  # Tamaños de problema (cantidad de ítems)
    rows = []  # Aquí se guardarán los resultados (n, tiempo_DP_prom, tiempo_Greedy_prom)
    for n in ns:  # Para cada tamaño n
        t_dp = 0.0  # Acumulador de tiempo para DP
        t_gr = 0.0  # Acumulador de tiempo para Greedy
        for _ in range(trials):  # Repetir varias veces y promediar
            v, w = random_instance(n)  # Genera instancia aleatoria de n ítems
            start = time.perf_counter()  # Marca de tiempo (alta resolución)
            _ = dp_knapsack(v, w, W)     # Ejecuta DP (resultado no se usa; medimos tiempo)
            t_dp += (time.perf_counter() - start)  # Acumula tiempo de DP
            start = time.perf_counter()  # Nueva marca para Greedy
            _ = greedy_knapsack(v, w, W)  # Ejecuta Greedy
            t_gr += (time.perf_counter() - start)  # Acumula tiempo de Greedy
        rows.append((n, t_dp / trials, t_gr / trials))  # Guarda promedios por n
    return rows  # Devuelve lista de tuplas (n, tiempo_DP_prom, tiempo_Greedy_prom)

def runtime_dp_vs_W():  # Mide el tiempo de DP variando W (n fijo) para evidenciar crecimiento pseudo-polinomial
    # Fijar n y medir DP variando W (pseudo-polinomial)
    n = 50  # Número fijo de ítems
    v, w = random_instance(n)  # Instancia aleatoria fija para todos los W (evitar variación por datos)
    Ws = [100, 200, 400, 800, 1200]  # Capacidades a evaluar (crecientes)
    rows = []  # Guardará (W, tiempo_DP)
    for W in Ws:  # Para cada capacidad W
        start = time.perf_counter()  # Marca de tiempo
        _ = dp_knapsack(v, w, W)     # Ejecuta DP con esta capacidad
        t = time.perf_counter() - start  # Tiempo transcurrido
        rows.append((W, t))  # Guarda resultado
    return rows  # Devuelve lista de tuplas (W, tiempo_DP)

def quality_greedy():  # Mide la calidad de Greedy comparada con Óptimo (DP) como promedio Greedy/Óptimo
    # Medir calidad Greedy (aprox) vs óptimo (DP)
    W = 800  # Capacidad fija para la comparación de calidad
    ns = [20, 30, 40, 50]  # Tamaños de ítems a evaluar
    trials = 20  # Número de corridas por cada n (promediar para robustez)
    rows = []  # Guardará (n, promedio_ratio)
    for n in ns:  # Para cada tamaño n
        ratios = []  # Lista de ratios Greedy/Óptimo por instancia
        for _ in range(trials):  # Repeticiones
            v, w = random_instance(n)  # Nueva instancia aleatoria
            opt = dp_knapsack(v, w, W)  # Valor óptimo con DP
            gr = greedy_knapsack(v, w, W)  # Valor obtenido por Greedy
            if opt > 0:  # Evita división por cero
                ratios.append(gr / opt)  # Ratio de calidad (≤ 1 usualmente)
        rows.append((n, sum(ratios) / len(ratios)))  # Promedio de ratios para este n
    return rows  # Devuelve lista de tuplas (n, calidad_promedio)

if __name__ == "__main__":  # Punto de entrada si se ejecuta como script
    import sys  # Para leer argumentos de línea de comandos
    mode = sys.argv[1] if len(sys.argv) > 1 else "n"  # Modo: "n", "w" o "q" (por defecto "n")
    if mode == "n":  # Modo tiempos DP vs Greedy variando n
        for n, tdp, tgr in runtime_vs_n():  # Itera resultados
            print(f"{n},{tdp:.6f},{tgr:.6f}")  # Imprime CSV: n, tiempo_DP_prom, tiempo_Greedy_prom
    elif mode == "w":  # Modo tiempo DP vs W (n fijo)
        for W, t in runtime_dp_vs_W():  # Itera resultados
            print(f"{W},{t:.6f}")  # Imprime CSV: W, tiempo_DP
    elif mode == "q":  # Modo calidad Greedy/Óptimo
        for n, r in quality_greedy():  # Itera resultados
            print(f"{n},{r:.6f}")  # Imprime CSV: n, promedio_ratio

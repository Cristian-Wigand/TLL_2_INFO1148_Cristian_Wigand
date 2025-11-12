import random  # Módulo estándar para generar números aleatorios (listas de prueba)
import time    # Módulo estándar para medir tiempos de ejecución con alta resolución
import os      # Módulo estándar para manejar rutas y creación de carpetas
import argparse  # Módulo estándar para parsear argumentos por línea de comandos
from typing import List  # Para anotar tipos de listas de enteros (sólo documentación/ayuda)

def insertion_sort(arr: List[int]) -> List[int]:  # Define la función de ordenamiento Insertion Sort, retorna una nueva lista ordenada
    a = arr[:]  # Crea una copia superficial para no modificar la lista original
    for i in range(1, len(a)):  # Recorre desde el índice 1 al final (el subarreglo a[0:i] se asume ordenado)
        key = a[i]  # Guarda el elemento actual que se insertará en la porción ordenada
        j = i - 1  # Comienza a comparar hacia la izquierda desde el elemento previo
        while j >= 0 and a[j] > key:  # Mientras no salgamos del arreglo y el elemento a la izquierda sea mayor que key
            a[j + 1] = a[j]  # Desplaza a la derecha el elemento mayor para hacer hueco
            j -= 1  # Mueve el índice hacia la izquierda
        a[j + 1] = key  # Inserta key en la posición correcta dentro de la parte ordenada
    return a  # Retorna la nueva lista ordenada

def merge_sort(arr: List[int]) -> List[int]:  # Define Merge Sort (divide y vencerás), retorna una nueva lista ordenada
    if len(arr) <= 1:  # Caso base: listas vacías o de un elemento ya están ordenadas
        return arr[:]  # Devuelve una copia para no alterar el original
    mid = len(arr) // 2  # Calcula el índice medio para dividir la lista en dos mitades
    left = merge_sort(arr[:mid])  # Ordena recursivamente la mitad izquierda
    right = merge_sort(arr[mid:])  # Ordena recursivamente la mitad derecha
    return merge(left, right)  # Mezcla (merge) las dos mitades ordenadas y devuelve el resultado

def merge(left: List[int], right: List[int]) -> List[int]:  # Función auxiliar para mezclar dos listas ya ordenadas
    i = j = 0  # Inicializa punteros para recorrer left (i) y right (j)
    result = []  # Lista donde se acumulará el resultado final ordenado
    while i < len(left) and j < len(right):  # Repite mientras haya elementos en ambas listas
        if left[i] <= right[j]:  # Si el elemento actual de left es menor o igual que el de right
            result.append(left[i]); i += 1  # Agrega left[i] al resultado y avanza el puntero i
        else:
            result.append(right[j]); j += 1  # Si no, agrega right[j] y avanza el puntero j
    result.extend(left[i:]); result.extend(right[j:])  # Agrega los elementos restantes de la lista que aún tenga elementos
    return result  # Devuelve la lista combinada y ordenada

def benchmark(sizes=None, trials: int = 5):  # Ejecuta pruebas de rendimiento para tamaños dados, promediando varias corridas
    if sizes is None:  # Si no se proporcionaron tamaños explícitos
        sizes = [200, 400, 800, 1600, 3200, 6400]  # Usa una lista por defecto de tamaños crecientes
    results = []  # Aquí se guardarán tuplas (n, tiempo_prom_insertion, tiempo_prom_merge)
    for n in sizes:  # Itera por cada tamaño n
        data = [random.randint(0, 10_000_000) for _ in range(n)]  # Genera una lista aleatoria de longitud n con enteros grandes
        t0 = 0.0  # Acumulador de tiempo para Insertion Sort
        for _ in range(trials):  # Repite varias veces para promediar y reducir ruido aleatorio
            d = data[:]  # Copia de los datos para no alterar la lista base (misma distribución)
            start = time.perf_counter()  # Toma un timestamp de alta resolución antes de ejecutar
            insertion_sort(d)  # Ejecuta Insertion Sort sobre la copia
            t0 += (time.perf_counter() - start)  # Suma el tiempo transcurrido tras la ejecución
        t0 /= trials  # Calcula el promedio de tiempos de Insertion Sort para este n
        t1 = 0.0  # Acumulador de tiempo para Merge Sort
        for _ in range(trials):  # Repite varias veces para promediar
            d = data[:]  # Copia los mismos datos base
            start = time.perf_counter()  # Toma un nuevo timestamp
            merge_sort(d)  # Ejecuta Merge Sort sobre la copia
            t1 += (time.perf_counter() - start)  # Suma el tiempo transcurrido
        t1 /= trials  # Calcula el promedio de tiempos de Merge Sort para este n
        results.append((n, t0, t1))  # Guarda los resultados promediados para este tamaño
    return results  # Devuelve la lista de resultados para todos los tamaños

def write_csv(path: str, rows):  # Escribe los resultados en un archivo CSV con encabezado
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None  # Crea la carpeta destino si existe parte de ruta
    with open(path, "w", encoding="utf-8") as f:  # Abre el archivo en modo escritura con codificación UTF-8
        f.write("n,insertion,merge\n")  # Escribe la línea de encabezado del CSV
        for n, ti, tm in rows:  # Recorre cada resultado
            f.write(f"{int(n)},{ti:.6f},{tm:.6f}\n")  # Escribe una fila con n y los tiempos promediados a 6 decimales

if __name__ == "__main__":  # Punto de entrada cuando el archivo se ejecuta como script (no cuando se importa)
    parser = argparse.ArgumentParser(description="Benchmark Insertion vs Merge y salida CSV opcional.")  # Crea un parser de argumentos
    parser.add_argument("--out", type=str, default="", help="Ruta del CSV de salida (p.ej., data/sort_benchmark.csv)")  # Argumento opcional para guardar CSV
    parser.add_argument("--trials", type=int, default=5, help="Corridas por tamaño para promediar")  # Argumento para definir cantidad de repeticiones
    parser.add_argument("--sizes", type=int, nargs="*", default=[200,400,800,1600,3200,6400], help="Tamaños n a evaluar")  # Argumento para definir los tamaños n
    args = parser.parse_args()  # Parsea los argumentos proporcionados por el usuario en la línea de comandos

    res = benchmark(sizes=args.sizes, trials=args.trials)  # Ejecuta el benchmark con los tamaños y trials deseados

    for n, ti, tm in res:  # Recorre los resultados obtenidos
        print(f"{n},{ti:.6f},{tm:.6f}")  # Imprime siempre por pantalla una línea CSV por cada tamaño

    if args.out:  # Si el usuario proporcionó una ruta de salida con --out
        write_csv(args.out, res)  # Guarda también los resultados en el archivo CSV indicado

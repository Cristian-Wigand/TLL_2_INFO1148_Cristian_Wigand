# Evidencia empírica — Ordenamiento y Mochila 0/1

Este repositorio contiene dos scripts en Python para generar **evidencia empírica**:

1) **`sorts.py`**: compara tiempos de **Insertion Sort** vs **Merge Sort**.  
2) **`knapsack.py`**: evalúa el problema de **Mochila 0/1** con:
   - **Programación Dinámica (DP)** — óptimo.  
   - **Greedy por valor/peso** — aproximado.

Las ejecuciones imprimen resultados en formato **CSV** (valores separados por comas), listos para abrir en Excel/LibreOffice o graficar con cualquier herramienta.

---

## Requisitos

- **Python 3.10+**  
- No se necesitan librerías externas.

Comprobar versión:
```bash
python --version
# o en algunos sistemas:
python3 --version
```

## 1) `sorts.py` — Insertion vs Merge

### ¿Qué hace?
- Genera listas aleatorias de distintos tamaños y mide el tiempo promedio de:
  - **Insertion Sort** (O(n²))
  - **Merge Sort** (O(n log n))
- Muestra **una línea CSV por tamaño** con: `n,insertion,merge` (tiempos en **segundos**).

### Uso básico

**Linux/macOS (bash)** o **Windows PowerShell**:

Imprimir por pantalla:
```bash
python src/sorts.py
```

Guardar también en un archivo CSV (crea carpeta si hace falta):
```bash
python src/sorts.py --out data/sort_benchmark.csv
```

Cambiar tamaños y número de repeticiones:
```bash
python src/sorts.py --sizes 100 200 400 800 --trials 7 --out data/sort_benchmark.csv
```

### Salida esperada (ejemplo)
```
n,insertion,merge
200,0.003512,0.000421
400,0.014233,0.000915
800,0.055879,0.002014
...
```

**Columnas:**
- `n`: tamaño de la lista.
- `insertion`: tiempo promedio (s) de Insertion Sort.
- `merge`: tiempo promedio (s) de Merge Sort.

---

## 2) `knapsack.py` — Mochila 0/1 (DP vs Greedy)

### ¿Qué hace?
Ejecuta tres **modos** distintos (se eligen por argumento):

1. `n` → **Tiempo vs número de ítems** (W fijo = 1000).  
   - Compara **DP (óptimo)** vs **Greedy (aprox.)**.  
   - Salida: `n,tdp,tgreedy`.

2. `w` → **Tiempo de DP vs capacidad W** (n fijo = 50).  
   - Evidencia crecimiento pseudo-polinomial de DP.  
   - Salida: `W,tdp`.

3. `q` → **Calidad Greedy/Óptimo** (promedio de razones `Greedy/DP`).  
   - Salida: `n,ratio_greedy_optimo`.

> Los tamaños, W y repeticiones están definidos **dentro del código**. Si necesitas cambiarlos, edita directamente las funciones `runtime_vs_n`, `runtime_dp_vs_W` y `quality_greedy`.

### Uso básico

**Modo `n`** — tiempos DP vs Greedy variando `n`:
```bash
python src/knapsack.py n
# Guardar a archivo:
python src/knapsack.py n > data/kn_vs_n.csv
```

**Modo `w`** — tiempo DP variando W:
```bash
python src/knapsack.py w
# Guardar a archivo:
python src/knapsack.py w > data/kn_vs_w.csv
```

**Modo `q`** — calidad Greedy/Óptimo:
```bash
python src/knapsack.py q
# Guardar a archivo:
python src/knapsack.py q > data/kn_quality.csv
```

### Salida esperada (ejemplos)

**`n` (DP vs Greedy):**
```
20,0.001234,0.000057
30,0.002901,0.000089
...
```
Columnas:  
- `n`: cantidad de ítems  
- `tdp`: tiempo promedio (s) de DP  
- `tgreedy`: tiempo promedio (s) de Greedy

**`w` (DP vs W):**
```
100,0.002331
200,0.004701
400,0.009518
...
```
Columnas:  
- `W`: capacidad  
- `tdp`: tiempo (s) de DP

**`q` (calidad Greedy):**
```
20,0.948611
30,0.962004
...
```
Columnas:  
- `n`: cantidad de ítems  
- `ratio_greedy_optimo`: promedio de `Greedy/Óptimo` (∈(0,1], más cercano a 1 es mejor).

---

## Abrir los CSV en Excel / LibreOffice

1. Abre Excel/LibreOffice Calc → **Datos → Desde texto/CSV**.  
2. Selecciona el archivo (`.csv`).  
3. **Separador**: **coma (,)**.  
4. Acepta e inserta.

> Nota regional: si tu Excel usa coma como separador decimal, te conviene importar indicando **separador = coma** y **decimal = punto** para ver bien los segundos (p. ej., `0.012345`).

---

## Reproducibilidad (opcional)

Los scripts generan **instancias aleatorias**. Para resultados **deterministas** puedes **sembrar** el generador, por ejemplo al inicio de cada función de experimento:
```python
import random
random.seed(42)  # fija la semilla
```
> Si fijas la semilla, las instancias y tiempos serán más consistentes entre corridas.

---

## Problemas comunes

- **“Se demora mucho con DP”**: recuerda que DP en Mochila 0/1 cuesta ~**O(n·W)**.  
  Soluciones:
  - Usa valores de `W` **más pequeños**.
  - Reduce los `n` de prueba.
  - Para exploración rápida, usa el modo `n` y enfócate en la curva relativa DP vs Greedy.

- **Excel no separa columnas**: importa como **CSV** con separador **coma**.

---

## Resumen rápido de comandos

```bash
# Insertion vs Merge
python src/sorts.py
python src/sorts.py --out data/sort_benchmark.csv
python src/sorts.py --sizes 100 200 400 --trials 7 --out data/sort_benchmark.csv

# Mochila 0/1
python src/knapsack.py n  > data/kn_vs_n.csv
python src/knapsack.py w  > data/kn_vs_w.csv
python src/knapsack.py q  > data/kn_quality.csv
```

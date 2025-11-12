# Manual de usuario — Evidencia empírica (INFO1148)

Este README explica **qué hace cada experimento**, **por qué lo hacemos**, y **qué deberías observar** en las figuras. Incluye comandos listos para Windows PowerShell y Linux/macOS. Todas las imágenes (PNG) se generan **con cuadricula** para facilitar la lectura.

---

## ¿Qué genera este repositorio?
1) **Ordenamiento (Insertion vs Merge)**: compara tiempos promedio y muestra por qué `O(n^2)` (inserción) escala peor que `O(n log n)` (merge).
2) **Mochila 0/1 (DP vs Greedy)**: evidencia el costo temporal de Programación Dinámica (óptimo) vs una heurística (rápida) y mide la **calidad** de la heurística respecto del óptimo.

---

## Requisitos y carpetas básicas
- Python 3.10+
- `matplotlib` (si falta: `python -m pip install matplotlib`)

Crea estas carpetas (si no existen):
```
data/   # CSV generados
figs/   # PNG para el informe
```

---

## 1) Ordenamiento — Insertion vs Merge

**¿Qué hace?**  
Genera listas aleatorias de distintos tamaños, ejecuta ambos algoritmos varias veces y promedia los tiempos. Sirve para **visualizar** que Insertion Sort crece cuadráticamente y Merge Sort crece log-linealmente.

**Ejecuta y genera CSV + PNG:**

**Windows PowerShell (una línea):**
```powershell
python src/sorts.py --seed 42 --trials 5 --sizes 200 400 800 1600 3200 6400 --out data/sort_benchmark.csv --png figs/fig_sort_tiempos.png --dpi 200 --grid
```
**Linux/macOS:**
```bash
python3 src/sorts.py --seed 42 --trials 5 --sizes 200 400 800 1600 3200 6400 --out data/sort_benchmark.csv --png figs/fig_sort_tiempos.png --dpi 200 --grid
```
**Qué sale y cómo leerlo:**
- CSV: `data/sort_benchmark.csv` con encabezado `n,insertion,merge`.
- PNG: `figs/fig_sort_tiempos.png` (con cuadricula).  
  Esperable: la curva de inserción sube mucho más rápido que la de merge al aumentar `n`.

---

## 2) Mochila 0/1 — DP vs Greedy

### 2.1) Tiempo vs n (W=1000)

**¿Qué hace?**  
Compara el **tiempo promedio** de DP (óptimo) y Greedy (aprox.) cuando crece el número de ítems `n`, manteniendo la capacidad `W=1000`. Muestra la diferencia de rendimiento entre un método óptimo y uno heurístico.

**Ejecuta y genera CSV + PNG:**

**PowerShell:**
```powershell
python src/knapsack.py n --seed 42 --W 1000 --ns 20 30 40 50 60 70 --trials 5 --out data/kn_vs_n.csv --png figs/fig_knap_tiempo_vs_n.png --dpi 200 --grid
```
**Linux/macOS:**
```bash
python3 src/knapsack.py n --seed 42 --W 1000 --ns 20 30 40 50 60 70 --trials 5 --out data/kn_vs_n.csv --png figs/fig_knap_tiempo_vs_n.png --dpi 200 --grid
```
**Qué sale y cómo leerlo:**
- CSV: `data/kn_vs_n.csv` con `n,tdp,tgreedy`.
- PNG: `figs/fig_knap_tiempo_vs_n.png`.  
  Esperable: **DP** demora más (crece con `n·W`), **Greedy** es mucho más rápido.

---

### 2.2) Tiempo DP vs W (n=50)

**¿Qué hace?**  
Mide **sólo DP** variando la capacidad `W` con `n=50`. Sirve para evidenciar el **crecimiento pseudo-polinomial** `O(n·W)` del algoritmo de DP (sube al incrementar `W`).

**Ejecuta y genera CSV + PNG:**

**PowerShell:**
```powershell
python src/knapsack.py w --seed 42 --n 50 --Ws 100 200 400 800 1200 --out data/kn_vs_w.csv --png figs/fig_knap_dp_vs_W.png --dpi 200 --grid
```
**Linux/macOS:**
```bash
python3 src/knapsack.py w --seed 42 --n 50 --Ws 100 200 400 800 1200 --out data/kn_vs_w.csv --png figs/fig_knap_dp_vs_W.png --dpi 200 --grid
```
**Qué sale y cómo leerlo:**
- CSV: `data/kn_vs_w.csv` con `W,tdp`.
- PNG: `figs/fig_knap_dp_vs_W.png`.  
  Esperable: la curva sube al aumentar `W` (más capacidad ⇒ tabla de DP más grande ⇒ más tiempo).

> Nota: por defecto se usa **la misma instancia** de ítems para todos los `W` (curva más “suave”).

---

### 2.3) Calidad Greedy vs Óptimo (W=800)

**¿Qué hace?**  
Calcula la **razón de calidad** `Greedy/Óptimo` (promedio sobre varias instancias). Un valor cercano a `1` implica que la heurística rinde muy parecido al óptimo; por debajo de `1` muestra la **pérdida** respecto del DP.

**Ejecuta y genera CSV + PNG:**

**PowerShell:**
```powershell
python src/knapsack.py q --seed 42 --Wq 800 --ns 20 30 40 50 --trials 20 --out data/kn_quality.csv --png figs/fig_knap_greedy_calidad.png --dpi 200 --grid
```
**Linux/macOS:**
```bash
python3 src/knapsack.py q --seed 42 --Wq 800 --ns 20 30 40 50 --trials 20 --out data/kn_quality.csv --png figs/fig_knap_greedy_calidad.png --dpi 200 --grid
```
**Qué sale y cómo leerlo:**
- CSV: `data/kn_quality.csv` con `n,ratio_greedy_optimo`.
- PNG: `figs/fig_knap_greedy_calidad.png`.  
  Interpretación: valores **cerca de 1** ⇒ Greedy acierta; valores **menores** ⇒ Greedy se aleja del óptimo.  
  Si las diferencias son muy pequeñas y “no se ven”, puedes **hacer zoom** en el eje Y cambiando `plt.ylim` en `plot_q`.

---

## Reproducibilidad y parámetros clave

- **`--seed`**: fija la semilla aleatoria (mismas curvas entre corridas).  
- **`--trials`**: repeticiones por punto (promedia y reduce ruido).  
- **`--ns`, `--Ws`, `--W/--Wq`**: tamaños y capacidades evaluadas.  
- **`--w-range`, `--v-range`**: rangos de pesos y valores que definen lo “difícil” de las instancias (p. ej., `--w-range 1:80 --v-range 1:60`).  
- **`--grid`, `--dpi`**: cuadricula y resolución del PNG.  
- **Multi-línea en PowerShell**: usa el **backtick** (`` ` ``) al final de la línea (sin espacios) si quieres partir comandos.

---

## CSV → Excel/LibreOffice
1) Datos → Desde texto/CSV  
2) Separador **coma (,)** y decimal **punto**  
3) Aceptar

---

## Rutas de salida esperadas
- `figs/fig_sort_tiempos.png`
- `figs/fig_knap_tiempo_vs_n.png`
- `figs/fig_knap_dp_vs_W.png`
- `figs/fig_knap_greedy_calidad.png`
- CSV correspondientes en `data/`.

---

## Resumen de comandos

### Windows PowerShell
> Crea carpetas, instala dependencias si falta `matplotlib`, y genera **todas** las figuras y CSV.
```powershell
mkdir data; mkdir figs
python -m pip install matplotlib

# 1) Sorts — Insertion vs Merge
python src/sorts.py --seed 42 --trials 5 --sizes 200 400 800 1600 3200 6400 --out data/sort_benchmark.csv --png figs/fig_sort_tiempos.png --dpi 200 --grid

# 2.1) Knapsack — tiempo vs n (W=1000)
python src/knapsack.py n --seed 42 --W 1000 --ns 20 30 40 50 60 70 --trials 5 --out data/kn_vs_n.csv --png figs/fig_knap_tiempo_vs_n.png --dpi 200 --grid

# 2.2) Knapsack — tiempo DP vs W (n=50)
python src/knapsack.py w --seed 42 --n 50 --Ws 100 200 400 800 1200 --out data/kn_vs_w.csv --png figs/fig_knap_dp_vs_W.png --dpi 200 --grid

# 2.3) Knapsack — calidad Greedy (W=800)
python src/knapsack.py q --seed 42 --Wq 800 --ns 20 30 40 50 --trials 20 --out data/kn_quality.csv --png figs/fig_knap_greedy_calidad.png --dpi 200 --grid
```

### Linux/macOS
```bash
mkdir -p data figs
python3 -m pip install matplotlib

# 1) Sorts — Insertion vs Merge
python3 src/sorts.py --seed 42 --trials 5 --sizes 200 400 800 1600 3200 6400 --out data/sort_benchmark.csv --png figs/fig_sort_tiempos.png --dpi 200 --grid

# 2.1) Knapsack — tiempo vs n (W=1000)
python3 src/knapsack.py n --seed 42 --W 1000 --ns 20 30 40 50 60 70 --trials 5 --out data/kn_vs_n.csv --png figs/fig_knap_tiempo_vs_n.png --dpi 200 --grid

# 2.2) Knapsack — tiempo DP vs W (n=50)
python3 src/knapsack.py w --seed 42 --n 50 --Ws 100 200 400 800 1200 --out data/kn_vs_w.csv --png figs/fig_knap_dp_vs_W.png --dpi 200 --grid

# 2.3) Knapsack — calidad Greedy (W=800)
python3 src/knapsack.py q --seed 42 --Wq 800 --ns 20 30 40 50 --trials 20 --out data/kn_quality.csv --png figs/fig_knap_greedy_calidad.png --dpi 200 --grid
```

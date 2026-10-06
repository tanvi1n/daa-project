# All-Pairs Shortest Path Matrix Update

**Course:** Design and Analysis of Algorithms (DAA) — Unit 3: Dynamic Programming  
**Project:** 8 — Floyd-Warshall Algorithm  

---

## Description

This project demonstrates the **Floyd-Warshall algorithm** by showing how the
distance matrix is iteratively updated as each vertex is considered as an
intermediate vertex on a potential shortest path.

The application is built using Python and Streamlit. It takes a fixed
4-vertex weighted directed graph as input and walks through all 4 iterations
of the algorithm (k = A, B, C, D) in a step-by-step, interactive visualization.
Changed cells are highlighted in yellow, making it easy to see exactly which
distances improved in each iteration.

---

## Algorithm

### Concept

Floyd-Warshall is a **dynamic programming** algorithm that solves the
**all-pairs shortest path** problem for a weighted graph. Unlike Dijkstra's
algorithm (single source), it finds shortest paths between **every pair**
of vertices simultaneously.

### Pseudocode

```
Initialize D[i][j] = weight of edge (i,j), or ∞ if no edge, or 0 if i == j

for k = 1 to n:                   // try each vertex as intermediate
    for i = 1 to n:               // source vertex
        for j = 1 to n:           // destination vertex
            if D[i][k] + D[k][j] < D[i][j]:
                D[i][j] = D[i][k] + D[k][j]   // relax the path

Return D  // D[i][j] = shortest path from i to j
```

---

## Formula

```
D[i][j] = min( D[i][j], D[i][k] + D[k][j] )
```

For every intermediate vertex `k`, and every pair `(i, j)`, the algorithm asks:
> *"Is the path from i to j via k shorter than the current best path from i to j?"*

---

## Input

The sample graph has **4 vertices: A, B, C, D** with the following edge weights:

| Edge | Weight |
|------|--------|
| A → B | 3 |
| A → D | 7 |
| B → A | 8 |
| B → C | 2 |
| C → A | 5 |
| C → D | 1 |
| D → A | 2 |

### Initial Distance Matrix

```
      A    B    C    D
 A    0    3    ∞    7
 B    8    0    2    ∞
 C    5    ∞    0    1
 D    2    ∞    ∞    0
```

---

## Iterations

| Step | k | Cells Updated |
|------|---|---------------|
| 0 | — (Initial) | — |
| 1 | A | D[B][D]: ∞→15, D[C][B]: ∞→8, D[D][B]: ∞→5 |
| 2 | B | D[A][C]: ∞→5, D[D][C]: ∞→7 |
| 3 | C | D[A][D]: 7→6, D[B][A]: 8→7, D[B][D]: 15→3 |
| 4 | D | D[B][A]: 7→5, D[C][A]: 5→3, D[C][B]: 8→6 |

### Final Shortest Path Matrix

```
      A    B    C    D
 A    0    3    5    6
 B    5    0    2    3
 C    3    6    0    1
 D    2    5    7    0
```

---

## Visualization

The Streamlit application displays:

1. **Iteration title** — shows which vertex is the current intermediate vertex.
2. **Distance matrix table** — styled HTML table with:
   - 🟡 Yellow highlight for cells that changed in this iteration.
   - 🟢 Green for diagonal cells (distance from a vertex to itself = 0).
3. **Change summary panel** — lists every cell that was updated, with the
   old value → new value and the path that caused the update.
4. **Navigation controls:**
   - ◀ Previous / Next ▶ — step through iterations manually.
   - ⏮ Reset — return to the initial matrix.
   - ⏭ Final — jump directly to the final result.
   - ▶▶ Auto Run — automatically step through all iterations.
5. **Progress bar** — shows current position (0 → 4 steps).
6. **Final matrix panel** — when the last iteration is reached, shows the
   initial and final matrices side by side for comparison.
7. **Sidebar** — contains the formula, pseudocode, complexity info, and
   the original edge list.

---

## Learning Outcome

By interacting with this visualization, students will gain an understanding of:

- The **Floyd-Warshall algorithm** and how it works
- **Dynamic programming** as a problem-solving strategy
- How **iterative distance matrix updates** converge to the optimal solution
- How algorithms can be **visualized** to make them easier to understand and teach
- The difference between **direct edge weights** and **optimal shortest paths**

---

## Project Structure

```
Unit3_DynamicProgramming/
│
├── Project8_FloydWarshall.py   # Main Streamlit application
├── Prompt.txt                  # Original faculty prompt + detailed AI prompt
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## How to Run

### 1. Install Python (if not already installed)

Download from: https://www.python.org/downloads/  
Recommended version: **Python 3.9 or higher**

### 2. Install dependencies

Open a terminal in the `Unit3_DynamicProgramming/` folder and run:

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install streamlit
```

### 3. Run the application

```bash
streamlit run Project8_FloydWarshall.py
```

The application will open automatically in your browser at:
```
http://localhost:8501
```

### 4. Interact

- Use **Next ▶** to step through iterations one at a time.
- Use **▶▶ Auto Run** to watch the algorithm play through automatically.
- Watch yellow-highlighted cells to see which distances improve at each step.
- Read the **What changed?** panel for a plain-English explanation.

---

*DAA Project 8 — Unit 3: Dynamic Programming*

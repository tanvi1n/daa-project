# Algorithm and Pseudocode
## Project 13 – 0/1 Knapsack Problem using Branch and Bound
### DAA Macro Project — Unit V: Branch and Bound

---

## A. Problem Definition

The **0/1 Knapsack Problem** asks:

Given `n` items, each with a weight `w[i]` and a profit `p[i]`, and a knapsack
of capacity `W`, select a subset of items such that:

- The **total weight** of selected items does not exceed `W`.
- The **total profit** is **maximised**.
- Each item is either taken completely (1) or not taken at all (0).
  Fractional selection is **not** allowed.

This is an **NP-Hard** combinatorial optimisation problem.

---

## B. Input

```
n         : number of items
W         : knapsack capacity
w[1..n]   : weights of each item
p[1..n]   : profits of each item
```

**Example Input (used throughout this project):**

| Item  | Weight | Profit | P/W Ratio |
|-------|--------|--------|-----------|
| Item1 |   2    |   40   |  20.00    |
| Item2 |   3    |   50   |  16.67    |
| Item3 |   4    |   65   |  16.25    |
| Item4 |   5    |   70   |  14.00    |

Capacity W = 8

---

## C. Output

```
best_profit  : maximum achievable profit
best_items   : set of items that achieves the maximum profit
total_weight : combined weight of selected items
```

**Example Output:**
```
Optimal Profit  = 120
Selected Items  = {Item2, Item4}
Total Weight    = 8
```

---

## D. Initialization

Before the main algorithm begins:

1. **Sort items** in descending order of profit/weight ratio.
   Reason: makes the greedy bound as tight (small) as possible → more pruning.
2. **Create the root node** with level = -1, profit = 0, weight = 0.
3. **Calculate the bound** for the root node using fractional knapsack.
4. **Initialise best_profit** = 0 (no item selected yet).
5. **Enqueue** the root node into the BFS queue.

---

## E. Node Structure

Each node in the Branch-and-Bound tree represents a **partial decision state**:

```
Node {
    level         : integer   // index of the last item decided (-1 = root)
    profit        : integer   // total profit accumulated so far
    weight        : integer   // total weight accumulated so far
    bound         : float     // optimistic upper bound on achievable profit
    include_flags : list      // binary decisions made so far [1=include, 0=exclude]
}
```

A node at `level = k` means items 0 through k have been decided.
Its two children represent the choices for item `k+1`:
- **Left child**  : include item `k+1`
- **Right child** : exclude item `k+1`

---

## F. Bound Calculation (Upper Bound Function)

The **bound function** computes an optimistic upper limit on the best profit
achievable from a given node using the **Fractional Knapsack Relaxation**.

Starting from the node's current profit and weight, greedily fill the
remaining capacity:
- Take whole items (in decreasing P/W ratio order) as long as they fit.
- Take a **fraction** of the next item if it doesn't fit completely.

This bound is always ≥ true 0/1 optimal from that node → **admissible / optimistic**.

### Pseudocode for Bound Calculation

```
FUNCTION CalculateBound(node, items[], W, n):
    IF node.weight >= W:
        RETURN 0                           // infeasible — no valid bound

    profit_bound ← node.profit
    j            ← node.level + 1         // start from next undecided item
    total_weight ← node.weight

    // Greedily take whole items
    WHILE j < n AND total_weight + items[j].weight <= W:
        total_weight  ← total_weight + items[j].weight
        profit_bound  ← profit_bound + items[j].profit
        j             ← j + 1

    // Take fractional part of next item if available
    IF j < n:
        remaining    ← W - total_weight
        profit_bound ← profit_bound + (remaining / items[j].weight) × items[j].profit

    RETURN profit_bound
END FUNCTION
```

### Manual Example: Root Node (level=-1, W=0, P=0, capacity=8)

```
Remaining capacity = 8
Take Item1 (w=2, p=40) fully  → weight=2,  profit=40,  rem=6
Take Item2 (w=3, p=50) fully  → weight=5,  profit=90,  rem=3
Item3 (w=4) does not fit fully → take 3/4 fraction
    profit += (3/4) × 65 = 48.75
Bound = 0 + 40 + 50 + 48.75 = 138.75
```

### Why is the Bound "Optimistic"?

The bound relaxes the 0/1 constraint by allowing fractional items.
Fractional knapsack ≥ 0/1 knapsack always.
Therefore: `Bound(node) ≥ True 0/1 Optimal(node)` — always.

---

## G. Branching

At each non-leaf node, two children are generated for the **next undecided item**:

```
Given current node at level k:

LEFT CHILD (Include item k+1):
    child.level   ← k + 1
    child.profit  ← current.profit + p[k+1]
    child.weight  ← current.weight + w[k+1]
    child.bound   ← CalculateBound(child)

RIGHT CHILD (Exclude item k+1):
    child.level   ← k + 1
    child.profit  ← current.profit          // unchanged
    child.weight  ← current.weight          // unchanged
    child.bound   ← CalculateBound(child)
```

If `k+1 == n`, the node is a **leaf** — a complete assignment of all items.

---

## H. Feasibility Check

A node's include-child is feasible only when:
```
child.weight <= W
```

If `child.weight > W`:
- Node is **infeasible** → immediately pruned, not enqueued.

---

## I. Pruning Condition

A node is pruned (not explored) under two conditions:

**Condition 1 — Infeasibility (weight-based):**
```
IF child.weight > W → PRUNE
```

**Condition 2 — Non-promising (bound-based):**
```
IF node.bound <= best_profit → PRUNE
```

**Why bound-based pruning is safe:**
`bound` is an optimistic upper limit. If the best possible outcome from
this node is ≤ what we already have, no solution in this subtree can
improve things. We can discard it entirely without missing the optimum.

---

## J. Best Solution Update

When an include-child is feasible AND better than the current best:
```
IF child.weight <= W AND child.profit > best_profit:
    best_profit ← child.profit
    best_items  ← child.include_flags
```

---

## K. Complete Pseudocode

```
ALGORITHM KnapsackBranchAndBound(n, W, weights[], profits[], names[])

─── PREPROCESSING ────────────────────────────────────────────────────
  Sort items by (profits[i] / weights[i]) DESCENDING

─── INITIALIZATION ───────────────────────────────────────────────────
  best_profit ← 0
  best_flags  ← [0, 0, ..., 0]          // n zeros

  root.level   ← -1
  root.profit  ← 0
  root.weight  ← 0
  root.flags   ← []
  root.bound   ← CalculateBound(root, items, W, n)

  Enqueue(Q, root)

─── MAIN LOOP ────────────────────────────────────────────────────────
  WHILE Q is not empty DO:

    current ← Dequeue(Q)

    IF current.bound <= best_profit THEN
        CONTINUE                          // PRUNE: non-promising

    next_level ← current.level + 1

    IF next_level < n THEN

        ─── LEFT CHILD: Include item[next_level] ─────────────────────
        lc.level   ← next_level
        lc.profit  ← current.profit + profits[next_level]
        lc.weight  ← current.weight + weights[next_level]
        lc.flags   ← current.flags + [1]
        lc.bound   ← CalculateBound(lc, items, W, n)

        IF lc.weight <= W AND lc.profit > best_profit THEN
            best_profit ← lc.profit
            best_flags  ← lc.flags

        IF lc.weight <= W AND lc.bound > best_profit THEN
            Enqueue(Q, lc)
        // ELSE: PRUNE (infeasible OR non-promising)

        ─── RIGHT CHILD: Exclude item[next_level] ────────────────────
        rc.level   ← next_level
        rc.profit  ← current.profit
        rc.weight  ← current.weight
        rc.flags   ← current.flags + [0]
        rc.bound   ← CalculateBound(rc, items, W, n)

        IF rc.bound > best_profit THEN
            Enqueue(Q, rc)
        // ELSE: PRUNE (non-promising)

  END WHILE

─── RESULT ───────────────────────────────────────────────────────────
  selected_items ← { names[i] : best_flags[i] == 1 }
  RETURN best_profit, selected_items

END ALGORITHM
```

---

## L. Step-by-Step Explanation of the Pseudocode

**Step 1 — Sort:**
Sorting by P/W ratio ensures the greedy bound picks the most profitable
items first, making the bound as tight as possible → more pruning.

**Step 2 — Root Node:**
The root represents the state before any decision. Profit=0, Weight=0.
Its bound = 138.75 (the fractional knapsack answer for all items).

**Step 3 — BFS Queue:**
FIFO queue gives level-order exploration. All level-k nodes are explored
before level k+1 nodes.

**Step 4 — Bound check before expanding:**
If `bound ≤ best_profit`, skip. This is the key pruning step.

**Step 5 — Two children per node:**
Include-child: profit and weight increase.
Exclude-child: profit and weight stay the same, but future items change.

**Step 6 — Best solution tracking:**
Updated every time a feasible include-child beats the current best.

**Step 7 — Enqueue only promising nodes:**
Only nodes with `bound > best_profit` AND `weight ≤ W` are enqueued.

**Step 8 — Termination:**
Queue empty = all promising nodes exhausted. Current `best_profit` is optimal.

---

## Why Branch and Bound is Better Than Brute Force

| Aspect                  | Brute Force              | Branch and Bound                     |
|-------------------------|--------------------------|--------------------------------------|
| Nodes explored          | All 2ⁿ subsets           | Only promising subtrees              |
| Uses bound function     | No                       | Yes — fractional knapsack relaxation |
| Pruning                 | None                     | Weight-based + bound-based           |
| Worst-case complexity   | O(2ⁿ)                    | O(2ⁿ) worst case                     |
| Practical performance   | Always 2ⁿ               | Far fewer nodes with good bounds     |
| Optimal solution        | Guaranteed               | Guaranteed                           |

Branch and Bound does **not** reduce worst-case complexity, but it
dramatically cuts the number of nodes explored in practice.

---

## Complexity Summary

| Measure          | Value                                                     |
|------------------|-----------------------------------------------------------|
| Worst-case time  | O(2ⁿ) — all nodes explored, no pruning possible           |
| Average-case     | Much better than O(2ⁿ) due to pruning                    |
| Space (queue)    | O(2ⁿ) worst case; O(n) per node stored                    |
| Bound function   | O(n) per node (linear scan of remaining items)            |
| Sorting          | O(n log n) once at startup                                |

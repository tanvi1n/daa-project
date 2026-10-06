# Explanation
## Project 13 – 0/1 Knapsack using Branch and Bound
### DAA Macro Project — Unit V: Branch and Bound

---

## Part 1: Algorithm Explanation

### 1.1 What is Branch and Bound?

Branch and Bound is a systematic method for solving combinatorial
optimisation problems. It explores the solution space as a tree
(the **state-space tree**), but avoids exploring the entire tree by:

1. **Branching** — splitting each node into sub-problems (children),
   each representing one possible decision (include or exclude an item).

2. **Bounding** — computing an optimistic estimate (upper bound) of the
   best solution reachable from a node.

3. **Pruning** — eliminating nodes whose bound cannot improve upon the
   current best solution, cutting off entire subtrees.

The algorithm always finds the **optimal solution** without necessarily
examining every possible subset.

---

### 1.2 Why Branch and Bound for 0/1 Knapsack?

The 0/1 Knapsack problem has 2ⁿ possible subsets. For n=4 that's 16,
but for n=40 that's over a trillion. Brute force is infeasible.

Branch and Bound makes it tractable by:
- Using the **fractional knapsack solution** as an optimistic upper bound.
  (Fractional knapsack is always ≥ 0/1 knapsack.)
- Pruning any subtree whose bound cannot beat the best known solution.

---

### 1.3 The Bounding Function — Heart of Branch and Bound

For the 0/1 Knapsack, the bound at any node is computed by:

1. Starting with the node's current profit and weight.
2. Greedily filling remaining capacity with items sorted by P/W ratio.
3. If an item doesn't fit entirely, take a **fraction** of it.

This is the **fractional knapsack relaxation**.

```
Key property:
    Bound(node)  ≥  True 0/1 Optimal from that node    (always)
```

Because of this, if `Bound(node) ≤ current_best`, we can safely prune
the entire subtree — the optimum cannot possibly lie there.

---

### 1.4 Worked Example — Step by Step

**Dataset (sorted by P/W ratio, descending):**

| Item  | w | p  | P/W Ratio |
|-------|---|----|-----------|
| Item1 | 2 | 40 | 20.00     |
| Item2 | 3 | 50 | 16.67     |
| Item3 | 4 | 65 | 16.25     |
| Item4 | 5 | 70 | 14.00     |

**Capacity = 8**

---

#### ROOT NODE  (level=-1, W=0, P=0)
```
Bound = 0 + 40 + 50 + (3/4)×65 = 138.75
Action: Expand
```

---

#### LEVEL 0 — Deciding Item1

**Node 1 — Include Item1:** W=2, P=40, Bound=138.75 → EXPAND, best=40
**Node 2 — Exclude Item1:** W=0, P=0,  Bound=129.00 → EXPAND

---

#### LEVEL 1 — Deciding Item2

**Node 3 — Incl Item1, Incl Item2:** W=5, P=90,  Bound=138.75 → EXPAND, best=90
**Node 4 — Incl Item1, Excl Item2:** W=2, P=40,  Bound=133.00 → EXPAND
**Node 5 — Excl Item1, Incl Item2:** W=3, P=50,  Bound=129.00 → EXPAND
**Node 6 — Excl Item1, Excl Item2:** W=0, P=0,   Bound=121.00 → EXPAND

---

#### LEVEL 2 — Deciding Item3

**Node 7  — Incl I1+I2+I3:** W=9 > 8 → PRUNED (weight exceeded)
**Node 8  — Incl I1+I2, Excl I3:** W=5, P=90,  Bound=132.00 → EXPAND
**Node 9  — Incl I1, Excl I2, Incl I3:** W=6, P=105, Bound=133.00 → EXPAND, best=105
**Node 10 — Incl I1, Excl I2+I3:** W=2, P=40,  Bound=110.00 → EXPAND
**Node 11 — Excl I1, Incl I2+I3:** W=7, P=115, Bound=129.00 → EXPAND, best=115
**Node 12 — Excl I1, Incl I2, Excl I3:** W=3, P=50, Bound=120.00 → EXPAND
**Node 13 — Excl I1+I2, Incl I3:** W=4, P=65,  Bound=121.00 → EXPAND
**Node 14 — Excl I1+I2+I3:** W=0, P=0, Bound=70.00 ≤ 115 → PRUNED (bound ≤ best)

---

#### LEVEL 3 — Deciding Item4

**Node 15 — Incl I1+I2+I4:** W=10 > 8 → PRUNED (weight)
**Node 16 — Incl I1+I2, leaf P=90:** 90 ≤ 115 → PRUNED
**Node 17 — Incl I1+I3+I4:** W=11 > 8 → PRUNED (weight)
**Node 18 — Incl I1+I3, leaf P=105:** 105 ≤ 115 → PRUNED
  (Node 10 children: bound=110 ≤ 115 → PRUNED before expanding)
**Node 19 — Excl I1, Incl I2+I3+I4:** W=12 > 8 → PRUNED (weight)
**Node 20 — Excl I1, Incl I2+I3, leaf P=115:** 115 ≤ 120 → PRUNED

**Node 21 — Excl I1, Incl I2, Excl I3, Incl I4:**
```
W = 3+5 = 8, P = 50+70 = 120
120 > 115 → UPDATE BEST = 120, Items = {Item2, Item4}
Bound = 0 (leaf, no more items) → PRUNED at next dequeue
```

**Node 22 — Excl I1, Incl I2, Excl I3+I4:** P=50 < 120 → leaf, no update
**Node 23 — Excl I1+I2, Incl I3+I4:** W=9 > 8 → PRUNED (weight)
**Node 24 — Excl I1+I2, Incl I3, Excl I4:** P=65 < 120 → leaf, no update

---

#### Final Answer
```
Optimal Profit = 120
Selected Items = { Item2 (w=3, p=50), Item4 (w=5, p=70) }
Total Weight   = 3 + 5 = 8  (exactly fills capacity)
```

---

## Part 2: Visualization Explanation

### 2.1 What the Visualization Shows

The search tree visualization represents the **complete state-space
exploration** of the Branch-and-Bound algorithm for this knapsack instance.

Each box (node) in the tree contains:
```
┌──────────────────────────┐
│  Decision: Incl/Excl ItemX│
│  P = <profit>             │
│  W = <weight>             │
│  Bound = <upper bound>    │
│  Status: EXPAND / PRUNED  │
└──────────────────────────┘
```

### 2.2 Tree Layout

- **Root node** sits at the top centre.
- Each **level** of the tree = a decision about one item (L0=Item1, L1=Item2, ...).
- **Left branch** = Include the item.
- **Right branch** = Exclude the item.
- The tree grows downward, left=include, right=exclude.

### 2.3 Colour / Style Coding in the Visualization

| Style            | Meaning                                           |
|------------------|---------------------------------------------------|
| Blue / Green     | Node was expanded (promising, feasible)           |
| Red / Crossed    | Pruned — weight exceeded capacity (W > 8)         |
| Orange / Dashed  | Pruned — bound ≤ current best profit              |
| Gold / Bold      | Path to optimal solution (Item2 → Item4)          |
| Star node        | Optimal solution node (P=120, W=8)                |

### 2.4 Key Observations from the Visualization

1. **Multiple prunings by infeasibility** — left-heavy paths (include multiple
   large items) quickly exceed W=8 and are cut off.

2. **Bound-based pruning increases as best profit grows** — once best=115
   and then best=120, many previously-promising nodes become non-promising.

3. **The optimal path is non-obvious** — it skips Item1 (highest ratio),
   skips Item3, and combines Item2 + Item4 to perfectly fill capacity.

4. **24 nodes explored vs 16 brute-force subsets** — for this small example
   B&B explores a comparable number of nodes, but the real saving emerges
   at larger n values.

### 2.5 What Brute Force Would Have Done

Brute force evaluates all 2⁴ = 16 subsets without any pruning:
```
{}, {I1}, {I2}, {I3}, {I4},
{I1,I2}, {I1,I3}, {I1,I4}, {I2,I3}, {I2,I4}, {I3,I4},
{I1,I2,I3}, {I1,I2,I4}, {I1,I3,I4}, {I2,I3,I4}, {I1,I2,I3,I4}
```
Branch and Bound cuts off entire subtrees using the bound function,
avoiding many of these. This saving scales exponentially as n grows.

---

## Part 3: Connecting Algorithm to Visualization

| Algorithm Step                  | Visualization Element                    |
|---------------------------------|------------------------------------------|
| Root creation (P=0, W=0)        | Top node, Bound=138.75                   |
| Items sorted by P/W ratio       | Left-to-right order of levels            |
| Include branch (left child)     | Left arrow from each node                |
| Exclude branch (right child)    | Right arrow from each node               |
| Weight > W → prune              | Red node with "PRUNED (W>cap)"           |
| Bound ≤ best → prune            | Orange node with "PRUNED (B≤best)"       |
| Update best profit              | Highlighted node when new best is found  |
| Optimal solution                | Gold star node at Level 3 (P=120, W=8)  |
| BFS traversal                   | Level-by-level left-to-right exploration |

The visualization is the algorithm made visible. Every arrow is a
decision, every box is a partial state, and every pruned branch is
the algorithm proving: *"No better solution lies in this subtree."*

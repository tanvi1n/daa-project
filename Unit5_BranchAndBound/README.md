# Project 13 – 0/1 Knapsack using Branch and Bound

> **DAA Macro Project | Unit V: Branch and Bound**
> Course: Design and Analysis of Algorithms

---

## 1. Project Overview

This project implements the **0/1 Knapsack Problem** using the **Branch
and Bound** algorithm — one of the most important exact optimisation
techniques in computer science.

The implementation explores a state-space tree of include/exclude decisions,
uses the fractional knapsack relaxation as an optimistic upper bound, and
prunes subtrees that cannot possibly improve upon the best solution found
so far. The result is an algorithm that is guaranteed to find the optimal
solution while examining far fewer nodes than brute-force enumeration.

---

## 2. Problem Statement

Given **n items**, each with a weight `w[i]` and a profit `p[i]`, and a
knapsack with capacity `W`:

- Select a **subset** of items to maximise the total profit.
- The total weight of selected items must not exceed `W`.
- Each item is either taken **completely (1)** or **not at all (0)**.
  Fractional selection is not allowed.

**Formally:**
```
Maximise:   Σ p[i] × x[i]         (for i = 1 to n)
Subject to: Σ w[i] × x[i] ≤ W
            x[i] ∈ {0, 1}
```

This is an **NP-Hard** problem. No polynomial-time algorithm is known.

---

## 3. Objective

- Implement the Branch and Bound approach for the 0/1 Knapsack problem.
- Demonstrate the concept of bounding and pruning through a visual search tree.
- Show how Branch and Bound improves upon brute-force enumeration.
- Verify the algorithm finds the provably optimal solution.

---

## 4. Why Branch and Bound?

| Approach        | Complexity   | Optimal? | Pruning? |
|-----------------|-------------|----------|----------|
| Brute Force     | O(2ⁿ)        | Yes      | No       |
| Greedy          | O(n log n)   | No       | N/A      |
| Dynamic Prog.   | O(nW)        | Yes      | No       |
| Backtracking    | O(2ⁿ) worst  | Yes      | Partial  |
| Branch & Bound  | O(2ⁿ) worst  | Yes      | Aggressive |

Branch and Bound is preferred when:
- An exact optimal solution is required.
- The problem structure allows good bounds to be computed cheaply.
- In practice, large portions of the search space can be eliminated.

For 0/1 Knapsack, the fractional knapsack solution provides an excellent
tight bound (solvable in O(n log n)), making B&B highly effective.

---

## 5. Algorithm

The Branch and Bound algorithm for 0/1 Knapsack works as follows:

1. **Pre-process**: Sort items by profit/weight ratio (descending).
2. **Initialise**: Create root node (profit=0, weight=0). Compute its bound.
3. **BFS loop**: Dequeue a node. If its bound ≤ best_profit, prune it.
4. **Branch**: Generate two children:
   - **Include** the next item (profit and weight increase).
   - **Exclude** the next item (profit and weight unchanged).
5. **Feasibility**: If include-child weight > capacity, prune it.
6. **Update best**: If include-child is feasible and better, update best.
7. **Enqueue**: Only add children with bound > best_profit to queue.
8. **Terminate**: When queue is empty, best_profit is the optimal answer.

---

## 6. Pseudocode

```
ALGORITHM KnapsackBranchAndBound(n, W, weights[], profits[])

  Sort items by (profit[i] / weight[i]) DESCENDING

  best_profit ← 0
  root ← Node(level=-1, profit=0, weight=0)
  root.bound ← CalculateBound(root)
  Enqueue(Q, root)

  WHILE Q not empty DO:
    current ← Dequeue(Q)
    IF current.bound ≤ best_profit: CONTINUE   // PRUNE

    next ← current.level + 1
    IF next < n:
      // Left child: Include item[next]
      lc.profit ← current.profit + profits[next]
      lc.weight ← current.weight + weights[next]
      lc.bound  ← CalculateBound(lc)
      IF lc.weight ≤ W AND lc.profit > best_profit:
        best_profit ← lc.profit
      IF lc.weight ≤ W AND lc.bound > best_profit:
        Enqueue(Q, lc)

      // Right child: Exclude item[next]
      rc.profit ← current.profit
      rc.weight ← current.weight
      rc.bound  ← CalculateBound(rc)
      IF rc.bound > best_profit:
        Enqueue(Q, rc)

  RETURN best_profit

FUNCTION CalculateBound(node):
  IF node.weight ≥ W: RETURN 0
  bound ← node.profit
  j     ← node.level + 1
  w     ← node.weight
  WHILE j < n AND w + weights[j] ≤ W:
    w     ← w + weights[j]
    bound ← bound + profits[j]
    j     ← j + 1
  IF j < n:
    bound ← bound + ((W - w) / weights[j]) × profits[j]
  RETURN bound
```

---

## 7. Branch-and-Bound Concept

**Branching** divides the search space. At each node, we branch on
whether the next item is included or excluded, producing a binary tree.

**Bounding** computes an optimistic upper limit on the best solution
reachable from a node. This bound is computed by solving the **relaxed**
problem (fractional knapsack) from that node's state forward.

**Pruning** eliminates nodes that cannot yield a better solution than
the current best. This is safe because the bound is **admissible** —
it never underestimates the true optimal from a node.

---

## 8. Upper Bound Calculation

The bound at a node uses the **fractional knapsack relaxation**:

Starting from the node's current (profit, weight), greedily fill
remaining capacity by taking items in order of decreasing P/W ratio.
If the last item doesn't fully fit, take a fraction of it.

### Example: Root Node

```
Current state: P=0, W=0, Remaining capacity=8

Step 1: Take Item1 (w=2, p=40) fully  → W=2,  P=40,  rem=6
Step 2: Take Item2 (w=3, p=50) fully  → W=5,  P=90,  rem=3
Step 3: Item3 (w=4) doesn't fit fully
        Take fraction: (3/4) × 65 = 48.75
        P = 90 + 48.75 = 138.75

Bound = 138.75
```

**Why it's optimistic:** Fractional knapsack ≥ 0/1 knapsack always.
Since no 0/1 solution from this node can exceed 138.75, and we use
this as the upper limit for pruning, we never incorrectly prune
a subtree containing the optimal solution.

**Pruning rule:**
```
If Bound ≤ best_profit  →  PRUNE (cannot improve)
If Bound > best_profit  →  EXPLORE (may contain better solution)
```

---

## 9. Branching Strategy

At each node at level `k`, two children are generated for item `k+1`:

```
                     [ Node at level k ]
                           |
              ┌────────────┴────────────┐
              ↓                         ↓
     Include item k+1           Exclude item k+1
     P += p[k+1]                P unchanged
     W += w[k+1]                W unchanged
     Bound = new bound          Bound = new bound
```

Children are explored in this order: include first (left), then exclude.
The BFS queue explores all nodes at one level before moving to the next.

---

## 10. Pruning Strategy

Two types of pruning are used:

**1. Infeasibility Pruning (weight-based):**
```
If include-child.weight > W  →  PRUNE immediately
```
The knapsack is overloaded. This subtree contains no feasible solutions.

**2. Bound-based Pruning (optimality-based):**
```
If node.bound ≤ best_profit  →  PRUNE
```
Even the most optimistic outcome from this node cannot beat what we
already have. Pruning is safe because the bound is admissible.

---

## 11. Example Input

```
n        = 4 items
Capacity = 8

Item   Weight  Profit  P/W Ratio
Item1    2       40      20.00
Item2    3       50      16.67
Item3    4       65      16.25
Item4    5       70      14.00
```

Items are already sorted by P/W ratio (descending). This is the order
in which the algorithm processes them at each level of the tree.

---

## 12. Step-by-Step Execution

### Node Trace

| Node | Lvl | Decision        | W  | P   | Bound  | Action                    |
|------|-----|-----------------|----|-----|--------|---------------------------|
| Root | -1  | Root            | 0  | 0   | 138.75 | Expand                    |
| 1    | 0   | Include Item1   | 2  | 40  | 138.75 | Expand, best=40           |
| 2    | 0   | Exclude Item1   | 0  | 0   | 129.00 | Expand                    |
| 3    | 1   | Include Item2   | 5  | 90  | 138.75 | Expand, best=90           |
| 4    | 1   | Exclude Item2   | 2  | 40  | 133.00 | Expand                    |
| 5    | 1   | Include Item2   | 3  | 50  | 129.00 | Expand                    |
| 6    | 1   | Exclude Item2   | 0  | 0   | 121.00 | Expand                    |
| 7    | 2   | Include Item3   | 9  | 155 | 0.00   | **PRUNED** (W>8)          |
| 8    | 2   | Exclude Item3   | 5  | 90  | 132.00 | Expand                    |
| 9    | 2   | Include Item3   | 6  | 105 | 133.00 | Expand, best=105          |
| 10   | 2   | Exclude Item3   | 2  | 40  | 110.00 | Expand                    |
| 11   | 2   | Include Item3   | 7  | 115 | 129.00 | Expand, best=115          |
| 12   | 2   | Exclude Item3   | 3  | 50  | 120.00 | Expand                    |
| 13   | 2   | Include Item3   | 4  | 65  | 121.00 | Expand                    |
| 14   | 2   | Exclude Item3   | 0  | 0   | 70.00  | **PRUNED** (bound≤best)   |
| 15   | 3   | Include Item4   | 10 | 160 | 0.00   | **PRUNED** (W>8)          |
| 16   | 3   | Exclude Item4   | 5  | 90  | 90.00  | **PRUNED** (bound≤best)   |
| 17   | 3   | Include Item4   | 11 | 175 | 0.00   | **PRUNED** (W>8)          |
| 18   | 3   | Exclude Item4   | 6  | 105 | 105.00 | **PRUNED** (bound≤best)   |
| —    | 2   | (Node 10)       | 2  | 40  | 110.00 | **PRUNED** (bound≤best)   |
| 19   | 3   | Include Item4   | 12 | 185 | 0.00   | **PRUNED** (W>8)          |
| 20   | 3   | Exclude Item4   | 7  | 115 | 115.00 | **PRUNED** (bound≤best)   |
| 21   | 3   | Include Item4   | 8  | 120 | 0.00   | **best=120** ← OPTIMAL    |
| 22   | 3   | Exclude Item4   | 3  | 50  | 50.00  | **PRUNED** (bound≤best)   |
| 23   | 3   | Include Item4   | 9  | 135 | 0.00   | **PRUNED** (W>8)          |
| 24   | 3   | Exclude Item4   | 4  | 65  | 65.00  | **PRUNED** (bound≤best)   |

### Best Profit Updates

```
After Node 1  (Include Item1)         : best = 40
After Node 3  (Include Item1, Item2)  : best = 90
After Node 9  (Include Item1, Item3)  : best = 105
After Node 11 (Include Item2, Item3)  : best = 115
After Node 21 (Include Item2, Item4)  : best = 120  ← FINAL OPTIMAL
```

---

## 13. Search Tree Explanation

The search tree has 4 levels (one per item), branching into
include (left) and exclude (right) at each level.

```
                              ROOT
                           P=0, W=0
                         Bound=138.75
                        /              \
              Include I1               Exclude I1
           P=40,W=2,B=138.75        P=0,W=0,B=129.00
               /       \               /         \
         Incl I2      Excl I2     Incl I2       Excl I2
       P=90,W=5     P=40,W=2    P=50,W=3      P=0,W=0
       B=138.75     B=133.00    B=129.00      B=121.00
        /    \       /    \       /    \        /    \
    I3✗   NoI3   I3     NoI3  I3     NoI3   I3      NoI3
    W=9  B=132  W=6   B=110  W=7   B=120   W=4    B=70✗
   PRUNED      B=133  PRUNED B=129 B=120   B=121   PRUNED
                                           ...
```

At level 4 (deciding Item4):
- All "include Item4" branches from heavy paths are pruned (W>8).
- Include Item2 + Item4 path: W=8, P=120 → OPTIMAL ★

---

## 14. AI Visualization

The visualization of the Branch-and-Bound search tree was generated
using an AI image tool with the exact prompt provided in `Prompt.txt`.

The visualization file is: **Visualization.png**

It shows the complete search tree with:
- All node labels (P, W, Bound)
- Colour-coded nodes (green=explored, red=weight-pruned, orange=bound-pruned)
- Bold gold path to the optimal solution
- Legend for node types

---

## 15. AI Prompt Used

See **Prompt.txt** for the complete, detailed prompt used to generate
the visualization. Key elements of the prompt:

- Exact item data (weights, profits, P/W ratios)
- Complete tree structure with all node values
- Colour coding requirements (green, red, orange, gold)
- Pruning reason labels
- Legend requirements
- Academic/professional style (white background, no decoration)
- Title and subtitle

---

## 16. Visualization Explanation

The visualization shows the **state-space tree** explored by Branch and
Bound. Reading it:

- **Top node** = Root (P=0, W=0, Bound=138.75) — no item decided yet.
- **Downward left arrow** = Item included.
- **Downward right arrow** = Item excluded.
- **Green nodes** = Explored (promising, feasible).
- **Red ✗ nodes** = Pruned because weight exceeded capacity 8.
- **Orange ✗ nodes** = Pruned because bound fell below best profit.
- **Gold ★ node** = Optimal solution (P=120, W=8, Items=Item2+Item4).

The visualization makes it visually clear that:
1. Not all 2⁴=16 subsets are evaluated.
2. Pruning eliminates large portions of the tree.
3. The algorithm converges to the correct optimal solution.

---

## 17. Python Implementation

**File:** `Project13_Knapsack_BnB.py`

**Key components:**
- `Node` class — stores level, profit, weight, bound, decisions
- `calculate_bound()` — fractional knapsack upper bound
- `knapsack_branch_and_bound()` — main BFS-based B&B solver
- Auto-sorts items by P/W ratio before processing
- Prints full node trace showing all expansions and prunings
- Returns optimal profit and selected item names

**Language:** Python 3  
**Dependencies:** Standard library only (`queue.Queue`)

---

## 18. Sample Output

```
==============================================================
   0/1 KNAPSACK — BRANCH AND BOUND
==============================================================

  Knapsack Capacity : 8

  Item         Weight   Profit    P/W Ratio
  ------------------------------------------
  Item1             2       40        20.00
  Item2             3       50        16.67
  Item3             4       65        16.25
  Item4             5       70        14.00

--------------------------------------------------------------
   Node   Lvl      W       P     Bound  Action
--------------------------------------------------------------
      1     0      2      40    138.75  Incl Item1      → EXPAND
      2     0      0       0    129.00  Excl Item1      → EXPAND
      ...
     21     3      8     120      0.00  Incl Item4      → PRUNED (bound ≤ best)
--------------------------------------------------------------

  ╔══════════════════════════════════════╗
  ║  Optimal Profit  : 120               ║
  ║  Selected Items  : Item2, Item4      ║
  ║  Total Weight    : 8                 ║
  ║  Capacity Used   : 8/8               ║
  ╚══════════════════════════════════════╝
```

See `sample_output.txt` for the full unabbreviated output.

---

## 19. Time Complexity

| Case        | Complexity | Reason                                        |
|-------------|------------|-----------------------------------------------|
| Worst case  | O(2ⁿ)      | All nodes explored; bound never prunes        |
| Average     | << O(2ⁿ)   | Tight bounds eliminate large subtrees         |
| Bound calc  | O(n)       | Linear scan of remaining items per node       |
| Sorting     | O(n log n) | One-time preprocessing step                   |

**Important:** Branch and Bound does **not** have polynomial worst-case
complexity for 0/1 Knapsack — it is still exponential in the worst case.
The benefit comes from practical performance: with a good bound function,
most subtrees are pruned early, and the algorithm terminates much faster
than examining all 2ⁿ subsets.

The Dynamic Programming approach runs in O(nW) pseudo-polynomial time.
Branch and Bound is preferred when W is very large (making DP impractical)
or when the problem has additional constraints.

---

## 20. Space Complexity

| Structure         | Space       |
|-------------------|-------------|
| BFS Queue         | O(2ⁿ) worst |
| Per-node storage  | O(n)        |
| Recursion stack   | O(n) if DFS |
| Total             | O(n × 2ⁿ) worst case |

In practice, the queue stays small because pruned nodes are never added.

---

## 21. Advantages

- **Guaranteed optimal** — never misses the best solution.
- **Efficient in practice** — good bounds prune most of the search space.
- **General technique** — applies to many NP-Hard problems beyond knapsack.
- **Interpretable** — the search tree makes the algorithm transparent.
- **No pseudo-polynomial dependency** — unlike DP, doesn't depend on W.

---

## 22. Limitations

- **Worst-case exponential** — no guarantee of polynomial runtime.
- **Memory intensive** — the BFS queue can hold many nodes.
- **Bound quality matters** — weak bounds reduce pruning effectiveness.
- **Not suitable for very large n** — n > 50 may be intractable in practice.
- **Problem-specific bound** — a good bound must be designed per problem.

---

## 23. Real-World Applications

| Domain                  | Application                                        |
|-------------------------|---------------------------------------------------|
| Resource allocation     | Maximise ROI with budget constraints              |
| Project selection       | Choose projects with limited resources            |
| Cargo loading           | Load ship/aircraft containers for max profit      |
| Portfolio optimisation  | Select investments under capital constraints      |
| Bin packing             | Pack items into fixed-capacity bins               |
| VLSI design             | Placement and routing under area constraints      |
| Scheduling              | Job scheduling with machine capacity limits       |
| Cryptography            | Subset-sum variants in knapsack-based encryption  |

---

## 24. Learning Outcomes

After studying this project, you should be able to:

1. Explain the Branch and Bound strategy (branch, bound, prune).
2. Formulate the 0/1 Knapsack problem mathematically.
3. Compute the fractional knapsack upper bound for any node.
4. Trace the B&B search tree for a given dataset.
5. Identify which nodes get pruned and explain why.
6. Compare B&B with brute force, backtracking, and DP.
7. Analyse the worst-case and practical complexity of B&B.
8. Read and understand the Python implementation.

---

## 25. How to Run

### Requirements
- Python 3.x (no external libraries needed)

### Steps
```bash
# Navigate to the project folder
cd Unit5_BranchAndBound

# Run the program
python3 Project13_Knapsack_BnB.py
```

### Custom Input
Edit the bottom section of `Project13_Knapsack_BnB.py`:
```python
weights    = [2, 3, 4, 5]     # change these
profits    = [40, 50, 65, 70]  # change these
item_names = ["Item1", "Item2", "Item3", "Item4"]
capacity   = 8                 # change this
```

---

## 26. Project Files

```
Unit5_BranchAndBound/
│
├── Project13_Knapsack_BnB.py   Python implementation
├── algorithm.md                Detailed pseudocode and explanation
├── explanation.md              Algorithm and visualization explanation
├── Prompt.txt                  Exact AI prompt for visualization
├── Visualization.png           AI-generated search tree diagram
├── README.md                   This file
├── sample_output.txt           Full program execution output
└── test_cases.txt              6 test cases with expected results
```

---

## 27. Viva Questions

**Q1. What is Branch and Bound?**
Branch and Bound is an algorithm design paradigm for exact combinatorial
optimisation. It systematically explores a state-space tree by branching
on decisions, computing optimistic bounds at each node, and pruning
subtrees that cannot improve upon the current best solution.

**Q2. Why is Branch and Bound used for the Knapsack problem?**
The 0/1 Knapsack problem is NP-Hard with 2ⁿ possible subsets. Branch
and Bound uses the fractional knapsack solution as a tight upper bound,
allowing large portions of the search space to be pruned, making it
far more efficient than brute-force enumeration in practice.

**Q3. What is a "bound" in Branch and Bound?**
A bound is an optimistic estimate of the best solution achievable from
a given node. For maximisation problems, it is an upper bound — no
solution in that subtree can exceed it. If the bound is not better
than the current best, the entire subtree is safely discarded.

**Q4. Why do we calculate an upper bound for 0/1 Knapsack?**
The upper bound tells us the maximum possible profit if we relax the
integer constraint. If this relaxed maximum is still worse than what
we already have, the subtree is guaranteed to contain nothing useful.

**Q5. Why is fractional knapsack used for the bound?**
Fractional knapsack can be solved greedily in O(n log n) and always
gives a result ≥ the 0/1 optimal (because it has fewer constraints).
This makes it an admissible (optimistic) upper bound — the key property
needed for correct pruning. It's also cheap to compute.

**Q6. What is pruning?**
Pruning means discarding a node and its entire subtree without
exploring it. Two types:
- Weight pruning: include-child weight > capacity → infeasible.
- Bound pruning: node's bound ≤ current best → non-promising.

**Q7. When is a node pruned?**
A node is pruned when:
1. Its weight exceeds the knapsack capacity (infeasible), OR
2. Its upper bound is ≤ current best profit (cannot improve).

**Q8. Difference between Branch and Bound vs Backtracking?**

| Feature       | Backtracking               | Branch and Bound           |
|---------------|----------------------------|----------------------------|
| Search        | DFS                        | BFS or Best-First          |
| Bounding      | Feasibility check only     | Optimistic bound function  |
| Pruning       | Infeasibility pruning      | Bound-based + feasibility  |
| Goal          | Find any/all solutions     | Find optimal solution      |
| Efficiency    | Less efficient             | More efficient (tighter pruning) |

**Q9. Difference between 0/1 Knapsack and Fractional Knapsack?**
In 0/1 Knapsack, items must be taken whole or not at all. In Fractional
Knapsack, you can take any fraction of an item. Fractional Knapsack
is solvable greedily in O(n log n); 0/1 Knapsack is NP-Hard.

**Q10. What is the worst-case time complexity of Branch and Bound?**
O(2ⁿ) — in the worst case, no pruning occurs and all nodes are
explored. This happens when the bound is equal to the profit at
every node, giving zero pruning benefit.

**Q11. Why can Branch and Bound be faster in practice?**
The fractional knapsack bound is very tight (close to the true 0/1
optimal). As soon as a good feasible solution is found, many nodes
can be pruned. The higher the best profit, the stricter the pruning
threshold, so later exploration is faster than earlier exploration.

**Q12. What does a node represent in the search tree?**
A node represents a **partial assignment** state: decisions have been
made for some items (included/excluded), and remaining items are
undecided. The node stores the profit, weight, and bound for this state.

**Q13. Why sort items by profit/weight ratio?**
Sorting by P/W ratio ensures the greedy bound fills the most profitable
items first, making the bound as tight as possible. A tighter bound
means more nodes get pruned, which means faster execution.

**Q14. What happens when a node exceeds capacity?**
It is immediately pruned. Adding more items will only increase weight
further (all weights are positive), so no feasible solution exists
in this subtree. The node is discarded without computing a bound.

**Q15. How do we know the final answer is optimal?**
When the queue is empty, every promising node has been explored.
Every pruned node was provably unable to improve upon the best found.
Since the bounding function is admissible (never underestimates the
true optimal), the guarantee is: the best_profit found equals the
true optimal. The algorithm is **exact**, not approximate.

---

## 2-Minute Presentation Script

*"Good morning everyone. I'm presenting Project 13 — 0/1 Knapsack
using Branch and Bound.*

*The problem is simple: we have a bag with limited capacity, and
a set of items with different weights and profits. We want to pick
items that maximise our profit without exceeding the capacity. The
catch is — we can't take half an item. It's all or nothing.*

*Now, brute force would check every possible combination. For 4 items
that's 16 combinations, but for 40 items that's over a trillion.
We need something smarter.*

*That's where Branch and Bound comes in. It builds a decision tree —
at each level, we decide: do we include this item or not? But instead
of exploring every path, we compute an upper bound at each node using
the fractional knapsack trick — which is just a greedy estimate of
the best we could possibly do from here.*

*If that best-case estimate is still worse than what we've already
found, we prune the entire subtree. We don't need to explore it further.*

*In our example with 4 items and capacity 8: the algorithm starts
at the root, calculates a bound of 138.75, and begins exploring.
Whenever it finds a new feasible solution — say profit 90, then 105,
then 115, then finally 120 — it raises the pruning threshold. As the
threshold rises, more and more nodes get cut off.*

*The visualization shows exactly this — green nodes were explored,
red nodes were infeasible, orange nodes had a bound too low to matter.
And the gold path shows the optimal solution: take Item2 and Item4,
profit 120, weight exactly 8.*

*The algorithm is guaranteed to find the optimal solution — it never
prunes a subtree that contains the answer, because the bound is always
an overestimate, never an underestimate.*

*Thank you."*

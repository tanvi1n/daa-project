"""
============================================================
  DAA Macro Project — Unit V: Branch and Bound
  Project 13: 0/1 Knapsack Problem using Branch and Bound
============================================================
  Algorithm  : Branch and Bound (FIFO / BFS Queue)
  Bounding   : Fractional Knapsack upper bound
  Dataset    : 4 items, Capacity = 8
============================================================
"""

from queue import Queue


# ─────────────────────────────────────────────
#  Node: represents a single node in the B&B tree
# ─────────────────────────────────────────────
class Node:
    def __init__(self, level, profit, weight, bound, include_flags):
        """
        level         : which item index this node was decided at (0-indexed)
        profit        : accumulated profit so far
        weight        : accumulated weight so far
        bound         : optimistic upper bound on profit from this node
        include_flags : list of 1/0 decisions for items decided so far
        """
        self.level         = level
        self.profit        = profit
        self.weight        = weight
        self.bound         = bound
        self.include_flags = include_flags

    def __repr__(self):
        flags_str = "".join(str(f) for f in self.include_flags).ljust(4, '?')
        return (f"Node(lvl={self.level}, P={self.profit}, "
                f"W={self.weight}, Bound={self.bound:.2f}, "
                f"Decisions={flags_str})")


# ─────────────────────────────────────────────
#  Upper Bound Calculation (Fractional Knapsack)
# ─────────────────────────────────────────────
def calculate_bound(node, n, capacity, items):
    """
    Calculates the optimistic upper bound for a node using the
    fractional knapsack relaxation.

    Items must be sorted by profit/weight ratio in descending order.
    Returns the upper bound (float).
    """
    if node.weight >= capacity:
        return 0

    profit_bound = float(node.profit)
    j            = node.level + 1
    total_weight = node.weight

    while j < n and total_weight + items[j][0] <= capacity:
        total_weight  += items[j][0]
        profit_bound  += items[j][1]
        j             += 1

    if j < n:
        remaining_capacity = capacity - total_weight
        profit_bound += (remaining_capacity / items[j][0]) * items[j][1]

    return profit_bound


# ─────────────────────────────────────────────
#  Branch and Bound Solver
# ─────────────────────────────────────────────
def knapsack_branch_and_bound(capacity, weights, profits, item_names):
    """
    Solves the 0/1 Knapsack problem using Branch and Bound.

    Parameters
    ----------
    capacity   : int   – knapsack capacity
    weights    : list  – item weights
    profits    : list  – item profits
    item_names : list  – display names for items

    Returns
    -------
    best_profit : int
    best_items  : list of item names included
    """

    n = len(weights)

    # ── Step 1: Sort items by profit/weight ratio (descending) ──
    items = sorted(
        zip(weights, profits, item_names),
        key=lambda x: x[1] / x[0],
        reverse=True
    )
    sorted_weights  = [it[0] for it in items]
    sorted_profits  = [it[1] for it in items]
    sorted_names    = [it[2] for it in items]
    items_wt_prof   = list(zip(sorted_weights, sorted_profits))

    print("=" * 62)
    print("   0/1 KNAPSACK — BRANCH AND BOUND")
    print("=" * 62)
    print(f"\n  Knapsack Capacity : {capacity}")
    print(f"\n  {'Item':<10} {'Weight':>8} {'Profit':>8} {'P/W Ratio':>12}")
    print("  " + "-" * 42)
    for i, (w, p, nm) in enumerate(items):
        print(f"  {nm:<10} {w:>8} {p:>8} {p/w:>12.2f}")
    print()

    # ── Step 2: Initialise ──
    best_profit    = 0
    best_flags     = [0] * n
    node_count     = 0

    root            = Node(level=-1, profit=0, weight=0,
                           bound=0, include_flags=[])
    root.bound      = calculate_bound(root, n, capacity, items_wt_prof)

    queue = Queue()
    queue.put(root)

    print("-" * 62)
    print(f"  {'Node':>5}  {'Lvl':>4}  {'W':>5}  {'P':>6}  {'Bound':>8}  Action")
    print("-" * 62)

    # ── Step 3: BFS exploration ──
    while not queue.empty():
        current = queue.get()

        if current.bound <= best_profit:
            if current.level != -1:
                print(f"  {'--':>5}  {current.level:>4}  "
                      f"{current.weight:>5}  {current.profit:>6}  "
                      f"{current.bound:>8.2f}  PRUNED (bound ≤ best)")
            continue

        next_level = current.level + 1

        if next_level < n:
            # --- Left child: INCLUDE item at next_level ---
            lc_weight = current.weight + sorted_weights[next_level]
            lc_profit = current.profit + sorted_profits[next_level]
            lc_flags  = current.include_flags + [1]
            node_count += 1

            if lc_weight <= capacity and lc_profit > best_profit:
                best_profit = lc_profit
                best_flags  = lc_flags + [0] * (n - len(lc_flags))

            left_child        = Node(next_level, lc_profit, lc_weight,
                                     0, lc_flags)
            left_child.bound  = calculate_bound(left_child, n, capacity,
                                                items_wt_prof)

            action = "EXPAND"
            if lc_weight > capacity:
                action = "PRUNED (weight > capacity)"
            elif left_child.bound <= best_profit:
                action = "PRUNED (bound ≤ best)"

            print(f"  {node_count:>5}  {next_level:>4}  "
                  f"{lc_weight:>5}  {lc_profit:>6}  "
                  f"{left_child.bound:>8.2f}  "
                  f"Incl {sorted_names[next_level]:<10} → {action}")

            if action == "EXPAND":
                queue.put(left_child)

            # --- Right child: EXCLUDE item at next_level ---
            node_count  += 1
            rc_flags     = current.include_flags + [0]
            right_child  = Node(next_level, current.profit, current.weight,
                                0, rc_flags)
            right_child.bound = calculate_bound(right_child, n, capacity,
                                                items_wt_prof)

            r_action = "EXPAND"
            if right_child.bound <= best_profit:
                r_action = "PRUNED (bound ≤ best)"

            print(f"  {node_count:>5}  {next_level:>4}  "
                  f"{current.weight:>5}  {current.profit:>6}  "
                  f"{right_child.bound:>8.2f}  "
                  f"Excl {sorted_names[next_level]:<10} → {r_action}")

            if r_action == "EXPAND":
                queue.put(right_child)

    # ── Step 4: Recover selected items ──
    selected = []
    for i, flag in enumerate(best_flags[:n]):
        if flag == 1:
            selected.append(sorted_names[i])

    total_weight = sum(
        sorted_weights[i] for i in range(n) if best_flags[i] == 1
    )

    print("-" * 62)
    print("\n  ╔══════════════════════════════════════╗")
    print(f"  ║  Optimal Profit  : {best_profit:<19}║")
    print(f"  ║  Selected Items  : {', '.join(selected):<19}║")
    print(f"  ║  Total Weight    : {total_weight:<19}║")
    print(f"  ║  Capacity Used   : {total_weight}/{capacity:<17}║")
    print("  ╚══════════════════════════════════════╝\n")

    return best_profit, selected


# ─────────────────────────────────────────────
#  Main Entry Point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    weights    = [2, 3, 4, 5]
    profits    = [40, 50, 65, 70]
    item_names = ["Item1", "Item2", "Item3", "Item4"]
    capacity   = 8

    knapsack_branch_and_bound(capacity, weights, profits, item_names)

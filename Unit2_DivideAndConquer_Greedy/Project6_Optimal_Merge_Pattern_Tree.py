"""
Optimal Merge Pattern - Pseudocode (Unit II, Project 6, Greedy method)

Problem:
    Given n sorted files, merging two files of sizes a and b costs a + b.
    Find the order of merges that minimizes the total cost.
    Input for this project: files of sizes 10, 20, 30, 40.

This file holds the PSEUDOCODE only (it is not meant to be executed).
The working implementation is in Project6_OptimalMergePattern.py.

------------------------------------------------------------------
OptimalMerge(sizes[1..n])
    1.  Create a min-heap H and insert all file sizes
    2.  totalCost <- 0
    3.  while H contains more than one element do
    4.      a <- ExtractMin(H)          // smallest file
    5.      b <- ExtractMin(H)          // second smallest file
    6.      merged <- a + b             // cost of this merge
    7.      totalCost <- totalCost + merged
    8.      Insert(H, merged)           // merged file goes back into heap
    9.  end while
    10. return totalCost
------------------------------------------------------------------

Greedy choice:
    Always merge the two smallest files. Merged files are re-counted in
    later merges, so small files are merged first and sit deepest in the tree.

Dry run (10, 20, 30, 40):
    Step 1: 10 + 20  = 30   cost 30    heap -> 30, 30, 40
    Step 2: 30 + 30  = 60   cost 60    heap -> 40, 60
    Step 3: 40 + 60  = 100  cost 100   heap -> 100
    Total minimum cost = 30 + 60 + 100 = 190

Complexity:
    Time  : O(n log n)  - (n-1) iterations, each O(log n) heap operations
    Space : O(n)        - the heap
"""
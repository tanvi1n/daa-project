# Project Title
Optimal Merge Pattern using Greedy Method (Weighted Merge Tree)

## Description
Given several sorted files, merging two files of sizes a and b costs a + b.
This project finds the order of merges that minimizes the total cost for files
of sizes 10, 20, 30 and 40, implements it in Python with a min-heap, and
visualizes the result as a weighted binary merge tree.

## Algorithm
```
OptimalMerge(sizes[1..n])
    create min-heap H containing all file sizes
    totalCost <- 0
    while H has more than one element
        a <- ExtractMin(H)
        b <- ExtractMin(H)
        merged <- a + b
        totalCost <- totalCost + merged
        Insert(H, merged)
    return totalCost
```
Greedy choice: always merge the two smallest files, so small files are pushed
deepest in the tree and are re-counted the most times, while large files are
counted fewest times.

**Complexity:** O(n log n)time(n heap extractions/insertions), O(n)space.

## Worked Example (10, 20, 30, 40)
| Step | Merge | Result | Cost |
|------|-------|--------|------|
| 1 | 10 + 20 | 30 | 30 |
| 2 | 30 + 30 | 60 | 60 |
| 3 | 40 + 60 | 100 | 100 |

**Minimum total cost = 30 + 60 + 100 = 190**

## Prompt Used
"Draw a binary tree showing optimal merge pattern for files of sizes 10, 20, 30, 40."

## Output
![Merge tree](Visualization.png)

Leaf nodes (blue) are the original files; internal nodes (orange) hold the
size of the merged file. Reading from the bottom up shows the merge order.
Edges are labelled 0/1. The root (100) is the final merged file, and the sum of
all internal node weights (30 + 60 + 100) is the total cost.



## How to Run
```
pip install matplotlib
python Project6_OptimalMergePattern.py
```

## Learning Outcome
- Understood the greedy strategy behind optimal merge patterns and its link to Huffman coding.
- Used a min-heap to implement the greedy choice in O(n log n).
- Learned prompt-based visualization of weighted trees.
- Practiced GitHub documentation.


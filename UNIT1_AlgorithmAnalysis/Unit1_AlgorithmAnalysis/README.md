# Recursion Tree for Merge Sort

**Course:** Design and Analysis of Algorithms (DAA)  
**Group:** 11  
**Unit:** I — Algorithm Analysis  
**Assigned topic:** 2. Recursion Tree for Merge Sort

## Description
This project illustrates how Merge Sort recursively divides an array of eight elements into single-element subarrays and then merges those subarrays in sorted order.

Input array: `[38, 27, 43, 3, 9, 82, 10, 1]`  
Expected sorted output: `[1, 3, 9, 10, 27, 38, 43, 82]`

## Algorithm (pseudocode)
```text
MERGE-SORT(A):
    if length(A) <= 1:
        return A
    mid = floor(length(A) / 2)
    left = MERGE-SORT(A[0 : mid])
    right = MERGE-SORT(A[mid : length(A)])
    return MERGE(left, right)

MERGE(L, R):
    create empty result
    while both L and R contain unprocessed elements:
        append the smaller front element to result
        advance the corresponding pointer
    append any remaining elements from L and R
    return result
```

## How the recursion tree works
1. The root contains the complete input array.
2. Each call splits its array into a left and right half.
3. Splitting continues until every leaf contains one element; a one-element array is already sorted.
4. The algorithm merges neighboring sorted subarrays, producing progressively larger sorted arrays.
5. The root-level merge produces the fully sorted array.

## Complexity analysis
- **Best, average, and worst-case time:** `Θ(n log n)`
- **Auxiliary space:** `Θ(n)` for the temporary arrays used by merging
- **Recursion depth:** `Θ(log n)`

The recurrence is `T(n) = 2T(n/2) + Θ(n)`, with `T(1) = Θ(1)`. By the Master Theorem, `T(n) = Θ(n log n)`.

## Files
- `Project2_RecursionTree_MergeSort.py` — executable Python implementation
- `Prompt.txt` — prompt used to specify the visualization
- `Visualization.png` — recursion and merge tree
- `README.md` — project documentation

## Run the program
Requires Python 3. Run:
```bash
python Project2_RecursionTree_MergeSort.py
```
Expected output:
```text
Original array: [38, 27, 43, 3, 9, 82, 10, 1]
Sorted array:   [1, 3, 9, 10, 27, 38, 43, 82]
```

## Learning outcomes
- Understand recursive divide-and-conquer decomposition.
- Trace the base case and recursive calls in Merge Sort.
- Connect the recursion tree to the `Θ(n log n)` time complexity.

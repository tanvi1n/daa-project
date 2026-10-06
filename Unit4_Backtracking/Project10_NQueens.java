/**
 * Project 10 - N-Queens State Space Tree (Unit 4: Backtracking)
 *
 * Solves the N-Queens problem for N = 4 using recursive backtracking and prints
 * every exploration step, i.e. every node of the state-space tree:
 *   - each (row, col) attempt is one node of the tree,
 *   - an unsafe attempt is an INVALID (pruned / red) branch,
 *   - a safe attempt is placed and the search recurses into the next row,
 *   - after the recursive call returns, the queen is removed (backtracking).
 *
 * Rows and columns are numbered 1..N, exactly as in the visualizer.
 *
 * Run:  javac Project10_NQueens.java
 *       java Project10_NQueens
 */
public class Project10_NQueens {

    static final int N = 4;

    static int[] col = new int[N + 1];   // col[r] = column of the queen in row r (0 = empty)
    static int nodes = 0;                // tree nodes generated (every attempt)
    static int pruned = 0;               // invalid (red) nodes
    static int solutions = 0;

    /** Returns null if (row, c) is safe, otherwise the reason it is not. */
    static String conflict(int row, int c) {
        for (int r = 1; r < row; r++) {
            if (col[r] == c)
                return "column conflict with queen at (R" + r + ", C" + col[r] + ")";
            if (Math.abs(col[r] - c) == row - r)
                return "diagonal conflict with queen at (R" + r + ", C" + col[r] + ")";
        }
        return null;
    }

    static boolean isSafe(int row, int c) {
        return conflict(row, c) == null;
    }

    /** Recursive backtracking: place one queen in `row`, then recurse into row + 1. */
    static void solve(int row) {
        if (row > N) {                              // all N queens placed
            solutions++;
            printSolution();
            return;
        }
        String indent = "  ".repeat(row - 1);
        for (int c = 1; c <= N; c++) {              // try every column of this row
            nodes++;
            if (isSafe(row, c)) {
                System.out.println(indent + "Row " + row + ", Col " + c + " -> valid, place queen");
                col[row] = c;                       // place queen
                solve(row + 1);                     // recurse into the next row
                col[row] = 0;                       // BACKTRACK: remove queen
                System.out.println(indent + "Row " + row + ", Col " + c + " -> backtrack (queen removed)");
            } else {
                pruned++;                           // invalid branch (red in the tree)
                System.out.println(indent + "Row " + row + ", Col " + c + " -> INVALID, " + conflict(row, c));
            }
        }
    }

    static void printSolution() {
        System.out.println("*** Solution " + solutions + " found ***");
        for (int r = 1; r <= N; r++) {
            StringBuilder sb = new StringBuilder("      ");
            for (int c = 1; c <= N; c++) sb.append(col[r] == c ? "Q " : ". ");
            System.out.println(sb);
        }
    }

    public static void main(String[] args) {
        System.out.println("N-Queens backtracking, N = " + N + "\n");
        solve(1);
        System.out.println("\nSolutions found     : " + solutions);
        System.out.println("Tree nodes explored : " + nodes + " (excluding the Start node)");
        System.out.println("Invalid (red) nodes : " + pruned);
        System.out.println("Valid nodes         : " + (nodes - pruned));
    }
}

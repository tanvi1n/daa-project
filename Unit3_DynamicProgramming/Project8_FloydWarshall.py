# =============================================================================
# Project 8 – All-Pairs Shortest Path Matrix Update
# Topic   : Floyd-Warshall Algorithm
# Course  : Design and Analysis of Algorithms (DAA)
# =============================================================================
# This Streamlit application demonstrates the Floyd-Warshall algorithm by
# showing how the distance matrix is iteratively updated as each vertex is
# used as an intermediate vertex (k = A, B, C, D).
# =============================================================================

import copy
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# 1.  ALGORITHM CORE
# ─────────────────────────────────────────────────────────────────────────────

INF = float("inf")   # Represents ∞ (no direct path)

VERTICES = ["A", "B", "C", "D"]   # Label for each vertex index

# Initial distance matrix (rows = source, cols = destination)
#         A     B     C     D
INITIAL = [
    [0,   3,   INF, 7  ],   # A
    [8,   0,   2,   INF],   # B
    [5,   INF, 0,   1  ],   # C
    [2,   INF, INF, 0  ],   # D
]


def run_floyd_warshall(initial_matrix):
    """
    Run the full Floyd-Warshall algorithm and capture a snapshot of the
    distance matrix after every iteration of k.

    Returns
    -------
    matrices : list of 5 matrices
        matrices[0]  = initial state (before any k)
        matrices[k+1] = state after using vertex k as intermediate
    changes  : list of 5 change-sets
        changes[0]   = [] (no changes before first k)
        changes[k+1] = list of (i, j, old_value, new_value) tuples
    """
    n = len(initial_matrix)
    matrices = [copy.deepcopy(initial_matrix)]   # snapshot 0 = initial
    changes  = [[]]                              # no changes at step 0

    D = copy.deepcopy(initial_matrix)

    for k in range(n):                           # k iterates over every vertex
        new_D = copy.deepcopy(D)
        iteration_changes = []

        for i in range(n):
            for j in range(n):
                # Skip if no path through k is possible
                if D[i][k] == INF or D[k][j] == INF:
                    continue

                candidate = D[i][k] + D[k][j]   # cost via intermediate k

                # Core Floyd-Warshall formula: relax the edge (i → j)
                if candidate < D[i][j]:
                    old_val = D[i][j]
                    new_D[i][j] = candidate
                    iteration_changes.append((i, j, old_val, candidate))

        D = new_D
        matrices.append(copy.deepcopy(D))
        changes.append(iteration_changes)

    return matrices, changes


# Pre-compute all snapshots once at module load (cached via session state)
MATRICES, CHANGES = run_floyd_warshall(INITIAL)


# ─────────────────────────────────────────────────────────────────────────────
# 2.  HELPER UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

def fmt(value):
    """Format a matrix cell: replace float infinity with the ∞ symbol."""
    return "∞" if value == INF else str(int(value))


def build_matrix_html(matrix, changed_cells):
    """
    Render the distance matrix as a styled HTML table.

    Parameters
    ----------
    matrix        : 2-D list of numbers (current state)
    changed_cells : set of (i, j) tuples whose values changed this iteration
    """
    n = len(VERTICES)

    # ── Table wrapper ──────────────────────────────────────────────────────
    html = """
    <style>
      .fw-table {
        border-collapse: collapse;
        font-family: 'Courier New', monospace;
        font-size: 18px;
        margin: 0 auto;
      }
      .fw-table th {
        background-color: #1e3a5f;
        color: #ffffff;
        padding: 12px 22px;
        text-align: center;
        border: 2px solid #aaa;
        font-size: 17px;
      }
      .fw-table td {
        padding: 12px 22px;
        text-align: center;
        border: 2px solid #aaa;
        font-size: 17px;
        background-color: #f8f9fa;
        color: #333;
      }
      .fw-table td.row-header {
        background-color: #1e3a5f;
        color: #ffffff;
        font-weight: bold;
      }
      .fw-table td.changed {
        background-color: #fff3cd;
        color: #333;
        font-weight: bold;
        border: 2px solid #f0ad4e;
      }
      .fw-table td.diagonal {
        background-color: #e8f5e9;
        color: #555;
      }
    </style>
    <table class="fw-table">
      <tr>
        <th></th>
    """

    # Column headers
    for v in VERTICES:
        html += f"<th>{v}</th>"
    html += "</tr>"

    # Data rows
    for i in range(n):
        html += "<tr>"
        html += f'<td class="row-header">{VERTICES[i]}</td>'
        for j in range(n):
            val = fmt(matrix[i][j])
            if i == j:
                css = "diagonal"
            elif (i, j) in changed_cells:
                css = "changed"
            else:
                css = ""
            html += f'<td class="{css}">{val}</td>'
        html += "</tr>"

    html += "</table>"
    return html


def build_change_summary(step):
    """
    Return a human-readable list describing every cell update that occurred
    in the given step.  step 0 = initial (no changes).  step 1..4 = k=A..D
    """
    if step == 0:
        return []

    k_label = VERTICES[step - 1]
    prev    = MATRICES[step - 1]
    summary = []

    for (i, j, old, new) in CHANGES[step]:
        old_str = "∞" if old == INF else str(int(old))
        summary.append(
            f"**D[{VERTICES[i]}][{VERTICES[j]}]**: "
            f"{old_str} → **{int(new)}** "
            f"&nbsp;&nbsp; *(path: {VERTICES[i]} → {k_label} → {VERTICES[j]})*"
        )

    return summary


# ─────────────────────────────────────────────────────────────────────────────
# 3.  STREAMLIT PAGE SETUP
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Floyd-Warshall Visualizer",
    page_icon="🔷",
    layout="centered",
)

# ── Session state: tracks which iteration step we are viewing ──────────────
# step 0 = initial matrix  |  step 1..4 = after k=A, B, C, D
if "step" not in st.session_state:
    st.session_state.step = 0

MAX_STEP = len(MATRICES) - 1   # = 4


# ─────────────────────────────────────────────────────────────────────────────
# 4.  PAGE HEADER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(
    "<h1 style='text-align:center; color:#1e3a5f;'>"
    "🔷 Floyd-Warshall Algorithm</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h4 style='text-align:center; color:#555;'>"
    "All-Pairs Shortest Path – Stepwise Matrix Visualization</h4>",
    unsafe_allow_html=True,
)
st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
# 5.  FORMULA BANNER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(
    """
    <div style='
        background-color:#1e3a5f;
        color:white;
        padding:14px 20px;
        border-radius:8px;
        text-align:center;
        font-family:Courier New, monospace;
        font-size:20px;
        letter-spacing:1px;
        margin-bottom:18px;
    '>
        <b>Core Formula :</b> &nbsp; D[i][j] = min( D[i][j] , D[i][k] + D[k][j] )
    </div>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# 6.  CURRENT STEP INFO
# ─────────────────────────────────────────────────────────────────────────────

step = st.session_state.step

if step == 0:
    step_title   = "Initial Distance Matrix"
    step_sub     = "No intermediate vertex used yet."
    badge_color  = "#6c757d"
    badge_text   = "Initial State"
elif step <= MAX_STEP:
    k_label      = VERTICES[step - 1]
    step_title   = f"Iteration {step}: Using **{k_label}** as Intermediate Vertex"
    step_sub     = (
        f"For every pair (i, j), check if going through **{k_label}** gives "
        f"a shorter path than the current best."
    )
    badge_color  = "#1e3a5f"
    badge_text   = f"k = {k_label}"

col_title, col_badge = st.columns([3, 1])

with col_title:
    st.markdown(f"### {step_title}")
    st.caption(step_sub)

with col_badge:
    st.markdown(
        f"""
        <div style='
            background:{badge_color};
            color:white;
            border-radius:50%;
            width:80px; height:80px;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:18px;
            font-weight:bold;
            margin:auto;
            font-family:Courier New, monospace;
        '>{badge_text}</div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# 7.  DISTANCE MATRIX TABLE
# ─────────────────────────────────────────────────────────────────────────────

# Build the set of (i,j) positions that changed in this step
changed_cells = set()
if step > 0:
    for (i, j, _, _) in CHANGES[step]:
        changed_cells.add((i, j))

matrix_html = build_matrix_html(MATRICES[step], changed_cells)
st.markdown(matrix_html, unsafe_allow_html=True)

# Legend row
if step > 0:
    st.markdown(
        """
        <div style='text-align:center; margin-top:10px; font-size:14px; color:#555;'>
            <span style='background:#fff3cd; padding:3px 10px; border:1px solid #f0ad4e;
                         border-radius:4px; margin-right:10px;'>
                🟡 Updated cell
            </span>
            <span style='background:#e8f5e9; padding:3px 10px; border:1px solid #aaa;
                         border-radius:4px;'>
                🟢 Diagonal (distance to self = 0)
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")   # spacing


# ─────────────────────────────────────────────────────────────────────────────
# 8.  CHANGE SUMMARY
# ─────────────────────────────────────────────────────────────────────────────

with st.expander("📋 What changed in this iteration?", expanded=(step > 0)):
    if step == 0:
        st.info(
            "This is the **initial distance matrix** loaded from the graph.  \n"
            "Direct edge weights are shown; ∞ means no direct edge exists.  \n"
            "Press **Next ▶** to begin the first iteration."
        )
    else:
        k_label   = VERTICES[step - 1]
        summary   = build_change_summary(step)
        num_cells = len(summary)

        if num_cells == 0:
            st.success(
                f"No cells were updated in iteration k = **{k_label}**.  \n"
                "The existing paths were already optimal through this vertex."
            )
        else:
            st.markdown(
                f"**{num_cells} cell(s) updated** when using "
                f"**{k_label}** as the intermediate vertex:"
            )
            for line in summary:
                st.markdown(f"- {line}")

        # Brief explanation of this specific iteration
        explanations = {
            "A": (
                "Using **A** as a relay point revealed three new shorter paths:\n"
                "- B→D through A costs 8+7=15 (was ∞)\n"
                "- C→B through A costs 5+3=8 (was ∞)\n"
                "- D→B through A costs 2+3=5 (was ∞)"
            ),
            "B": (
                "Using **B** as a relay point filled in two unreachable paths:\n"
                "- A→C through B costs 3+2=5 (was ∞)\n"
                "- D→C through B costs 5+2=7 (was ∞)"
            ),
            "C": (
                "Using **C** as a relay improved three paths:\n"
                "- A→D through C costs 5+1=6 (was 7 — improved!)\n"
                "- B→A through C costs 2+5=7 (was 8 — improved!)\n"
                "- B→D through C costs 2+1=3 (was 15 — improved!)"
            ),
            "D": (
                "Using **D** as a relay improved three more paths:\n"
                "- B→A through D costs 3+2=5 (was 7 — improved!)\n"
                "- C→A through D costs 1+2=3 (was 5 — improved!)\n"
                "- C→B through D costs 1+5=6 (was 8 — improved!)"
            ),
        }
        if k_label in explanations:
            st.markdown("---")
            st.markdown("**Explanation:**")
            st.markdown(explanations[k_label])


# ─────────────────────────────────────────────────────────────────────────────
# 9.  NAVIGATION BUTTONS
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("---")

# ── Progress bar ──────────────────────────────────────────────────────────────
progress_label = (
    "Initial" if step == 0
    else ("Final" if step == MAX_STEP else f"Step {step} / {MAX_STEP}")
)
st.progress(step / MAX_STEP, text=f"Progress: {progress_label}")

# ── Button row ────────────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

with col1:
    if st.button("⏮ Reset", use_container_width=True):
        st.session_state.step = 0
        st.rerun()

with col2:
    prev_disabled = (step == 0)
    if st.button("◀ Previous", disabled=prev_disabled, use_container_width=True):
        st.session_state.step -= 1
        st.rerun()

with col3:
    next_disabled = (step == MAX_STEP)
    if st.button("Next ▶", disabled=next_disabled, use_container_width=True):
        st.session_state.step += 1
        st.rerun()

with col4:
    if st.button("⏭ Final", use_container_width=True):
        st.session_state.step = MAX_STEP
        st.rerun()

with col5:
    # Auto-run: jump step by step using a flag in session state
    if "auto_run" not in st.session_state:
        st.session_state.auto_run = False

    if st.button("▶▶ Auto Run", use_container_width=True):
        # Reset to initial, then advance one step at a time via rerun loop
        if st.session_state.step == MAX_STEP:
            st.session_state.step = 0   # restart from beginning
        st.session_state.auto_run = True
        st.rerun()


# Auto-run logic: advance one step per rerun with a short delay
if st.session_state.auto_run:
    import time
    if step < MAX_STEP:
        time.sleep(1.2)                 # pause between steps
        st.session_state.step += 1
        st.rerun()
    else:
        st.session_state.auto_run = False   # stop when done


# ─────────────────────────────────────────────────────────────────────────────
# 10.  FINAL MATRIX PANEL (shown only when on the last step)
# ─────────────────────────────────────────────────────────────────────────────

if step == MAX_STEP:
    st.markdown("---")
    st.markdown(
        "<h3 style='text-align:center; color:#155724;'>"
        "✅ Final Shortest Path Matrix</h3>",
        unsafe_allow_html=True,
    )
    st.success(
        "The algorithm has completed all iterations.  \n"
        "Every cell D[i][j] now contains the **shortest path distance** "
        "from vertex i to vertex j, considering all possible intermediate vertices."
    )

    # Side-by-side: initial vs final
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Initial Matrix**")
        st.markdown(
            build_matrix_html(MATRICES[0], set()),
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown("**Final Shortest-Path Matrix**")
        st.markdown(
            build_matrix_html(MATRICES[MAX_STEP], set()),
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# 11.  ALGORITHM INFO SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 📖 About Floyd-Warshall")
    st.markdown(
        """
        **Floyd-Warshall** is a classic **Dynamic Programming** algorithm
        that finds shortest paths between **all pairs** of vertices in a
        weighted graph.

        ---
        ### Key Properties
        | Property | Value |
        |---|---|
        | Time Complexity | O(V³) |
        | Space Complexity | O(V²) |
        | Works with | Negative edges |
        | Detects | Negative cycles |

        ---
        ### Formula
        ```
        D[i][j] = min(
            D[i][j],
            D[i][k] + D[k][j]
        )
        ```

        ---
        ### Pseudocode
        ```
        for k in vertices:
          for i in vertices:
            for j in vertices:
              if D[i][k] + D[k][j]
                   < D[i][j]:
                D[i][j] = D[i][k]
                           + D[k][j]
        ```

        ---
        ### Sample Graph Edges
        | From | To | Weight |
        |---|---|---|
        | A | B | 3 |
        | A | D | 7 |
        | B | A | 8 |
        | B | C | 2 |
        | C | A | 5 |
        | C | D | 1 |
        | D | A | 2 |
        """
    )

    st.markdown("---")
    st.markdown("**DAA – Unit 3: Dynamic Programming**")
    st.caption("Project 8 – All-Pairs Shortest Path")

from math import isqrt
from typing import List, Tuple, Optional

Grid = List[List[int]]

def is_unique_solution(grid: Grid) -> bool:
    """
    Return True if the given Sudoku grid has exactly one solution, else False.
    - grid: 2D list of ints; 0 denotes empty.
    Supports n^2 x n^2 Sudoku (e.g., 9x9, 16x16) as long as entries are 0..n^2.
    """
    n2 = len(grid)
    if n2 == 0 or any(len(row) != n2 for row in grid):
        raise ValueError("Grid must be square (n^2 x n^2).")
    n = isqrt(n2)
    if n * n != n2:
        raise ValueError("Side length must be a perfect square (e.g., 9, 16).")

    # Bitmask helpers
    # For values 1..n2, we use bits 0..(n2-1)
    FULL = (1 << n2) - 1
    def bit(v: int) -> int:
        return 1 << (v - 1)

    # Row/Col/Box masks of used digits (bit=1 means digit already used)
    row_used = [0] * n2
    col_used = [0] * n2
    box_used = [0] * n2

    empties: List[Tuple[int, int]] = []

    # Initialize masks; validate existing digits
    for r in range(n2):
        for c in range(n2):
            v = grid[r][c]
            if v == 0:
                empties.append((r, c))
            else:
                if not (1 <= v <= n2):
                    raise ValueError(f"Value out of range at ({r},{c}): {v}")
                b = (r // n) * n + (c // n)
                mask = bit(v)
                if (row_used[r] & mask) or (col_used[c] & mask) or (box_used[b] & mask):
                    # Duplicate in row/col/box → no solution
                    return False
                row_used[r] |= mask
                col_used[c] |= mask
                box_used[b] |= mask

    # Count solutions up to 2 (early stop once we find 2)
    sol_count = 0

    def select_cell() -> Optional[Tuple[int, int, int]]:
        """
        MRV heuristic: pick the empty cell with the fewest candidates.
        Returns (r, c, candidates_mask) or None if no empties left.
        """
        best_idx = -1
        best_mask = 0
        best_count = n2 + 1

        for i, (r, c) in enumerate(empties):
            if grid[r][c] != 0:
                continue
            b = (r // n) * n + (c // n)
            used = row_used[r] | col_used[c] | box_used[b]
            cand_mask = FULL & ~used
            # No candidates -> dead end
            if cand_mask == 0:
                return r, c, 0
            # Count bits (number of candidates)
            cnt = cand_mask.bit_count()
            if cnt < best_count:
                best_count = cnt
                best_mask = cand_mask
                best_idx = i
                if cnt == 1:  # cannot do better
                    break
        if best_idx == -1:
            return None
        # Move this cell to front to reduce future scans (optional)
        empties[0], empties[best_idx] = empties[best_idx], empties[0]
        r, c = empties[0]
        return r, c, best_mask

    def dfs() -> bool:
        nonlocal sol_count
        if sol_count >= 2:
            return True  # early terminate
        sel = select_cell()
        if sel is None:
            # All filled → one solution found
            sol_count += 1
            return sol_count >= 2
        r, c, cand_mask = sel
        if cand_mask == 0:
            return False

        b = (r // n) * n + (c // n)

        # Try candidates (least to greatest)
        m = cand_mask
        while m:
            lsb = m & -m
            v = (lsb.bit_length() - 1) + 1  # convert bit -> value
            # place
            grid[r][c] = v
            row_used[r] |= lsb
            col_used[c] |= lsb
            box_used[b] |= lsb

            dfs()
            if sol_count >= 2:
                return True

            # undo
            row_used[r] &= ~lsb
            col_used[c] &= ~lsb
            box_used[b] &= ~lsb
            box_used[b] &= ~lsb
            grid[r][c] = 0

            m &= m - 1  # pop lsb

        return False

    dfs()
    return sol_count == 1

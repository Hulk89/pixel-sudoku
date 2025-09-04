from math import isqrt
from typing import List, Tuple, Optional

Grid = List[List[int]]

def is_unique_solution(grid: Grid) -> bool:
    """
    Return True if the given Sudoku grid has exactly one solution, else False.
    - grid: 2D list of ints; 0 denotes empty.
    Supports n^2 x n^2 Sudoku (e.g., 9x9, 16x16) as long as entries are 0..n^2.
    """
    new_grid = [row[:] for row in grid]
    # Bitmask helpers
    def bit(v: int) -> int:
        return 1 << (v - 1)

    n2 = len(new_grid)
    if n2 == 0 or any(len(row) != n2 for row in new_grid):
        raise ValueError("Grid must be square (n^2 x n^2).")
    n = isqrt(n2)
    if n * n != n2:
        raise ValueError("Side length must be a perfect square (e.g., 9, 16).")

    # For values 1..n2, we use bits 0..(n2-1)
    FULL = (1 << n2) - 1

    # Row/Col/Box masks of used digits (bit=1 means digit already used)
    row_used = [0] * n2
    col_used = [0] * n2
    box_used = [0] * n2

    empties: List[Tuple[int, int]] = []

    # Initialize masks; validate existing digits
    for row in range(n2):
        for col in range(n2):
            value = new_grid[row][col]
            if value == 0:
                empties.append((row, col))
            else:
                if not (1 <= value <= n2):
                    raise ValueError(f"Value out of range at ({row},{col}): {value}")
                box_index = (row // n) * n + (col // n)
                mask = bit(value)
                if (row_used[row] & mask) or (col_used[col] & mask) or (box_used[box_index] & mask):
                    # Duplicate in row/col/box → no solution
                    return False
                row_used[row] |= mask
                col_used[col] |= mask
                box_used[box_index] |= mask

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

        for i, (row, col) in enumerate(empties):
            if new_grid[row][col] != 0:
                continue
            box_index = (row // n) * n + (col // n)
            # NOTE: row와 col, box에서 하나라도 썼으면 used의 bit는 1
            # 따라서 unused_count는 하나도 안쓴 number의 갯수를 샌다.
            used = row_used[row] | col_used[col] | box_used[box_index]
            cand_mask = FULL & ~used

            # No candidates -> dead end
            if cand_mask == 0:
                return row, col, 0
            # Count bits (number of candidates)
            unused_count = cand_mask.bit_count()
            if unused_count < best_count:
                best_count = unused_count
                best_mask = cand_mask
                best_idx = i
                if unused_count == 1:  # cannot do better
                    break
        if best_idx == -1:
            return None
        # Move this cell to front to reduce future scans (optional)
        empties[0], empties[best_idx] = empties[best_idx], empties[0]
        row, col = empties[0]
        return row, col, best_mask

    def dfs():
        nonlocal sol_count
        if sol_count >= 2:
            return
        sel = select_cell()
        if sel is None:
            # All filled → one solution found
            sol_count += 1
            return
        row, col, cand_mask = sel
        if cand_mask == 0:
            return

        box_index = (row // n) * n + (col // n)

        # Try candidates (least to greatest)
        m = cand_mask
        while m:
            lsb = m & -m
            number_value = lsb.bit_length()  # bit to number
            # place
            new_grid[row][col] = number_value
            row_used[row] |= lsb
            col_used[col] |= lsb
            box_used[box_index] |= lsb

            dfs()
            if sol_count >= 2:
                return

            # undo
            row_used[row] &= ~lsb
            col_used[col] &= ~lsb
            box_used[box_index] &= ~lsb
            box_used[box_index] &= ~lsb
            new_grid[row][col] = 0

            m &= m - 1  # pop lsb

        return

    dfs()
    return sol_count == 1

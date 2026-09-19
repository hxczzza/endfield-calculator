"""Endfield 数织求解器。

棋盘中的 0 表示未知格，1 表示需要填充，-1 表示不能填充。
初始障碍只限制可填位置，不计入行列目标数。
"""

from itertools import combinations


UNKNOWN = 0
FILLED = 1
EMPTY = -1


def _normalise_blocked(board_size, blocked):
    """把坐标集合或二维状态表统一为障碍坐标集合。"""
    if blocked is None:
        return set()

    if isinstance(blocked, (list, tuple)) and len(blocked) == board_size:
        if all(isinstance(row, (list, tuple)) and len(row) == board_size for row in blocked):
            return {
                (row, col)
                for row in range(board_size)
                for col in range(board_size)
                if blocked[row][col] == EMPTY
            }

    return {tuple(position) for position in blocked}


def solve(board_size, row_targets, col_targets, blocked=None):
    """返回所有满足行列目标且避开初始障碍的解。

    参数 ``blocked`` 可传 ``{(行, 列), ...}``，也可传 n×n 状态表；状态表中
    ``-1`` 的位置视为障碍。每个返回解都是 n×n 二维列表（1=填，-1=空）。
    输入非法或无解时返回空列表。
    """
    if not isinstance(board_size, int) or board_size < 1:
        return []
    if len(row_targets) != board_size or len(col_targets) != board_size:
        return []
    if any(not isinstance(value, int) or value < 0 for value in (*row_targets, *col_targets)):
        return []
    if sum(row_targets) != sum(col_targets):
        return []

    try:
        blocked_cells = _normalise_blocked(board_size, blocked)
    except (TypeError, ValueError):
        return []
    if any(
        len(position) != 2
        or not all(isinstance(value, int) for value in position)
        or not (0 <= position[0] < board_size and 0 <= position[1] < board_size)
        for position in blocked_cells
    ):
        return []

    available_by_row = [
        [col for col in range(board_size) if (row, col) not in blocked_cells]
        for row in range(board_size)
    ]
    if any(row_targets[row] > len(available_by_row[row]) for row in range(board_size)):
        return []
    if any(
        col_targets[col]
        > sum((row, col) not in blocked_cells for row in range(board_size))
        for col in range(board_size)
    ):
        return []

    row_patterns = [
        [frozenset(cols) for cols in combinations(available_by_row[row], row_targets[row])]
        for row in range(board_size)
    ]
    col_filled = [0] * board_size
    solutions = []
    chosen_rows = [frozenset() for _ in range(board_size)]
    row_order = sorted(range(board_size), key=lambda row: len(row_patterns[row]))

    def can_still_reach_targets(depth):
        remaining_rows = row_order[depth:]
        for col in range(board_size):
            if col_filled[col] > col_targets[col]:
                return False
            possible = sum((row, col) not in blocked_cells for row in remaining_rows)
            if col_filled[col] + possible < col_targets[col]:
                return False
        return True

    def search(depth):
        if depth == board_size:
            if col_filled == list(col_targets):
                solutions.append([
                    [FILLED if col in chosen_rows[row] else EMPTY for col in range(board_size)]
                    for row in range(board_size)
                ])
            return

        row = row_order[depth]
        for pattern in row_patterns[row]:
            if any(col_filled[col] >= col_targets[col] for col in pattern):
                continue
            chosen_rows[row] = pattern
            for col in pattern:
                col_filled[col] += 1
            if can_still_reach_targets(depth + 1):
                search(depth + 1)
            for col in pattern:
                col_filled[col] -= 1

    if can_still_reach_targets(0):
        search(0)
    return solutions

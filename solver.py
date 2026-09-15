def solve(board_size, row_targets, col_targets):
    """返回所有解。每个解是 board_size×board_size 的二维列表（1=填，0=空）。
    无解时返回空列表 []。不打印、不退出进程——GUI 需要的是数据。"""
    board = [[0] * board_size for _ in range(board_size)]
    solutions = []

    num = 0
    for i in row_targets:
        num += i
    for i in col_targets:
        num -= i
    if num != 0:
        return []

    fill_patterns=[[[] for _ in range(7)] for _ in range(7)]
    pattern_counts=[[0]*7 for _ in range(7)]
    for i in range(1,7):
        pattern_counts[i][0] = 1
        fill_patterns[i][0].append([-1]*i)
        pattern_counts[i][i] = 1
        fill_patterns[i][i].append([1]*i)
    for i in range(2,7):
        for j in range(1,i):
            pattern_counts[i][j] = pattern_counts[i-1][j-1] + pattern_counts[i-1][j]
            for former_fill_pattern_or_next_function in fill_patterns[i-1][j-1]:
                fill_patterns[i][j].append(former_fill_pattern_or_next_function + [1])
            for former_fill_pattern_or_next_function in fill_patterns[i-1][j]:
                fill_patterns[i][j].append(former_fill_pattern_or_next_function + [-1])

    stack_for_changed_positions = []
    def record_solution():
        # 必须深拷贝：board 是复用的，回溯会把格子改回 0
        solutions.append([row[:] for row in board])
    def try_row(index):
        nonlocal former_fill_pattern_or_next_function
        stack_for_changed_positions.append([])
        j = row_targets[index]
        for i in range(board_size):
            if board[index][i] == 0:
                stack_for_changed_positions[-1].append(i)
            if board[index][i] == 1:
                j -= 1
        i = len(stack_for_changed_positions[-1])
        for k in range(pattern_counts[i][j]):
            for l in range(i):
                board[index][stack_for_changed_positions[-1][l]] = fill_patterns[i][j][k][l]
            next_index = find_best_line()
            if next_index == None:
                record_solution()
                next_index = -1
            if next_index != -1:
                former_fill_pattern_or_next_function(next_index)
            for l in range(i):
                board[index][stack_for_changed_positions[-1][l]] = 0
        stack_for_changed_positions.pop()
    def try_col(index):
        nonlocal former_fill_pattern_or_next_function
        stack_for_changed_positions.append([])
        empty_remained_to_be_filled = col_targets[index]
        for i in range(board_size):
            if board[i][index] == 0:
                stack_for_changed_positions[-1].append(i)
            if board[i][index] == 1:
                empty_remained_to_be_filled -= 1
        i = len(stack_for_changed_positions[-1])
        for k in range(pattern_counts[i][empty_remained_to_be_filled]):
            for l in range(i):
                board[stack_for_changed_positions[-1][l]][index] = fill_patterns[i][empty_remained_to_be_filled][k][l]
            next_index = find_best_line()
            if next_index == None:
                record_solution()
                next_index = -1
            if next_index != -1:
                former_fill_pattern_or_next_function(next_index)
            for l in range(i):
                board[stack_for_changed_positions[-1][l]][index] = 0
        stack_for_changed_positions.pop()
        


    former_fill_pattern_or_next_function = try_row
    def find_best_line():
        nonlocal former_fill_pattern_or_next_function 
        min = 21
        t = None
        for i in range(board_size):
            empty_count = 0
            empty_remained_to_be_filled=row_targets[i]
            for j in range(board_size):
                if board[i][j] == 1:
                    empty_remained_to_be_filled -= 1
                if board[i][j] == 0:
                    empty_count += 1
            if empty_remained_to_be_filled < 0 or empty_remained_to_be_filled > empty_count:
                return -1
            if empty_count == 0:
                continue
            if pattern_counts[empty_count][empty_remained_to_be_filled] < min:
                min = pattern_counts[empty_count][empty_remained_to_be_filled]
                former_fill_pattern_or_next_function = try_row
                t = i
        for j in range(board_size):
            empty_count=0
            empty_remained_to_be_filled=col_targets[j]
            for i in range(board_size):
                if board[i][j] == 1:
                    empty_remained_to_be_filled -= 1
                if board[i][j] == 0:
                    empty_count += 1
            if empty_remained_to_be_filled < 0 or empty_remained_to_be_filled > empty_count:
                return -1
            if empty_count == 0:
                continue
            if pattern_counts[empty_count][empty_remained_to_be_filled] < min:
                min = pattern_counts[empty_count][empty_remained_to_be_filled]
                former_fill_pattern_or_next_function = try_col
                t = j
        return t



    t1 = find_best_line()
    if t1 is None or t1 == -1:
        return solutions
    former_fill_pattern_or_next_function(t1)
    return solutions







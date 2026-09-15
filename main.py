# -*- coding: utf-8 -*-
"""Endfield Calculator —— 数织谜题求解器的图形界面。

分工说明：
  solver.py 负责算，本文件负责界面。
  _build_board() 里的 grid 布局骨架来自本地 qwen3.5-9b（经人工修正两处错误：
  一行的 rowconfigure 写成了裸函数调用；行列按钮的命名贴反了）。
  状态管理与回调由人工编写——这正是小模型容易出错的部分。

solver.solve() 的返回约定（很重要，别记错）：
    返回 list[list[list[int]]]，每个解是 n×n 的二维列表。
        1  = 要填黑的格子
       -1  = 确定不填的格子
    （注意：是 -1 不是 0！0 只在搜索过程中出现，不会出现在返回的解里）
    无解时返回 []，不会打印也不会退出进程。
"""

import tkinter as tk

from solver import solve


class EndfieldGUI:
    def __init__(self, root):
        self.root = root
        self.n = 3
        self.row_values = [0] * self.n
        self.col_values = [0] * self.n
        self.solutions = []
        self.current = 0

        self._build_static_parts()
        self._build_board()

    # ============================================================ 界面搭建

    def _build_static_parts(self):
        """搭好外围：尺寸选择栏、棋盘占位区、按钮栏、状态栏。

        棋盘本身放在 _build_board() 里单独建，因为切换尺寸时要整个拆掉重建。
        """
        root = self.root
        root.title("Endfield Calculator")

        # ---- 顶部：棋盘尺寸选择 ----
        top = tk.Frame(root, pady=6)
        top.grid(row=0, column=0)

        tk.Label(top, text="棋盘大小：").pack(side="left")
        self.size_buttons = {}
        for size in (3, 4, 5, 6):
            # lambda 的默认参数 size=size 是关键：不写的话所有按钮都会
            # 捕获同一个变量，点哪个都变成最后一个值（经典闭包陷阱）。
            btn = tk.Button(top, text=str(size), width=3,
                            command=lambda size=size: self.set_size(size))
            btn.pack(side="left", padx=2)
            self.size_buttons[size] = btn

        # ---- 中部：棋盘占位区（内容可整体替换）----
        self.board_holder = tk.Frame(root)
        self.board_holder.grid(row=1, column=0)
        self.board_frame = None             # 棋盘本体还没建，见 _build_board()

        # ---- 底部：操作按钮 ----
        bar = tk.Frame(root, pady=6)
        bar.grid(row=2, column=0)

        tk.Button(bar, text="求解", width=8,
                  command=self.solve_it).pack(side="left", padx=3)
        tk.Button(bar, text="下一个解", width=8,
                  command=self.next_solution).pack(side="left", padx=3)
        tk.Button(bar, text="清空", width=8,
                  command=self.clear).pack(side="left", padx=3)

        # ---- 状态提示 ----
        self.status = tk.Label(root, text="设置每行每列的目标数，然后点「求解」")
        self.status.grid(row=3, column=0, pady=(0, 10))

    def _build_board(self):
        """(n+1)×(n+1) 的网格：左上角留空，第 0 行是列按钮，第 0 列是行按钮。

        grid 坐标对照：
            列按钮 → (row=0,     column=j+1)
            行按钮 → (row=i+1,   column=0)
            格子   → (row=i+1,   column=j+1)
        所以 row=0 那一排按钮控制的是【列】——它们的循环变量是 j。
        """
        n = self.n

        if self.board_frame is not None:
            self.board_frame.destroy()          # 换尺寸时拆掉旧的

        self.board_frame = tk.Frame(self.board_holder, padx=10, pady=10)
        self.board_frame.grid(row=0, column=0)
        frame = self.board_frame

        for k in range(n + 1):                  # 让窗口拉伸时格子跟着缩放
            frame.rowconfigure(k, weight=1)
            frame.columnconfigure(k, weight=1)

        # 左上角留空
        tk.Label(frame, width=3, height=1).grid(row=0, column=0, sticky="nsew")

        # 第 0 行：列目标按钮（控制第 j 列）
        self.col_buttons = []
        for j in range(n):
            btn = tk.Button(frame, width=3, height=1, text="0",
                            command=lambda j=j: self.bump_col(j))
            btn.grid(row=0, column=j + 1, sticky="nsew")
            self.col_buttons.append(btn)

        # 第 0 列：行目标按钮（控制第 i 行）
        self.row_buttons = []
        for i in range(n):
            btn = tk.Button(frame, width=3, height=1, text="0",
                            command=lambda i=i: self.bump_row(i))
            btn.grid(row=i + 1, column=0, sticky="nsew")
            self.row_buttons.append(btn)

        # 中间的棋盘格子
        self.cells = []
        for i in range(n):
            line = []
            for j in range(n):
                lbl = tk.Label(frame, width=3, height=1, bg="white",
                               relief="solid", borderwidth=1)
                lbl.grid(row=i + 1, column=j + 1, sticky="nsew")
                line.append(lbl)
            self.cells.append(line)

        self._paint_blank()

    def set_size(self, size):
        """切换棋盘尺寸：重置所有状态并重建棋盘区。"""
        if size == self.n and self.solutions:
            pass
        self.n = size
        self.row_values = [0] * size
        self.col_values = [0] * size
        self.solutions = []
        self.current = 0
        self._build_board()
        self.status.config(text=f"已切换到 {size}×{size}，设置目标数后点「求解」")

    # ============================================================ 交互

    def bump_col(self, j):
        """点击列按钮：0 → 1 → … → n → 0 循环。"""
        self.col_values[j] = (self.col_values[j] + 1) % (self.n + 1)
        self.col_buttons[j].config(text=str(self.col_values[j]))
        self._paint_blank()                     # 目标变了，旧的解就不再对应

    def bump_row(self, i):
        """点击行按钮：0 → 1 → … → n → 0 循环。"""
        self.row_values[i] = (self.row_values[i] + 1) % (self.n + 1)
        self.row_buttons[i].config(text=str(self.row_values[i]))
        self._paint_blank()

    # ============================================================ 求解与绘制

    def _paint_blank(self):
        for line in self.cells:
            for lbl in line:
                lbl.config(bg="white")

    def solve_it(self):
        self.solutions = solve(self.n, self.row_values, self.col_values)
        self.current = 0

        if not self.solutions:
            self._paint_blank()
            self.status.config(text="无解。检查行、列目标数是否矛盾（行和必须等于列和）")
            return

        self._paint_current()

    def next_solution(self):
        if not self.solutions:
            self.status.config(text="还没求解呢，先点「求解」")
            return
        self.current = (self.current + 1) % len(self.solutions)
        self._paint_current()

    def _paint_current(self):
        sol = self.solutions[self.current]
        for i in range(self.n):
            for j in range(self.n):
                # 关键：解里 1 = 填，-1 = 空。-1 在 Python 里是"真值"，
                # 写成 `if sol[i][j]` 会让整块棋盘都变黑——这是最容易踩的坑。
                color = "black" if sol[i][j] == 1 else "white"
                self.cells[i][j].config(bg=color)
        self.status.config(
            text=f"第 {self.current + 1} / {len(self.solutions)} 个解")

    def clear(self):
        self.row_values = [0] * self.n
        self.col_values = [0] * self.n
        self.solutions = []
        self.current = 0
        for i, btn in enumerate(self.row_buttons):
            btn.config(text="0")
        for j, btn in enumerate(self.col_buttons):
            btn.config(text="0")
        self._paint_blank()
        self.status.config(text="已清空")


def main():
    root = tk.Tk()
    EndfieldGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

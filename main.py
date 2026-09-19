# -*- coding: utf-8 -*-
"""Endfield Calculator：支持初始障碍的数织谜题求解器。"""

import tkinter as tk

from solver import solve


class EndfieldGUI:
    BG = "#11141b"
    PANEL = "#1a1f2a"
    PANEL_ALT = "#222938"
    GRID = "#3b4558"
    TEXT = "#f2f4f8"
    MUTED = "#98a2b3"
    ACCENT = "#ffb547"
    ACCENT_HOVER = "#ffc96b"
    FILLED = "#60d394"
    BLOCKED = "#586174"
    EMPTY = "#f3f5f8"
    DANGER = "#ff6b6b"

    def __init__(self, root):
        self.root = root
        self.n = 3
        self.row_values = [0] * self.n
        self.col_values = [0] * self.n
        self.blocked = set()
        self.solutions = []
        self.current = 0
        self._configure_window()
        self._build_static_parts()
        self._build_board()

    def _configure_window(self):
        self.root.title("Endfield Calculator · 障碍版")
        self.root.configure(bg=self.BG)
        self.root.minsize(580, 690)
        self.root.geometry("680x760")
        self.root.option_add("*Font", ("Microsoft YaHei UI", 10))
        self.root.bind("<Return>", lambda _event: self.solve_it())
        self.root.bind("<Control-r>", lambda _event: self.clear_all())

    def _build_static_parts(self):
        container = tk.Frame(self.root, bg=self.BG, padx=34, pady=28)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(3, weight=1)

        header = tk.Frame(container, bg=self.BG)
        header.grid(row=0, column=0, sticky="ew")
        tk.Label(header, text="ENDFIELD  /  CALCULATOR", bg=self.BG,
                 fg=self.ACCENT, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(header, text="数织部署规划器", bg=self.BG, fg=self.TEXT,
                 font=("Microsoft YaHei UI", 24, "bold")).pack(anchor="w", pady=(2, 3))
        tk.Label(header, text="设置行列目标，点击棋盘加入初始障碍，然后开始求解。",
                 bg=self.BG, fg=self.MUTED).pack(anchor="w")

        size_panel = tk.Frame(container, bg=self.PANEL, padx=16, pady=12)
        size_panel.grid(row=1, column=0, sticky="ew", pady=(22, 12))
        tk.Label(size_panel, text="棋盘尺寸", bg=self.PANEL, fg=self.TEXT,
                 font=("Microsoft YaHei UI", 10, "bold")).pack(side="left")
        self.size_buttons = {}
        for size in (3, 4, 5, 6):
            button = tk.Button(size_panel, text=f"{size} × {size}", bd=0, padx=12, pady=6,
                               command=lambda value=size: self.set_size(value), cursor="hand2")
            button.pack(side="left", padx=(10, 0))
            self.size_buttons[size] = button

        legend = tk.Frame(container, bg=self.BG)
        legend.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        self._legend_item(legend, self.BLOCKED, "初始障碍")
        self._legend_item(legend, self.FILLED, "部署位置")
        tk.Label(legend, text="目标数字：左键 +1 / 右键 -1", bg=self.BG,
                 fg=self.MUTED).pack(side="right")

        self.board_holder = tk.Frame(container, bg=self.PANEL, padx=22, pady=22)
        self.board_holder.grid(row=3, column=0, sticky="nsew")
        self.board_holder.rowconfigure(0, weight=1)
        self.board_holder.columnconfigure(0, weight=1)
        self.board_frame = None

        navigation = tk.Frame(container, bg=self.BG)
        navigation.grid(row=4, column=0, sticky="ew", pady=(14, 0))
        self._button(navigation, "‹ 上一个", self.previous_solution, secondary=True).pack(side="left")
        self.solution_label = tk.Label(navigation, text="尚未求解", bg=self.BG,
                                       fg=self.MUTED, width=18)
        self.solution_label.pack(side="left", padx=8)
        self._button(navigation, "下一个 ›", self.next_solution, secondary=True).pack(side="left")
        self._button(navigation, "清空全部", self.clear_all, secondary=True).pack(side="right")
        self._button(navigation, "开始求解", self.solve_it).pack(side="right", padx=(0, 10))

        self.status = tk.Label(container, text="准备就绪 · 点击格子可切换障碍",
                               bg=self.PANEL_ALT, fg=self.TEXT, anchor="w", padx=14, pady=10)
        self.status.grid(row=5, column=0, sticky="ew", pady=(14, 0))

    def _button(self, parent, text, command, secondary=False):
        bg = self.PANEL_ALT if secondary else self.ACCENT
        fg = self.TEXT if secondary else self.BG
        active = self.GRID if secondary else self.ACCENT_HOVER
        return tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                         activebackground=active, activeforeground=fg, bd=0,
                         padx=16, pady=9, cursor="hand2",
                         font=("Microsoft YaHei UI", 10, "bold"))

    def _legend_item(self, parent, color, text):
        tk.Label(parent, text="  ", bg=color, width=2).pack(side="left")
        tk.Label(parent, text=text, bg=self.BG, fg=self.MUTED).pack(side="left", padx=(5, 14))

    def _build_board(self):
        if self.board_frame is not None:
            self.board_frame.destroy()
        self.board_frame = tk.Frame(self.board_holder, bg=self.PANEL)
        self.board_frame.grid(row=0, column=0)
        for index in range(self.n + 1):
            self.board_frame.rowconfigure(index, weight=1, minsize=48)
            self.board_frame.columnconfigure(index, weight=1, minsize=48)

        tk.Label(self.board_frame, text="目标", bg=self.PANEL, fg=self.MUTED,
                 font=("Microsoft YaHei UI", 8)).grid(row=0, column=0)
        self.col_buttons = []
        for col in range(self.n):
            button = self._target_button(self.board_frame, lambda col=col: self.bump_col(col, 1))
            button.bind("<Button-3>", lambda _event, col=col: self.bump_col(col, -1))
            button.grid(row=0, column=col + 1, padx=3, pady=3, sticky="nsew")
            self.col_buttons.append(button)

        self.row_buttons = []
        for row in range(self.n):
            button = self._target_button(self.board_frame, lambda row=row: self.bump_row(row, 1))
            button.bind("<Button-3>", lambda _event, row=row: self.bump_row(row, -1))
            button.grid(row=row + 1, column=0, padx=3, pady=3, sticky="nsew")
            self.row_buttons.append(button)

        self.cells = []
        for row in range(self.n):
            line = []
            for col in range(self.n):
                cell = tk.Button(self.board_frame, text="", bg=self.EMPTY,
                                 activebackground="#dfe4eb", bd=0, relief="flat",
                                 cursor="hand2", font=("Segoe UI Symbol", 15, "bold"),
                                 command=lambda row=row, col=col: self.toggle_block(row, col))
                cell.grid(row=row + 1, column=col + 1, padx=3, pady=3, sticky="nsew")
                line.append(cell)
            self.cells.append(line)
        self._refresh_size_buttons()
        self._paint_editor()

    def _target_button(self, parent, command):
        return tk.Button(parent, text="0", command=command, bg=self.PANEL_ALT, fg=self.ACCENT,
                         activebackground=self.GRID, activeforeground=self.ACCENT,
                         bd=0, cursor="hand2", font=("Segoe UI", 12, "bold"))

    def _refresh_size_buttons(self):
        for size, button in self.size_buttons.items():
            selected = size == self.n
            button.config(bg=self.ACCENT if selected else self.PANEL_ALT,
                          fg=self.BG if selected else self.MUTED,
                          activebackground=self.ACCENT_HOVER if selected else self.GRID)

    def set_size(self, size):
        if size == self.n:
            return
        self.n = size
        self.row_values = [0] * size
        self.col_values = [0] * size
        self.blocked.clear()
        self._discard_solutions()
        self._build_board()
        self._set_status(f"已切换为 {size} × {size}，请设置目标与障碍")

    def bump_col(self, col, delta):
        self.col_values[col] = (self.col_values[col] + delta) % (self.n + 1)
        self.col_buttons[col].config(text=str(self.col_values[col]))
        self._return_to_editor("列目标已更新")
        return "break"

    def bump_row(self, row, delta):
        self.row_values[row] = (self.row_values[row] + delta) % (self.n + 1)
        self.row_buttons[row].config(text=str(self.row_values[row]))
        self._return_to_editor("行目标已更新")
        return "break"

    def toggle_block(self, row, col):
        position = (row, col)
        if position in self.blocked:
            self.blocked.remove(position)
            message = "已移除障碍"
        else:
            self.blocked.add(position)
            message = "已添加障碍"
        self._return_to_editor(f"{message} · 当前 {len(self.blocked)} 个")

    def _discard_solutions(self):
        self.solutions = []
        self.current = 0
        if hasattr(self, "solution_label"):
            self.solution_label.config(text="尚未求解", fg=self.MUTED)

    def _return_to_editor(self, message):
        self._discard_solutions()
        self._paint_editor()
        self._set_status(message)

    def _paint_editor(self):
        for row in range(self.n):
            for col in range(self.n):
                blocked = (row, col) in self.blocked
                self.cells[row][col].config(text="×" if blocked else "",
                                            bg=self.BLOCKED if blocked else self.EMPTY,
                                            fg=self.TEXT if blocked else self.BG,
                                            activebackground=self.BLOCKED if blocked else "#dfe4eb")

    def solve_it(self):
        self.solutions = solve(self.n, self.row_values, self.col_values, self.blocked)
        self.current = 0
        if not self.solutions:
            self._paint_editor()
            self.solution_label.config(text="无可行解", fg=self.DANGER)
            self._set_status("没有可行解，请检查目标数与障碍位置", error=True)
            return
        self._paint_current()

    def previous_solution(self):
        self._move_solution(-1)

    def next_solution(self):
        self._move_solution(1)

    def _move_solution(self, step):
        if not self.solutions:
            self._set_status("请先设置棋盘并开始求解")
            return
        self.current = (self.current + step) % len(self.solutions)
        self._paint_current()

    def _paint_current(self):
        solution = self.solutions[self.current]
        for row in range(self.n):
            for col in range(self.n):
                blocked = (row, col) in self.blocked
                filled = solution[row][col] == 1
                self.cells[row][col].config(text="×" if blocked else ("●" if filled else ""),
                                            bg=self.BLOCKED if blocked else (self.FILLED if filled else self.EMPTY),
                                            fg=self.BG if filled else self.TEXT)
        total = len(self.solutions)
        self.solution_label.config(text=f"方案 {self.current + 1} / {total}", fg=self.TEXT)
        self._set_status(f"求解完成 · 共找到 {total} 个可行方案")

    def clear_all(self):
        self.row_values = [0] * self.n
        self.col_values = [0] * self.n
        self.blocked.clear()
        self._discard_solutions()
        for button in self.row_buttons + self.col_buttons:
            button.config(text="0")
        self._paint_editor()
        self._set_status("已清空全部目标与障碍")

    def _set_status(self, message, error=False):
        self.status.config(text=message, fg=self.DANGER if error else self.TEXT)


def main():
    root = tk.Tk()
    EndfieldGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

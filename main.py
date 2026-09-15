import tkinter as tk
root = tk.Tk()
root.title("endfield calculator")
root.geometry("600x500")

title = tk.Label(root, text="Endfield Calculator")
title.pack()

board_size = tk.Label(root, text="棋盘大小：")
board_size.pack()
board_size_entry = tk.Entry(root)
board_size_entry.pack()




root.mainloop()










while True:
    try:
        board_size = int(input("Enter the board size (0-6): "))
        if 3 <= board_size <= 6:
            break
        else:
            print("Row and column must be between 3 and 6.")
    except ValueError:
        print("Invalid input. Please try again.")
    except KeyboardInterrupt:
        print("\nExiting the program.")
        sys.exit()

while True:
    try:
        row_targets = list(map(int, input("Enter the row values (space-separated): ").split()))
        col_targets = list(map(int, input("Enter the column values (space-separated): ").split()))
        if len(row_targets) == board_size and len(col_targets) == board_size and all(0 <= x <= board_size for x in row_targets + col_targets):
            break
        else:
            print(f"Please enter exactly {board_size} integers between 0 and {board_size}.")
    except ValueError:
        print("Invalid input. Please enter integers only.")
    except KeyboardInterrupt:
        print("\nExiting the program.")
        sys.exit()
这两段要如何改成gui版本的呢？其实我设想的是一个方块状的可视化棋盘，然后用户可以在每一行，每一列的边上通过点击一个按钮来调节所需的目标占格数。请教我其中涉及的基本gui设计语法知识，教我怎么编写这样一个gui

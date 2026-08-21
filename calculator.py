import sys
board=[[0]*6 for _ in range(6)]
ways = 0
while True:
    try:
        boardsize = int(input("Enter the board size (0-6): "))
        if 3 <= boardsize <= 6:
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
        rw = list(map(int, input("Enter the row values (space-separated): ").split()))
        cl = list(map(int, input("Enter the column values (space-separated): ").split()))
        if len(rw) == boardsize and len(cl) == boardsize and all(0 <= x <= boardsize for x in rw + cl):
            break
        else:
            print(f"Please enter exactly {boardsize} integers between 0 and {boardsize}.")
    except ValueError:
        print("Invalid input. Please enter integers only.")
    except KeyboardInterrupt:
        print("\nExiting the program.")
        sys.exit()

num = 0
for i in rw:
    num += i
for i in cl:
    num -= i
if num != 0:
    print("No solution found.")
    sys.exit()

C=[[[] for _ in range(7)] for _ in range(7)]
c=[[0]*7 for _ in range(7)]
for i in range(1,7):
    c[i][0] = 1
    C[i][0].append([-1]*i)
    c[i][i] = 1
    C[i][i].append([1]*i)
for i in range(2,7):
    for j in range(1,i):
        c[i][j] = c[i-1][j-1] + c[i-1][j]
        for x in C[i-1][j-1]:
            C[i][j].append(x + [1])
        for x in C[i-1][j]:
            C[i][j].append(x + [-1])

stack = []
def prt():
    global ways
    ways += 1
    for i in range(boardsize):
        for j in range(boardsize):
            if board[i][j] == 1:
                print("X", end=" ")
            else:
                print("O", end=" ")
        print()
    print()
def row(t):
    global x
    stack.append([])
    j = rw[t]
    for i in range(boardsize):
        if board[t][i] == 0:
            stack[-1].append(i)
        if board[t][i] == 1:
            j -= 1
    i = len(stack[-1])
    for k in range(c[i][j]):
        for l in range(i):
            board[t][stack[-1][l]] = C[i][j][k][l]
        t1 = find()
        if t1 == None:
            prt()
            t1 = -1
        if t1 != -1:
            x(t1)
        for l in range(i):
            board[t][stack[-1][l]] = 0
    stack.pop()
def col(t):
    global x
    stack.append([])
    j = cl[t]
    for i in range(boardsize):
        if board[i][t] == 0:
            stack[-1].append(i)
        if board[i][t] == 1:
            j -= 1
    i = len(stack[-1])
    for k in range(c[i][j]):
        for l in range(i):
            board[stack[-1][l]][t] = C[i][j][k][l]
        t1 = find()
        if t1 == None:
            prt()
            t1 = -1
        if t1 != -1:
            x(t1)
        for l in range(i):
            board[stack[-1][l]][t] = 0
    stack.pop()
    


x = row
def find():
    global x 
    min = 21
    t = None
    for i in range(boardsize):
        m = 0
        n=rw[i]
        for j in range(boardsize):
            if board[i][j] == 1:
                n -= 1
            if board[i][j] == 0:
                m += 1
        if n < 0 or n > m:
            return -1
        if m == 0:
            continue
        if c[m][n] < min:
            min = c[m][n]
            x = row
            t = i
    for j in range(boardsize):
        m=0
        n=cl[j]
        for i in range(boardsize):
            if board[i][j] == 1:
                n -= 1
            if board[i][j] == 0:
                m += 1
        if n < 0 or n > m:
            return -1
        if m == 0:
            continue
        if c[m][n] < min:
            min = c[m][n]
            x = col
            t = j
    return t



t1 = find()
x(t1)
if ways == 0:
    print("No solution found.")
else:
    print(f"Total ways to fill the board: {ways}")







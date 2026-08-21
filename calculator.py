board=[[0]*6 for _ in range(6)]



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
        break
rw = list(map(int, input("Enter the row values (space-separated): ").split()))
cl = list(map(int, input("Enter the column values (space-separated): ").split()))
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
    for i in range(boardsize):
        for j in range(boardsize):
            if board[i][j] == 1:
                print("X", end=" ")
            elif board[i][j] == -1:
                print("O", end=" ")
            else:
                print(".", end=" ")
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
        if len(stack) == boardsize * 2:
            prt()
            continue
        t1 = find()
        if t1 != -1:
            x(t1)
        for l in range(i):
            board[t][stack[-1][l]] = 0
    stack.pop()
def col(t):
    global x
    stack.append([])
    j = rw[t]
    for i in range(boardsize):
        if board[i][t] == 0:
            stack[-1].append(i)
        if board[i][t] == 1:
            j -= 1
    i = len(stack[-1])
    for k in range(c[i][j]):
        for l in range(i):
            board[stack[-1][l]][t] = C[i][j][k][l]
        if len(stack) == boardsize * 2:
            prt()
            continue
        t1 = find()
        if t1 != -1:
            x(t1)
        for l in range(i):
            board[stack[-1][l]][t] = 0
    stack.pop()
    


t = 0
min = 21
x = row
def find():
    global x
    for i in range(boardsize):
        m=0
        n=rw[i]
        for j in range(boardsize):
            if board[i][j] == 1:
                n -= 1
            if board[i][j] == 0:
                m += 1
        if n < 0 or n > m:
            return -1
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
        if c[m][n] < min:
            min = c[m][n]
            x = col
            t = j
    return t







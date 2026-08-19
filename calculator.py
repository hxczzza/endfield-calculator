board=[[0]*6 for _ in range(6)]

while True:
    try:
        boardsize = int(input("Enter the board size (0-6): "))
        if 0 <= boardsize <= 6:
            break
        else:
            print("Row and column must be between 0 and 6.")
    except ValueError:
        print("Invalid input. Please try again.")
    except KeyboardInterrupt:
        print("\nExiting the program.")
        break
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




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



def main():
    board = [[0] * 4 for _ in range(4)]

    for i in range(4):
        line = list(map(int, input().split()))
        board[i] = line
    move = int(input())

    if move == 0:
        board = moveLeft(board)
    if move == 1:
        board = moveUp(board)
    if move == 2:
        board = moveRight(board)
    if move == 3:
        board = moveDown(board)

    display(board)


def moveLeft(board):
    # initial shift
    shiftLeft(board)

    # merge cells
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j + 1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j + 1] = 0
                j = 0

    # final shift
    shiftLeft(board)
    return board


def moveUp(board):
    board = rotateLeft(board)
    board = moveLeft(board)
    board = rotateRight(board)
    return board


def moveRight(board):
    # initial shift
    shiftRight(board)

    # merge cells
    for i in range(4):
        for j in range(3, 0, -1):
            if board[i][j] == board[i][j - 1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j - 1] = 0
                j = 0

    # final shift
    shiftRight(board)

    return board


def moveDown(board):
    board = rotateLeft(board)
    board = moveLeft(board)
    shiftRight(board)
    board = rotateRight(board)
    return board


def shiftLeft(board):
    # remove 0's in between numbers
    for i in range(4):
        nums, count = [], 0
        for j in range(4):
            if board[i][j] != 0:
                nums.append(board[i][j])
                count += 1
        board[i] = nums
        board[i].extend([0] * (4 - count))


def shiftRight(board):
    # remove 0's in between numbers
    for i in range(4):
        nums, count = [], 0
        for j in range(4):
            if board[i][j] != 0:
                nums.append(board[i][j])
                count += 1
        board[i] = [0] * (4 - count)
        board[i].extend(nums)


def rotateLeft(board):
    # 90 degree counter clockwise rotation
    b = [[board[j][i] for j in range(4)] for i in range(3, -1, -1)]
    return b


def rotateRight(board):
    # 270 degree counter clockwise rotation
    b = rotateLeft(board)
    b = rotateLeft(b)
    return rotateLeft(b)


def display(board):
    for i in range(4):
        for j in range(4):
            print(board[i][j], end=' ')
        print()


if __name__ == "__main__":
    main()

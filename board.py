import random


def check_position(row, col, num, board):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    row_block = 3 * (row // 3)
    col_block = 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[row_block + i][col_block + j] == num:
                return False
    return True


def set_random_positions(board):
    for _ in range(10):
        while True:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            num = random.randint(1, 9)
            if check_position(row, col, num, board):
                board[row][col] = num
                break


def board_solution(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == '.':
                for num in range(1, 10):
                    if check_position(row, col, num, board):
                        board[row][col] = num
                        if board_solution(board):
                            return True
                        board[row][col] = '.'
                return False
    return True


def sudoku_board():
    board = [['.' for _ in range(9)] for _ in range(9)]
    set_random_positions(board)
    board_solution(board)
    return board

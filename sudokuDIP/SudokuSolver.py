class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid

    def isInCol(self, col, num):
        for row in range(0,9):
            if self.grid[row][col] == num:
                return True
        return False

    def isInRow(self, row, num):
        for col in range(0, 9):
            if self.grid[row][col] == num:
                return True
        return False

    def isInBox(self, start_row, start_col, num):
        for row in range(0,3):
            for col in range(0,3):
                if self.grid[row+start_row][col+start_col] == num:
                    return True
        return False

    def haveEmpty(self):
        for row in range(0,9):
            for col in range(0,9):
                if self.grid[row][col] == 0:
                    return True
        return False

    def isValidBox(self, row, col, num):
        return not self.isInRow(row, num) and not self.isInCol(col, num) and not self.isInBox(row-row%3, col-col%3, num)

    def solveSudoku(self, row, col):
        if row == 8 and col == 9:
            return True
        
        if col == 9:
            row += 1
            col = 0
        
        if self.grid[row][col] > 0:
            return self.solveSudoku(row, col+1)
        for num in range(1, 10):
            if self.isValidBox(row, col, num):
                self.grid[row][col] = num
                if self.solveSudoku(row, col+1):
                    return True
            self.grid[row][col] = 0
        return False
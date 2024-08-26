import os
import time
import psutil
import random
import math
from BFS import BFS
from SA import SA

class Sudoku:
    def __init__(self, N, K):
        self.N = N
        self.K = K
 
        # Compute square root of N
        SRNd = math.sqrt(N)
        self.SRN = int(SRNd)
        self.mat = [[0 for _ in range(N)] for _ in range(N)]
     
    def fillValues(self):
        # Fill the diagonal of SRN x SRN matrices
        self.fillDiagonal()
 
        # Fill remaining blocks
        self.fillRemaining(0, self.SRN)
 
        # Remove Randomly K digits to make game
        self.removeKDigits()
     
    def fillDiagonal(self):
        for i in range(0, self.N, self.SRN):
            self.fillBox(i, i)
     
    def unUsedInBox(self, rowStart, colStart, num):
        for i in range(self.SRN):
            for j in range(self.SRN):
                if self.mat[rowStart + i][colStart + j] == num:
                    return False
        return True
     
    def fillBox(self, row, col):
        num = 0
        for i in range(self.SRN):
            for j in range(self.SRN):
                while True:
                    num = self.randomGenerator(self.N)
                    if self.unUsedInBox(row, col, num):
                        break
                self.mat[row + i][col + j] = num
     
    def randomGenerator(self, num):
        return math.floor(random.random() * num + 1)
     
    def checkIfSafe(self, i, j, num):
        return (self.unUsedInRow(i, num) and self.unUsedInCol(j, num) and self.unUsedInBox(i - i % self.SRN, j - j % self.SRN, num))
     
    def unUsedInRow(self, i, num):
        for j in range(self.N):
            if self.mat[i][j] == num:
                return False
        return True
     
    def unUsedInCol(self, j, num):
        for i in range(self.N):
            if self.mat[i][j] == num:
                return False
        return True
     
    
    def fillRemaining(self, i, j):
        # Check if we have reached the end of the matrix
        if i == self.N - 1 and j == self.N:
            return True
     
        # Move to the next row if we have reached the end of the current row
        if j == self.N:
            i += 1
            j = 0
     
        # Skip cells that are already filled
        if self.mat[i][j] != 0:
            return self.fillRemaining(i, j + 1)
     
        # Try filling the current cell with a valid value
        for num in range(1, self.N + 1):
            if self.checkIfSafe(i, j, num):
                self.mat[i][j] = num
                if self.fillRemaining(i, j + 1):
                    return True
                self.mat[i][j] = 0
         
        # No valid value was found, so backtrack
        return False
 
    def removeKDigits(self):
        count = self.K
 
        while (count != 0):
            i = self.randomGenerator(self.N) - 1
            j = self.randomGenerator(self.N) - 1
            if (self.mat[i][j] != 0):
                count -= 1
                self.mat[i][j] = 0
     
        return
 
    def printSudoku(self):
        for i in range(self.N):
            for j in range(self.N):
                print(self.mat[i][j], end=" ")
            print()

def create_sudoku_level(N, K):
    sudoku = Sudoku(N, K)
    sudoku.fillValues()
    return sudoku

def print_board(board):
    border = "------+-------+------"
    rows = [board[i] for i in range(9)]
    for i, row in enumerate(rows):
        if i % 3 == 0:
            print(border)
        three = [row[i : i + 3] for i in range(0, 9, 3)]
        print(" | ".join(" ".join(str(x or "0") for x in one) for one in three))
    print(border)

def main():
    user_level = input("Please enter the difficulty (easy, medium, hard, evil): ")
    N = 9
    K = 0
    # Matrix 9 x 9, which has (81 - K) clues.
    if user_level == "easy":
        K = 45
    elif user_level == "medium":
        K = 49
    elif user_level == "hard":
        K = 53
    elif user_level == "evil":
        K = 64
    else:
        print("Input must be \"easy\", \"medium\", \"hard\", and \"evil\"")
        return
    
    user_algo = input("Please enter the type of algorithm (BFS, SA): ")
    if user_algo != "BFS" and user_algo != "SA":
        print("The algorithm must be BFS (Breadth-first Search) or SA (Simulated Annealing)!")
        return

    board = create_sudoku_level(N, K)
    print("=================================================================================")
    print("Initial State:")
    print_board(board.mat)

    process = psutil.Process(os.getpid())
    start_time = time.time()
    if user_algo == "BFS":
        path, count_calls = BFS(board.mat)
    if user_algo == "SA":
        board_1D = []
        for i in range(9):
            for j in range(9):
                board_1D.append(board.mat[i][j])
        result = SA(board_1D)
    end_time = time.time()
    
    memory_usage = round(process.memory_info().rss / (1024 * 1024), 2)
    elapsed_time = end_time - start_time

    if user_algo == "BFS":
        if path:
            for i, node in enumerate(path):
                if i == K:
                    final = node.state
                    print("Final:")
                    print_board(final)
                    break
            print("Calculation done!!!")
            print(f"Count calls: {count_calls[0]}")
            print(f"Elapsed time: {elapsed_time} seconds")
            print(f"Memory used: {memory_usage} MB")
        else:
            print("Không tìm thấy lời giải cho bảng Sudoku này.")
            return
    if user_algo == "SA":
        if result.all():
            border = "------+-------+------"
            rows = [result[i : i + 9] for i in range(0, 81, 9)]
            for i, row in enumerate(rows):
                if i % 3 == 0:
                    print(border)
                three = [row[i : i + 3] for i in range(0, 9, 3)]
                print(" | ".join(" ".join(str(x or "_") for x in one) for one in three))
            print(border)
            print("Calculation done!!!")
            print(f"Elapsed time: {elapsed_time} seconds")
            print(f"Memory used: {memory_usage} MB")
        else:
            print("Không tìm thấy lời giải cho bảng Sudoku này.")
            return

    # Write output:
    if not os.path.exists(os.path.join('./Output', user_algo)):
        os.makedirs(os.path.join('./Output', user_algo))
    with open(os.path.join('./Output', user_algo, 'output.txt'), 'w') as f:
        f.write(f"{user_level.title()} Mode + {user_algo} Algorithm:\n")
        f.write(f"===============================\n")
        f.write(f"Initial State:\n")
        border = "------+-------+------"
        rows = [board.mat[i] for i in range(9)]
        for i, row in enumerate(rows):
            if i % 3 == 0:
                f.write(border)
                f.write('\n')
            three = [row[i : i + 3] for i in range(0, 9, 3)]
            f.write(" | ".join(" ".join(str(x or "0") for x in one) for one in three))
            f.write('\n')
        f.write(border)
        f.write('\n')

        if user_algo == "BFS":
            f.write("Final State:\n")
            border = "------+-------+------"
            rows = [final[i] for i in range(9)]
            for i, row in enumerate(rows):
                if i % 3 == 0:
                    f.write(border)
                    f.write('\n')
                three = [row[i : i + 3] for i in range(0, 9, 3)]
                f.write(" | ".join(" ".join(str(x or "0") for x in one) for one in three))
                f.write('\n')
            f.write(border)
            f.write('\n')
            f.write(f"Count calls: {count_calls[0]}\n")
            f.write(f"Elapsed time: {elapsed_time} seconds\n")
            f.write(f"Memory used: {memory_usage} MB\n")
        if user_algo == "SA":
            f.write("Final State:\n")
            border = "------+-------+------"
            rows = [result[i : i + 9] for i in range(0, 81, 9)]
            for i, row in enumerate(rows):
                if i % 3 == 0:
                    f.write(border)
                    f.write('\n')
                three = [row[i : i + 3] for i in range(0, 9, 3)]
                f.write(" | ".join(" ".join(str(x or "_") for x in one) for one in three))
                f.write('\n')
            f.write(border)
            f.write('\n')
            f.write(f"Elapsed time: {elapsed_time} seconds\n")
            f.write(f"Memory used: {memory_usage} MB\n")        
    print('=================================================================================')
    print('File write operation successful.')
    print("Task completed successfully.")

if __name__ == "__main__":
    main()
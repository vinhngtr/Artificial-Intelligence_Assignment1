from fakedata import  TESTCASE
from algorithm_A import SearchPuzzle
import time
import matplotlib.pyplot as plt

class PipesPuzzle:
    def __init__(self):
        self.init_state = None
        self.level = None
        self.create_puzzle()
        self.path = []
        self.dataForPlot = []
    def create_puzzle(self):
        print("Lua chon testcase:")
        print("Test 1 to 3: choose one testcase")
        print("Test 4 to 5: choose one testcase")
        self.level = int(input())
        if self.level > 5:
            quit()
        testcase = TESTCASE[f"level{self.level}"]
        self.init_state = testcase
    def solve(self, solve_choice):
        solver = SearchPuzzle()
        startTime = time.time()
        print("Doi vai giay!!!")
        if solve_choice == "1":
            temp = solver.solve_Astar(self.init_state)
            self.dataForPlot = temp[0]
            self.path = temp[1]
        else:
            print("Chon phim phu hop voi lua chon giai thuat!")
            exit(1)
        executeTime = time.time() - startTime
        print("Tong thoi gian thuc hien tim kiem: ", str(round(executeTime, 4)))
    def simulatePlot(self):
        plt.bar(*zip(*self.dataForPlot.items()))
        plt.xlabel('Tong so buoc tim kiem')
        plt.ylabel('Tong so tim kiem trong moi buoc')
        plt.title('Thong ke')
        plt.show()       
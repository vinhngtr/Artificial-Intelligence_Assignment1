import copy
import random
import numpy as np
from simanneal import Annealer

def coord(row, col):
    return row*9+col

def block_indices(block_num):
    first_row = (block_num // 3) * 3
    first_col = (block_num % 3) * 3
    indices = [coord(first_row + i, first_col + j) for i in range(3) for j in range(3)]
    return indices

def initial_solution(problem):
    sol = problem.copy()
    for block in range(9):
        indices = block_indices(block)
        block = problem[indices]
        zeros = [i for i in indices if problem[i] == 0]
        toFill = [i for i in range(1, 10) if i not in block]
        random.shuffle(toFill)
        for idx, val in zip(zeros, toFill):
            sol[idx] = val
    return sol

class Sudoku(Annealer):
    def __init__(self, problem):
        self.problem = problem
        state = initial_solution(problem)
        super().__init__(state)
    def move(self):
        block = random.randrange(9)
        indices = []
        for i in block_indices(block):
            if self.problem[i] == 0:
                indices.append(i)
        m, n = random.sample(indices, 2)
        self.state[m], self.state[n] = self.state[n], self.state[m]
    def energy(self):
        col_sc = lambda n: -len(set(self.state[coord(i, n)] for i in range(9)))
        row_sc = lambda n: -len(set(self.state[coord(n, i)] for i in range(9)))
        final_score = 0
        for n in range(9):
            total_score = col_sc(n) + row_sc(n)
            final_score += total_score
        if final_score == -162:
            self.user_exit = True
        return final_score

def SA(board):
    problem = np.array(board)
    sudoku = Sudoku(problem)
    sudoku.copy_strategy = "method"
    sudoku.Tmax = 0.5
    sudoku.Tmin = 0.05
    sudoku.steps = 100000
    sudoku.updates = 100
    state, e = sudoku.anneal()
    print("\n")
    print("E=%f (expect -162)" % e)
    return state

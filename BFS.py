from collections import deque

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

def is_valid(board, row, col, num):
    # Kiểm tra xem giá trị num có hợp lệ không trong hàng và cột
    for i in range(9):
        if board[row][i] == num and i != col:
            return False
        if board[i][col] == num and i != row:
            return False
    
    # Kiểm tra xem giá trị num có hợp lệ không trong ô 3x3
    start_row = row - (row % 3)
    start_col = col - (col % 3)

    for i in range(3):
        for j in range(3):
            if num == board[start_row + i][start_col + j] and start_row + i != row and start_col + j != col:
                return False
    return True

def get_neighbors(node, count_calls):
    neighbors = []
    board = node.state
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    count_calls[0] += 1  # Tăng biến đếm số lần gọi hàm
                    if is_valid(board, i, j, num):
                        new_board = [row[:] for row in board]
                        new_board[i][j] = num
                        neighbors.append(Node(new_board, node))
                return neighbors

def is_goal_state(board):
    # Hàm kiểm tra xem bảng Sudoku đã đầy đủ và hợp lệ chưa
    for row in board:
        if 0 in row:
            return False
    return True

def BFS(board):
    root = Node(board)
    queue = deque([root])
    visited = set()
    visited.add(tuple(map(tuple, board)))
    end_state = None
    count_calls = [0]  # Biến đếm số lần gọi hàm
    while queue:
        node = queue.popleft()
        if is_goal_state(node.state):  # Kiểm tra xem trạng thái hiện tại có phải là trạng thái cuối không
            end_state = node
            break
        neighbors = get_neighbors(node, count_calls)
        if neighbors is not None:
            for neighbor in neighbors:
                neighbor_state = tuple(map(tuple, neighbor.state))
                if neighbor_state not in visited:
                    visited.add(neighbor_state)
                    queue.append(neighbor)
    if end_state is None:
        return [], count_calls
    
    # Truy vết từ trạng thái cuối về trạng thái ban đầu
    path = []
    while end_state is not None:
        path.append(end_state)
        end_state = end_state.parent
    path.reverse()
    return path, count_calls
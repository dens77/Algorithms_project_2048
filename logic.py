import random
import heapq

def start_game():
    mat = []
    for i in range(4):
        mat.append([0] * 4)
    add_new_2(mat)
    add_new_2(mat)  
    return mat

def add_new_2(mat):
    r = random.randint(0, 3)
    c = random.randint(0, 3)
    while mat[r][c] != 0:
        r = random.randint(0, 3)
        c = random.randint(0, 3)
    mat[r][c] = 2 if random.random() < 0.9 else 4

def search_for_2048(mat, target=2048):
    rows, cols = len(mat), len(mat[0])
    visited = [[False] * cols for _ in range(rows)]

    def dfs(i, j):
        if i < 0 or j < 0 or i >= rows or j >= cols or visited[i][j]:
            return False
        visited[i][j] = True
        if mat[i][j] == target:
            return True
        return dfs(i + 1, j) or dfs(i - 1, j) or dfs(i, j + 1) or dfs(i, j - 1)

    for i in range(rows):
        for j in range(cols):
            if dfs(i, j):
                return 'WON'
    return 'GAME NOT OVER' if any(0 in row for row in mat) else 'LOST'

def compress_with_priority(mat):
    changed = False
    new_mat = []
    for i in range(4):
        new_mat.append([0] * 4)
    for i in range(4):
        pq = []
        for j in range(4):
            if mat[i][j] != 0:
                heapq.heappush(pq, (j, mat[i][j])) 

        pos = 0
        while pq:
            _, value = heapq.heappop(pq)
            new_mat[i][pos] = value
            if pos != _:
                changed = True
            pos += 1
    return new_mat, changed

def merge_with_priority(mat):
    changed = False
    for i in range(4):
        pq = []
        for j in range(4):
            if mat[i][j] != 0:
                heapq.heappush(pq, (j, mat[i][j]))

        new_row = [0] * 4
        pos = 0
        while pq:
            _, value = heapq.heappop(pq)
            if pos < 3 and new_row[pos] == value: 
                new_row[pos] *= 2
                changed = True
            else:
                if new_row[pos] != 0:  
                    pos += 1
                new_row[pos] = value
        mat[i] = new_row
    return mat, changed

def reverse(mat):
    new_mat = []
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[i][3 - j])
    return new_mat

def transpose(mat):
    new_mat = []
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[j][i])
    return new_mat

def move_left(grid):
    new_grid, changed1 = compress_with_priority(grid)
    new_grid, changed2 = merge_with_priority(new_grid)
    changed = changed1 or changed2
    new_grid, _ = compress_with_priority(new_grid)
    return new_grid, changed

def move_right(grid):
    reversed_grid = reverse(grid)
    new_grid, changed = move_left(reversed_grid)
    new_grid = reverse(new_grid)
    return new_grid, changed

def move_up(grid):
    transposed_grid = transpose(grid)
    new_grid, changed = move_left(transposed_grid)
    new_grid = transpose(new_grid)
    return new_grid, changed

def move_down(grid):
    transposed_grid = transpose(grid)
    new_grid, changed = move_right(transposed_grid)
    new_grid = transpose(new_grid)
    return new_grid, changed

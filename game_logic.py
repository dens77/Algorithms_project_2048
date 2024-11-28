import random
from collections import defaultdict, deque
import heapq

def start_game():
    mat = [[0] * 4 for _ in range(4)]
    add_new_2(mat)
    add_new_2(mat)
    return mat

def add_new_2(mat):
    r, c = random.randint(0, 3), random.randint(0, 3)
    while mat[r][c] != 0:
        r, c = random.randint(0, 3), random.randint(0, 3)
    mat[r][c] = 2 if random.random() < 0.9 else 4

def board_to_graph(mat):
    rows, cols = len(mat), len(mat[0])
    graph = defaultdict(list)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for i in range(rows):
        for j in range(cols):
            for dx, dy in directions:
                x, y = i + dx, j + dy
                if 0 <= x < rows and 0 <= y < cols:
                    graph[(i, j)].append((x, y))
    return graph

def has_valid_moves(mat, graph):
    for node, neighbors in graph.items():
        i, j = node
        for x, y in neighbors:
            if mat[x][y] == mat[i][j] or mat[x][y] == 0:
                return "GAME NOT OVER"
    return "LOST"

def bfs_search_value(mat, graph, target=2048):
    visited = set()
    queue = deque([(i, j) for i in range(4) for j in range(4)])

    while queue:
        i, j = queue.popleft()
        if (i, j) in visited:
            continue
        visited.add((i, j))

        if mat[i][j] == target:
            return "WON"

        for x, y in graph[(i, j)]:
            if (x, y) not in visited:
                queue.append((x, y))

    return "CONTINUE"

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
            idx, value = heapq.heappop(pq)
            new_mat[i][pos] = value
            if pos != idx:
                changed = True
            pos += 1
    return new_mat, changed

def merge_with_priority(mat):
    changed = False
    score = 0  
    for i in range(4):
        pq = []
        for j in range(4):
            if mat[i][j] != 0:
                heapq.heappush(pq, (j, mat[i][j]))

        new_row = [0] * 4
        pos = 0
        while pq:
            idx, value = heapq.heappop(pq)
            if pos < 3 and new_row[pos] == value: 
                new_row[pos] *= 2
                score += new_row[pos] 
                changed = True
            else:
                if new_row[pos] != 0:  
                    pos += 1
                new_row[pos] = value
        mat[i] = new_row
    return mat, changed, score

def reverse(mat):
    return [row[::-1] for row in mat]

def transpose(mat):
    return [list(row) for row in zip(*mat)]

def move_left(mat):
    mat, changed1 = compress_with_priority(mat)
    mat, changed2, score = merge_with_priority(mat)
    mat, _ = compress_with_priority(mat)
    return mat, changed1 or changed2, score

def move_right(mat):
    mat = reverse(mat)
    mat, changed, score = move_left(mat)
    mat = reverse(mat)
    return mat, changed, score

def move_up(mat):
    mat = transpose(mat)
    mat, changed, score = move_left(mat)
    mat = transpose(mat)
    return mat, changed, score

def move_down(mat):
    mat = transpose(mat)
    mat, changed, score = move_right(mat)
    mat = transpose(mat)
    return mat, changed, score

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key_item = arr[i]
        j = i - 1
        while j >= 0 and arr[j] < key_item:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item

def create_custom_board(values):
    if len(values) != 4 or any(len(row) != 4 for row in values):
        raise ValueError("The board must be a 4x4 list of integers.")
    for row in values:
        if any(not isinstance(cell, int) or cell < 0 for cell in row):
            raise ValueError("All tiles must be non-negative integers.")
    return [row[:] for row in values]

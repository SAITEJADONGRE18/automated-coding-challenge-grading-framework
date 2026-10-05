from collections import deque

def shortest_path_grid(grid: list[list[int]]) -> int:
    if not grid or not grid[0]:
        return -1
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] != 0 or grid[rows - 1][cols - 1] != 0:
        return -1
    distances = [[-1] * cols for _ in range(rows)]
    distances[0][0] = 1
    queue = deque([(0, 0)])
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    while queue:
        r, c = queue.popleft()
        if (r, c) == (rows - 1, cols - 1):
            return distances[r][c]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and grid[nr][nc] == 0 and distances[nr][nc] == -1):
                distances[nr][nc] = distances[r][c] + 1
                queue.append((nr, nc))
    return -1

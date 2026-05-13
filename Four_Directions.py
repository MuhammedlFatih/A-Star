import heapq

# Basit bir 5x5 grid (0 = boş, 1 = engel)
grid = [
    [0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (4, 4)

# Heuristik fonksiyon (Manhattan mesafesi)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Komşu bulma fonksiyonu (4 yönlü)
def get_neighbors(r, c):
    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == 0:
            yield (nr, nc)

# A* algoritması
def astar(start, goal):
    pq = [(0, start)]  # (f_score, hücre)
    came_from = {start: None}
    g = {start: 0}

    while pq:
        _, current = heapq.heappop(pq)

        if current == goal:
            break

        for neighbor in get_neighbors(*current):
            tentative_g = g[current] + 1
            if neighbor not in g or tentative_g < g[neighbor]:
                g[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(pq, (f, neighbor))
                came_from[neighbor] = current

    # Geriye doğru yolu oluştur
    path = []
    node = goal
    while node and node in came_from:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path

path = astar(start, goal)
print("Path:", path)

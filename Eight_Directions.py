# astar8.py
import heapq
import math

# Basit grid: 0 = boş, 1 = engel
GRID = [
    [0,0,0,0,0,0],
    [0,1,1,0,1,0],
    [0,0,0,0,1,0],
    [0,1,0,0,0,0],
    [0,0,0,1,0,0],
    [0,0,0,0,0,0],
]

ROWS = len(GRID)
COLS = len(GRID[0])

START = (0, 0)
GOAL  = (5, 5)

# Diagonal harekete izin verirken "corner cutting" (köşe kesme) engelleme seçeneği
ALLOW_DIAGONAL_CORNER_CUT = False

# Hareket vektörleri ve maliyetleri (8 yön)
# (dr, dc, cost)
SQRT2 = math.sqrt(2)
MOVES = [
    ( 1,  0, 1.0),  # down
    (-1,  0, 1.0),  # up
    ( 0,  1, 1.0),  # right
    ( 0, -1, 1.0),  # left
    ( 1,  1, SQRT2),# down-right (diag)
    ( 1, -1, SQRT2),# down-left
    (-1,  1, SQRT2),# up-right
    (-1, -1, SQRT2) # up-left
]

# Octile heuristic: uygun ve admissible (8-connected grid with diagonal cost sqrt(2))
def heuristic(a, b):
    (x1, y1), (x2, y2) = a, b
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    # Octile: h = (dx + dy) + (sqrt(2)-2) * min(dx,dy)
    return (dx + dy) + (SQRT2 - 2) * min(dx, dy)

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def is_passable(r, c):
    return in_bounds(r, c) and GRID[r][c] == 0

def get_neighbors(node):
    r, c = node
    for dr, dc, cost in MOVES:
        nr, nc = r + dr, c + dc
        # temel geçilebilirlik
        if not in_bounds(nr, nc):
            continue
        if GRID[nr][nc] == 1:
            continue
        # köşe kesmeyi engelle (örn. sağ-üst diag yapılırken sağ veya üstten en az biri engel ise izin verme)
        if not ALLOW_DIAGONAL_CORNER_CUT and abs(dr) == 1 and abs(dc) == 1:
            # iki ortogonal komşuyu kontrol et
            if GRID[r + dr][c] == 1 or GRID[r][c + dc] == 1:
                continue
        yield (nr, nc, cost)

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from and came_from[current] is not None:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def astar(start, goal):
    open_heap = []  # (f_score, counter, node)
    counter = 0
    g_score = {start: 0.0}
    f_score = {start: heuristic(start, goal)}
    came_from = {start: None}
    heapq.heappush(open_heap, (f_score[start], counter, start))
    closed_set = set()

    while open_heap:
        current_f, _, current = heapq.heappop(open_heap)

        # Skip stale entries (if we've already visited cheaper)
        if current in closed_set:
            continue

        if current == goal:
            return reconstruct_path(came_from, current)

        closed_set.add(current)

        for nr, nc, move_cost in get_neighbors(current):
            neighbor = (nr, nc)
            tentative_g = g_score[current] + move_cost
            if neighbor in closed_set and tentative_g >= g_score.get(neighbor, float('inf')):
                continue
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                f_score[neighbor] = f
                counter += 1
                heapq.heappush(open_heap, (f, counter, neighbor))

    return None  # yol bulunamadı

# Basit terminal görselleştirme
def print_grid_with_path(path):
    out = [row[:] for row in GRID]
    if path:
        for (r,c) in path:
            if (r,c) != START and (r,c) != GOAL:
                out[r][c] = 2
    for r in range(ROWS):
        line = ''
        for c in range(COLS):
            if (r,c) == START:
                line += 'S '
            elif (r,c) == GOAL:
                line += 'G '
            elif out[r][c] == 1:
                line += '# '
            elif out[r][c] == 2:
                line += 'o '
            else:
                line += '. '
        print(line)
    print()

if __name__ == "__main__":
    path = astar(START, GOAL)
    if path:
        print("Path found:", path)
    else:
        print("No path found.")
    print_grid_with_path(path)

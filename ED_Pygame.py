import pygame
import time
import heapq
from collections import deque
import math

# --- Ayarlar ---
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 30, 30
CELL = WIDTH // COLS

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding with A-star")

# --- Renkler ---
WHITE = (255,255,255)      # Düz zemin
YELLOW = (255,255,0)       # Orta zemin
BROWN = (139,69,19)        # Zor zemin
BLACK = (0,0,0)            # Engel
BLUE = (0,255,255)         # BFS yol
ORANGE = (255,165,0)       # Dijkstra yol
PURPLE = (160,32,240)      # A* yol
GREEN = (0,255,0)          # Başlangıç
RED = (255,0,0)            # Bitiş

# --- Zemin maliyetleri ---
terrain_cost = {0:1, 1:2, 2:3, 3:float('inf')}  # 0=düz, 1=orta, 2=zor, 3=engel

# --- Grid ---
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

start = (0,0)
goal = (ROWS-1,COLS-1)

ALLOW_DIAGONAL_CORNER_CUT = False

# --- Fonksiyonlar ---
def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            terrain = grid[r][c]
            if terrain==0:
                color=WHITE
            elif terrain==1:
                color=YELLOW
            elif terrain==2:
                color=BROWN
            else:
                color=BLACK
            pygame.draw.rect(win,color,(c*CELL,r*CELL,CELL-1,CELL-1))
    pygame.draw.rect(win,GREEN,(start[1]*CELL,start[0]*CELL,CELL-1,CELL-1))
    pygame.draw.rect(win,RED,(goal[1]*CELL,goal[0]*CELL,CELL-1,CELL-1))
    pygame.display.update()

def draw_path(path,color):
    for r,c in path:
        pygame.draw.rect(win,color,(c*CELL,r*CELL,CELL-1,CELL-1))
        pygame.display.update()
        time.sleep(0.01)

SQRT2 = math.sqrt(2)
def get_neighbors(r,c):
    moves = [
        ( 1,  0, 1.0), (-1,  0, 1.0), ( 0,  1, 1.0), ( 0, -1, 1.0),
        ( 1,  1, SQRT2),( 1, -1, SQRT2),(-1,  1, SQRT2),(-1, -1, SQRT2)
    ]
    for dr,dc, cost in moves:
        nr,nc=r+dr,c+dc
        if not (0<=nr<ROWS and 0<=nc<COLS):
            continue
        if grid[nr][nc] == 3:
            continue
        if not ALLOW_DIAGONAL_CORNER_CUT and abs(dr) == 1 and abs(dc) == 1:
            if grid[r + dr][c] == 3 or grid[r][c + dc] == 3:
                continue
        yield (nr, nc, cost)

# --- A* ---
def heuristic(a,b):
    (x1, y1),(x2, y2) = a, b
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return (dx + dy) + (SQRT2 - 2) * min(dx, dy)

def astar(start,goal):
    t0=time.time()
    open_heap=[(0,0,start)]
    counter = 0
    parent={start:None}
    g={start:0}
    closed_set = set()
    while open_heap:
        _,_,current=heapq.heappop(open_heap)
        if current in closed_set:
            continue
        if current == goal:
            break
        closed_set.add(current)
        for nr, nc, move_cost in get_neighbors(*current):
            neighbor = (nr, nc)
            tentative_g=g[current]+terrain_cost[grid[neighbor[0]][neighbor[1]]]*move_cost
            if neighbor in closed_set and tentative_g >= g.get(neighbor, float('inf')):
                continue
            if tentative_g<g.get(neighbor, float('inf')):
                parent[neighbor]=current
                g[neighbor]=tentative_g
                f=tentative_g+heuristic(neighbor,goal)
                counter += 1
                heapq.heappush(open_heap,(f,counter,neighbor))
                if neighbor != start and neighbor != goal:
                    pygame.draw.rect(win,PURPLE,(neighbor[1]*CELL,neighbor[0]*CELL,CELL-1,CELL-1))
                    pygame.display.update()
    t1=time.time()
    path=[]
    node=goal
    while node and node in parent:
        path.append(node)
        node=parent[node]
    path.reverse()
    return path,t1-t0

# --- Kenarlıklı yazı ---
font=pygame.font.SysFont(None,28)
def draw_outlined_text(surface,text,pos,text_color,outline_color):
    x,y=pos
    for dx,dy in [(-2,0),(2,0),(0,-2),(0,2),(-2,-2),(-2,2),(2,-2),(2,2)]:
        outline = font.render(text,True,outline_color)
        surface.blit(outline,(x+dx,y+dy))
    main=font.render(text,True,text_color)
    surface.blit(main,(x,y))

# --- Ana Döngü ---
run=True
setup_mode=True
terrain_mode=0  # 0=düz,1=orta,2=zor,3=engel
draw_grid()

while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                setup_mode=False
            elif event.key==pygame.K_TAB:  # TAB ile zemin türünü değiştir
                terrain_mode=(terrain_mode+1)%4
            elif event.key==pygame.K_c:
                ALLOW_DIAGONAL_CORNER_CUT = not ALLOW_DIAGONAL_CORNER_CUT
                print("ALLOW_DIAGONAL_CORNER_CUT =", ALLOW_DIAGONAL_CORNER_CUT)

    if setup_mode:
        mouse_pressed=pygame.mouse.get_pressed()
        mx,my=pygame.mouse.get_pos()
        r,c=my//CELL,mx//CELL
        if mouse_pressed[0] and (r,c)!=start and (r,c)!=goal:
            grid[r][c]=terrain_mode
            draw_grid()
        elif mouse_pressed[2] and (r,c)!=start and (r,c)!=goal:
            grid[r][c]=0
            draw_grid()
    else:
        draw_grid()
        path_astar,time_astar=astar(start,goal)
        draw_path(path_astar,ORANGE)

        # Süreleri kenarlıklı yaz
        draw_outlined_text(win,f"A*: {time_astar:.3f}s",(10,10),PURPLE,BLACK)
        pygame.display.update()
        setup_mode=True  # Tek seferlik çalıştırma; yeniden Space basılınca tekrar

pygame.quit()

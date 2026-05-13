import pygame
import time
import heapq
from collections import deque
from PIL import Image

size = (400, 400)

def load_map_from_image(path, grid_size=(size), threshold=128):
    """
    path : PNG dosya yolu
    grid_size : (rows, cols) -> Pygame grid boyutu
    threshold : 0-255 arası, altında siyah (engel), üstünde beyaz (geçilebilir)
    """
    img = Image.open(path).convert('L')  # gri tonlama
    # img = img.resize(grid_size)           # grid boyutuna göre yeniden boyutlandır
    pixels = img.load()

    grid = []
    for y in range(grid_size[0]):
        row = []
        for x in range(grid_size[1]):
            val = 0 if pixels[x,y] > threshold else 3  # 0=düz, 3=engel
            row.append(val)
        grid.append(row)
    return grid

grid = load_map_from_image("maze(2).png", grid_size=(size))

# --- Ayarlar ---
WIDTH, HEIGHT = 1000, 1000
ROWS, COLS = size
CELL = WIDTH // COLS

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding with Terrain Types")

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
# grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

start = (0,0)
goal = (ROWS-1,COLS-1)

# --- Fonksiyonlar ---
def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            terrain = grid[r][c]
            if terrain==0:
                color=WHITE
            else:
                color=BLACK
            # elif terrain==1:
            #     color=YELLOW
            # elif terrain==2:
            #     color=BROWN
            # else:
            #     color=BLACK
            pygame.draw.rect(win,color,(c*CELL,r*CELL,CELL-1,CELL-1))
    pygame.draw.rect(win,GREEN,(start[1]*CELL,start[0]*CELL,CELL-1,CELL-1))
    pygame.draw.rect(win,RED,(goal[1]*CELL,goal[0]*CELL,CELL-1,CELL-1))
    pygame.display.update()

def draw_path(path,color):
    for r,c in path:
        pygame.draw.rect(win,color,(c*CELL,r*CELL,CELL-1,CELL-1))
        pygame.display.update()
        time.sleep(0.001)

def get_neighbors(r,c):
    for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr,nc=r+dr,c+dc
        if 0<=nr<ROWS and 0<=nc<COLS and grid[nr][nc]!=3:
            yield nr,nc

# --- BFS ---
def bfs(start,goal):
    t0=time.time()
    queue=deque([start])
    parent={start:None}
    while queue:
        r,c=queue.popleft()
        if (r,c)==goal: break
        for nr,nc in get_neighbors(r,c):
            if (nr,nc) not in parent:
                parent[(nr,nc)]=(r,c)
                queue.append((nr,nc))
                pygame.draw.rect(win,BLUE,(nc*CELL,nr*CELL,CELL-1,CELL-1))
                pygame.display.update()
    t1=time.time()
    path=[]
    node=goal
    while node and node in parent:
        path.append(node)
        node=parent[node]
    path.reverse()
    return path,t1-t0

# --- Dijkstra ---
def dijkstra(start,goal):
    t0=time.time()
    pq=[(0,start)]
    parent={start:None}
    dist={start:0}
    while pq:
        cost,(r,c)=heapq.heappop(pq)
        if (r,c)==goal: break
        for nr,nc in get_neighbors(r,c):
            new_cost=cost+terrain_cost[grid[nr][nc]]
            if (nr,nc) not in dist or new_cost<dist[(nr,nc)]:
                dist[(nr,nc)]=new_cost
                parent[(nr,nc)]=(r,c)
                heapq.heappush(pq,(new_cost,(nr,nc)))
                pygame.draw.rect(win,ORANGE,(nc*CELL,nr*CELL,CELL-1,CELL-1))
                pygame.display.update()
    t1=time.time()
    path=[]
    node=goal
    while node and node in parent:
        path.append(node)
        node=parent[node]
    path.reverse()
    return path,t1-t0

# --- A* ---
def heuristic(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def astar(start,goal):
    t0=time.time()
    pq=[(0,start)]
    parent={start:None}
    g={start:0}
    while pq:
        _,current=heapq.heappop(pq)
        if current==goal: break
        for neighbor in get_neighbors(*current):
            tentative_g=g[current]+terrain_cost[grid[neighbor[0]][neighbor[1]]]
            if neighbor not in g or tentative_g<g[neighbor]:
                g[neighbor]=tentative_g
                f=tentative_g+heuristic(neighbor,goal)
                parent[neighbor]=current
                heapq.heappush(pq,(f,neighbor))
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
        path_bfs,time_bfs=bfs(start,goal)
        draw_path(path_bfs,RED)

        draw_grid()
        path_dij,time_dij=dijkstra(start,goal)
        draw_path(path_dij,RED)

        draw_grid()
        path_astar,time_astar=astar(start,goal)
        draw_path(path_astar,RED)

        # Süreleri kenarlıklı yaz
        draw_outlined_text(win,f"BFS: {time_bfs:.3f}s",(10,10),BLUE,BLACK)
        draw_outlined_text(win,f"Dijkstra: {time_dij:.3f}s",(10,40),ORANGE,BLACK)
        draw_outlined_text(win,f"A*: {time_astar:.3f}s",(10,70),PURPLE,BLACK)
        pygame.display.update()
        setup_mode=True  # Tek seferlik çalıştırma; yeniden Space basılınca tekrar

pygame.quit()

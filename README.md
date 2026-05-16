# 🗺️ Pathfinding Visualizer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-00B140?style=for-the-badge&logo=python&logoColor=white)
![Algorithms](https://img.shields.io/badge/Algorithms-BFS%20%7C%20Dijkstra%20%7C%20A*-FF6B35?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)

**An interactive, real-time pathfinding algorithm visualizer built with Pygame.**  
Draw walls · Set terrain costs · Watch BFS, Dijkstra, and A* compete live.

[Features](#-features) · [Demos](#-demos) · [Installation](#-installation) · [Usage](#-usage) · [Algorithms](#-algorithms)

</div>

---

## 📖 Overview

This project provides a hands-on, visual way to understand how classic pathfinding algorithms work. You can draw custom mazes, set different terrain costs, and watch each algorithm explore the grid in real time — then compare their results side by side.

A pre-built maze loader is also included, allowing you to import any PNG image as a grid and run pathfinding directly on it.

---

## ✨ Features

- 🖱️ **Interactive grid editor** — draw walls and terrain with left/right mouse click
- 🎨 **Terrain cost system** — 3 terrain types (flat, medium, hard) with different traversal costs
- 📷 **PNG maze import** — load any grayscale image as a grid
- ↗️ **4-directional and 8-directional movement** — toggle diagonal traversal
- 🚫 **Corner-cutting prevention** — realistic diagonal movement constraints
- ⏱️ **Live performance timer** — see execution time for each algorithm
- 🔄 **Algorithm comparison** — run BFS, Dijkstra, and A* back-to-back on the same grid

---

## 🎬 Demos

| File | Algorithm(s) | Movement | Grid Source |
|------|-------------|----------|-------------|
| `Four_Directions.py` | A* | 4-directional | Hardcoded 5×5 |
| `Eight_Directions.py` | A* | 8-directional | Hardcoded 6×6 |
| `FD_Pygame.py` | A* | 4-directional | Interactive 30×30 |
| `ED_Pygame.py` | A* | 8-directional | Interactive 30×30 |
| `A_BFS_DIJK.py` | BFS + Dijkstra + A* | 4-directional | PNG image |
| `maze.py` | A* | 8-directional | PNG image |

---

## 🛠️ Installation

### Requirements

```
Python 3.8+
```

### Install Dependencies

```bash
pip install pygame pillow
```

### Clone the Repository

```bash
git clone https://github.com/your-username/pathfinding-visualizer.git
cd pathfinding-visualizer
```

---

## 🚀 Usage

### Interactive Grid (Recommended Starting Point)

```bash
# 4-directional A* on a drawable 30x30 grid
python FD_Pygame.py

# 8-directional A* with diagonal movement
python ED_Pygame.py
```

### Algorithm Comparison (BFS vs Dijkstra vs A*)

```bash
python A_BFS_DIJK.py
```

### Maze from PNG Image

```bash
python maze.py
```

> Make sure `maze(2).png` (400×400 grayscale) is in the same directory.

### Terminal-Only (No Pygame)

```bash
python Four_Directions.py   # 4-dir A* on a 5×5 grid
python Eight_Directions.py  # 8-dir A* on a 6×6 grid
```

---

## 🎮 Controls

| Key / Action | Effect |
|---|---|
| **Left click** | Draw wall or selected terrain |
| **Right click** | Erase (reset to flat terrain) |
| **SPACE** | Run pathfinding |
| **TAB** | Cycle terrain type (flat → medium → hard → wall) |
| **C** | Toggle corner-cutting for diagonal moves *(ED_Pygame, maze only)* |

---

## 🧠 Algorithms

### BFS — Breadth-First Search
Explores all neighbors at equal cost before moving outward. Guarantees the **shortest path in number of steps** but ignores terrain costs entirely.

```
Time complexity : O(V + E)
Optimal         : Only on uniform-cost grids
Completeness    : ✅ Always finds a path if one exists
```

### Dijkstra's Algorithm
Expands nodes in order of cumulative cost. Correctly handles **weighted terrain** and guarantees the globally optimal path.

```
Time complexity : O((V + E) log V)
Optimal         : ✅ Yes (with non-negative costs)
Completeness    : ✅ Yes
```

### A* (A-star)
Combines Dijkstra's cost tracking with a **heuristic estimate** to the goal, dramatically reducing unnecessary exploration.

```
Time complexity : O(E log V) — in practice much faster than Dijkstra
Optimal         : ✅ Yes (with admissible heuristic)
Completeness    : ✅ Yes
```

**Heuristics used:**

| Movement Mode | Heuristic | Formula |
|---|---|---|
| 4-directional | Manhattan | `|dx| + |dy|` |
| 8-directional | Octile | `(dx + dy) + (√2 − 2) × min(dx, dy)` |

---

## 🎨 Terrain System

| Terrain | Color | Cost | Keyboard |
|---------|-------|------|----------|
| Flat | White | 1 | TAB ×1 |
| Medium | Yellow | 2 | TAB ×2 |
| Hard | Brown | 3 | TAB ×3 |
| Wall | Black | ∞ | TAB ×4 |

Terrain costs directly affect **Dijkstra** and **A\*** path selection. BFS ignores them.

---

## 🗺️ PNG Maze Loader

`A_BFS_DIJK.py` and `maze.py` can load any grayscale PNG as a grid:

```python
def load_map_from_image(path, grid_size=(400, 400), threshold=128):
    # Pixels above threshold → passable (0)
    # Pixels below threshold → wall (3)
```

- **White pixels** → open cells
- **Black pixels** → walls
- Image is read pixel-by-pixel at native resolution (no resizing)

---

## 📂 Project Structure

```
pathfinding-visualizer/
├── Four_Directions.py    # A* — terminal only, 4-dir, 5×5 hardcoded grid
├── Eight_Directions.py   # A* — terminal only, 8-dir, 6×6 hardcoded grid
├── FD_Pygame.py          # A* — Pygame visualizer, 4-directional
├── ED_Pygame.py          # A* — Pygame visualizer, 8-directional + corner-cut toggle
├── A_BFS_DIJK.py         # BFS + Dijkstra + A* comparison, PNG maze support
├── maze.py               # A* on PNG maze, 8-directional
└── maze.png              # Sample maze image (400×400)
```

---

## 🔬 Algorithm Comparison

On a 400×400 maze with complex walls:

| Algorithm | Explores | Path Quality | Terrain-Aware |
|-----------|----------|-------------|----------------|
| BFS | Most nodes | Shortest steps | ❌ |
| Dijkstra | Many nodes | Lowest cost | ✅ |
| A* | Fewest nodes | Lowest cost | ✅ |

A* is typically the **fastest** in practice thanks to its heuristic guidance. BFS is the simplest. Dijkstra is the safest choice when terrain costs vary but no heuristic is available.

---

## 🌱 What's Next

Ideas to extend this project:

- **Bidirectional A\*** — search from both start and goal simultaneously
- **Jump Point Search (JPS)** — dramatically faster on open grids
- **Weighted A\*** — trade optimality for speed with `ε × h(n)`
- **Dynamic obstacles** — moving walls during search
- **RRT / PRM** — probabilistic planners for continuous spaces

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-algorithm`)
3. Commit your changes (`git commit -m 'Add: Jump Point Search'`)
4. Push to the branch (`git push origin feature/new-algorithm`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">

**Happy pathfinding! 🚀**

</div>

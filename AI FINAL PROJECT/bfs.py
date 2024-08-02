import pygame as pg
from random import random
from collections import deque

# Function to get the rectangle coordinates for drawing
def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2

# Function to get next possible nodes for BFS
def get_next_nodes(x, y):
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(x + dx, y + dy) for dx, dy in ways if 0 <= x + dx < cols and 0 <= y + dy < rows and not grid[y + dy][x + dx]]

# Initialize pygame
pg.init()
# Set up display
cols, rows = 25, 15
TILE = 60
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()

# Generate grid with obstacles randomly
grid = [[1 if random() < 0.2 else 0 for _ in range(cols)] for _ in range(rows)]

# Generate adjacency list graph for each grid cell
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

# BFS settings
start = (0, 0)
queue = deque([start])
visited = {start: None}
cur_node = start

# Main game loop
while True:
    # Fill screen with black
    sc.fill(pg.Color('black'))
    
    # Draw grid
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col:  # Obstacle
                pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=TILE // 5)

    # Draw BFS visited nodes and queue
    for x, y in visited:
        pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x, y))
    for x, y in queue:
        pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(x, y))
    
    # BFS logic
    if queue:
        cur_node = queue.popleft()
        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
    
    # Draw path
    path_head, path_segment = cur_node, cur_node
    while path_segment:
        pg.draw.rect(sc, pg.Color('white'), get_rect(*path_segment), TILE, border_radius=TILE // 3)
        path_segment = visited[path_segment]
    pg.draw.rect(sc, pg.Color('blue'), get_rect(*start), border_radius=TILE // 3)
    pg.draw.rect(sc, pg.Color('magenta'), get_rect(*path_head), border_radius=TILE // 3)
    
    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
    
    # Update display
    pg.display.flip()
    clock.tick(7)

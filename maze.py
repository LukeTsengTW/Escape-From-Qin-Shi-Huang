import pygame
import random
import heapq
from PIL import Image
from constants import TILE_SIZE, MAZE_COLS, MAZE_ROWS

# === Maze Map ===

def generate_maze(width, height, loop_chance=0.1):
    """
    width: Odd Width
    height: Odd Height
    loop_chance: The probability of deliberately breaking through a wall near an open path (0~1). 
                 The larger the value, the more loops there are. 0 means no loops.
    """
    
    assert width % 2 == 1 and height % 2 == 1

    maze = [[1 for _ in range(width)] for _ in range(height)]

    # Start Point
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0

    # Storage backtracking path
    stack = [(start_x, start_y)]

    directions = [(2,0), (-2,0), (0,2), (0,-2)]

    while stack:
        x, y = stack[-1]

        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < width-1 and 1 <= ny < height-1:
                if maze[ny][nx] == 1:
                    neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)

            maze[(y + ny)//2][(x + nx)//2] = 0
            maze[ny][nx] = 0

            stack.append((nx, ny))

            # Form a loop (optional) and try to break through non-traversed neighbor walls near the current point
            if random.random() < loop_chance:
                loop_dirs = [(2,0), (-2,0), (0,2), (0,-2)]
                random.shuffle(loop_dirs)
                for ldx, ldy in loop_dirs:
                    lx, ly = x + ldx, y + ldy
                    wall_x, wall_y = x + ldx//2, y + ldy//2
                    if 1 <= lx < width-1 and 1 <= ly < height-1:
                        if maze[ly][lx] == 0 and maze[wall_y][wall_x] == 1:
                            maze[wall_y][wall_x] = 0  # Break the wall to connect two paths
                            break  # Only one loop wall can be opened per round
        else:
            # No neighbors, backtracing
            stack.pop()

    return maze

# random generate the maze map
MAZE = generate_maze(MAZE_COLS, MAZE_ROWS)

walls = [pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
          for row, line in enumerate(MAZE)
          for col, tile in enumerate(line) if tile == 1]

def load_gif_frames(filename):
    pil_img = Image.open(filename)
    frames = []
    try:
        while True:
            frame = pil_img.convert("RGBA")
            mode = frame.mode
            size = frame.size
            data = frame.tobytes()
            py_image = pygame.image.fromstring(data, size, mode)
            frames.append(py_image)
            pil_img.seek(pil_img.tell() + 1)
    except EOFError:
        pass
    return frames

# detect if can walk
def is_path(x, y):
    col, row = x // TILE_SIZE, y // TILE_SIZE
    return 0 <= row < len(MAZE) and 0 <= col < len(MAZE[0]) and MAZE[row][col] == 0

# heuristic algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* Algorithm, for enemy - 修復版本
def a_star(start, goal):
    """
    A* pathfinding algorithm
    Args:
        start: (x, y) in pixel coordinates
        goal: (x, y) in pixel coordinates
    Returns:
        List of (x, y) positions in pixel coordinates representing the path
    """
    # Convert pixel coordinates to tile coordinates
    start_tile = (start[0] // TILE_SIZE, start[1] // TILE_SIZE)
    goal_tile = (goal[0] // TILE_SIZE, goal[1] // TILE_SIZE)
    
    # Bounds checking
    if (start_tile[1] < 0 or start_tile[1] >= len(MAZE) or 
        start_tile[0] < 0 or start_tile[0] >= len(MAZE[0]) or
        goal_tile[1] < 0 or goal_tile[1] >= len(MAZE) or 
        goal_tile[0] < 0 or goal_tile[0] >= len(MAZE[0])):
        return []
    
    # Check if start or goal is a wall
    if (MAZE[start_tile[1]][start_tile[0]] == 1 or 
        MAZE[goal_tile[1]][goal_tile[0]] == 1):
        return []
    
    frontier = [(0, start_tile)]
    came_from = {start_tile: None}
    cost_so_far = {start_tile: 0}

    while frontier:
        _, current = heapq.heappop(frontier)
        
        if current == goal_tile:
            break

        # Check all 4 directions
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Bounds checking
            if (0 <= neighbor[1] < len(MAZE) and 
                0 <= neighbor[0] < len(MAZE[0]) and 
                MAZE[neighbor[1]][neighbor[0]] == 0):
                
                new_cost = cost_so_far[current] + 1
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(goal_tile, neighbor)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

    # Reconstruct path
    path = []
    if goal_tile in came_from:
        current = goal_tile
        while current != start_tile:
            # Convert back to pixel coordinates
            path.append((current[0] * TILE_SIZE, current[1] * TILE_SIZE))
            current = came_from[current]
        path.reverse()
    
    # If no path found, return empty list
    return path

def random_walkable_position():
    while True:
        x = random.randint(0, MAZE_COLS - 1) * TILE_SIZE
        y = random.randint(0, MAZE_ROWS - 1) * TILE_SIZE
        if is_path(x + TILE_SIZE // 2, y + TILE_SIZE // 2):
            return x, y
        
def get_non_overlapping_positions():
    key_pos = random_walkable_position()
    while True:
        exit_pos = random_walkable_position()
        # Calculate the distance
        dx = abs(exit_pos[0] - key_pos[0])
        dy = abs(exit_pos[1] - key_pos[1])
        if dx >= TILE_SIZE*10 or dy >= TILE_SIZE*10:
            break
    return key_pos, exit_pos
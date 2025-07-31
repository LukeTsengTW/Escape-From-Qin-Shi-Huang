import pygame
import random
import heapq
import sys

# Try to import PIL, but handle the case where it's not available
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL not available, some features may be limited")

# Import constants (adjust this based on your PC version structure)
from constants import TILE_SIZE, MAZE_COLS, MAZE_ROWS

# === Maze Map ===

def generate_maze(width, height, loop_chance=0.1):
    """
    Generate a proper maze using recursive backtracking algorithm
    Creates narrow corridors with some 2-wide areas for better gameplay
    
    Args:
        width: Maze width (must be odd)
        height: Maze height (must be odd)  
        loop_chance: Probability of creating loops (0-1)
    
    Returns:
        2D list representing the maze (0=path, 1=wall)
    """
    assert width % 2 == 1 and height % 2 == 1, "Width and height must be odd numbers"

    # Initialize maze - all walls (1)
    maze = [[1 for _ in range(width)] for _ in range(height)]

    # Starting position (must be odd coordinates for proper maze generation)
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0

    # Stack for backtracking and visited set
    stack = [(start_x, start_y)]
    visited = set([(start_x, start_y)])

    # Directions: move by 2 to maintain wall-path-wall pattern
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    
    # Prevent infinite loops
    max_iterations = width * height * 10
    iteration_count = 0

    while stack and iteration_count < max_iterations:
        iteration_count += 1
        current_x, current_y = stack[-1]

        # Find unvisited neighbors that are 2 steps away
        neighbors = []
        for dx, dy in directions:
            nx, ny = current_x + dx, current_y + dy
            
            # Check if neighbor is within bounds and unvisited
            if (1 <= nx < width - 1 and 1 <= ny < height - 1 and 
                (nx, ny) not in visited):
                neighbors.append((nx, ny))

        if neighbors:
            # Choose random neighbor
            nx, ny = random.choice(neighbors)
            visited.add((nx, ny))

            # Carve path to neighbor
            # Remove wall between current and neighbor
            wall_x = current_x + (nx - current_x) // 2
            wall_y = current_y + (ny - current_y) // 2
            
            maze[wall_y][wall_x] = 0  # Remove wall between
            maze[ny][nx] = 0          # Mark destination as path

            # Selectively create wider corridors (only sometimes)
            if random.random() < 0.3:  # 30% chance for wider corridors
                # For horizontal corridors
                if nx != current_x:
                    # Make corridor 2 tiles wide vertically (sometimes)
                    if wall_y + 1 < height and random.random() < 0.5:
                        maze[wall_y + 1][wall_x] = 0
                    if ny + 1 < height and random.random() < 0.5:
                        maze[ny + 1][nx] = 0
                    if current_y + 1 < height and random.random() < 0.5:
                        maze[current_y + 1][current_x] = 0
                        
                # For vertical corridors  
                if ny != current_y:
                    # Make corridor 2 tiles wide horizontally (sometimes)
                    if wall_x + 1 < width and random.random() < 0.5:
                        maze[wall_y][wall_x + 1] = 0
                    if nx + 1 < width and random.random() < 0.5:
                        maze[ny][nx + 1] = 0
                    if current_x + 1 < width and random.random() < 0.5:
                        maze[current_y][current_x + 1] = 0

            stack.append((nx, ny))

            # Occasionally create loops for better connectivity
            if random.random() < loop_chance:
                for ldx, ldy in random.sample(directions, len(directions)):
                    lx, ly = current_x + ldx, current_y + ldy
                    if (1 <= lx < width - 1 and 1 <= ly < height - 1 and 
                        (lx, ly) in visited):
                        # Remove wall to create loop
                        loop_wall_x = current_x + ldx // 2
                        loop_wall_y = current_y + ldy // 2
                        if (0 <= loop_wall_x < width and 0 <= loop_wall_y < height):
                            maze[loop_wall_y][loop_wall_x] = 0
                        break

        else:
            # No unvisited neighbors, backtrack
            stack.pop()

    if iteration_count >= max_iterations:
        print("Warning: Maze generation hit iteration limit")

    # Ensure starting area is properly carved (2x2 area for player movement)
    maze[1][1] = 0
    if width > 2:
        maze[1][2] = 0
    if height > 2:
        maze[2][1] = 0
    if width > 2 and height > 2:
        maze[2][2] = 0

    return maze

# Global maze variables
MAZE = None
walls = []

def regenerate_maze():
    """Generate a new random maze and update all related data"""
    global MAZE, walls
    MAZE = generate_maze(MAZE_COLS, MAZE_ROWS)
    update_walls()
    
    # Debug: Count walkable tiles
    walkable_count = 0
    total_tiles = MAZE_COLS * MAZE_ROWS
    for row in MAZE:
        for tile in row:
            if tile == 0:
                walkable_count += 1
    
    print(f"Maze generated: {walkable_count}/{total_tiles} walkable tiles ({walkable_count/total_tiles*100:.1f}%)")
    
    return MAZE

def update_walls():
    """Update walls list based on current MAZE"""
    global walls
    if MAZE is None:
        walls = []
        return
    walls = [pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
             for row, line in enumerate(MAZE)
             for col, tile in enumerate(line) if tile == 1]

def load_gif_frames(filename):
    """Load GIF frames, with fallback for environments without PIL"""
    if not PIL_AVAILABLE:
        print(f"Warning: Cannot load GIF {filename} - PIL not available")
        return []
    
    try:
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
    except Exception as e:
        print(f"Warning: Could not load GIF {filename}: {e}")
        return []

def is_path(x, y):
    """Check if position is walkable"""
    if MAZE is None:
        return False
    col, row = x // TILE_SIZE, y // TILE_SIZE
    return 0 <= row < len(MAZE) and 0 <= col < len(MAZE[0]) and MAZE[row][col] == 0

def heuristic(a, b):
    """Manhattan distance heuristic for A* algorithm"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal):
    """
    A* pathfinding algorithm
    Args:
        start: (x, y) in pixel coordinates
        goal: (x, y) in pixel coordinates
    Returns:
        List of (x, y) positions in pixel coordinates representing the path
    """
    # Check if maze is available
    if MAZE is None:
        return []
        
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
    
    return path

def random_walkable_position():
    """Find a random walkable position in the maze"""
    max_attempts = 1000  # Prevent infinite loops
    attempts = 0
    
    while attempts < max_attempts:
        x = random.randint(0, MAZE_COLS - 1) * TILE_SIZE
        y = random.randint(0, MAZE_ROWS - 1) * TILE_SIZE
        if is_path(x + TILE_SIZE // 2, y + TILE_SIZE // 2):
            return x, y
        attempts += 1
    
    # Fallback: return a default position if no walkable position found
    print("Warning: Could not find walkable position, using fallback")
    return TILE_SIZE, TILE_SIZE  # Return top-left walkable area

def get_non_overlapping_positions():
    """Get key and exit positions that are well separated"""
    max_attempts = 1000
    attempt = 0
    
    key_pos = random_walkable_position()
    best_exit_pos = None
    best_distance = 0
    
    while attempt < max_attempts:
        exit_pos = random_walkable_position()
        # Calculate the distance
        dx = abs(exit_pos[0] - key_pos[0])
        dy = abs(exit_pos[1] - key_pos[1])
        # Calculate Manhattan distance in tiles
        manhattan_distance = (dx + dy) // TILE_SIZE
        
        # Store the position with the best distance found so far
        if manhattan_distance > best_distance:
            best_distance = manhattan_distance
            best_exit_pos = exit_pos
        
        # Try to find positions with good separation
        # Adaptive minimum distance based on maze size
        min_distance = min(8, MAZE_COLS // 3)  
        if manhattan_distance >= min_distance:
            return key_pos, exit_pos
            
        attempt += 1
    
    # If we couldn't find a good position after max_attempts, return the best we found
    if best_exit_pos is not None:
        return key_pos, best_exit_pos
    else:
        # Fallback: generate a new random position
        return key_pos, random_walkable_position()

# Initialize maze when module is imported
# Commented out to fix sync issue - maze will be generated when game starts
# if __name__ != "__main__":
#     regenerate_maze()
#     update_walls()

# Test function for standalone testing
def test_maze():
    """Test the maze generation"""
    print("Testing maze generation...")
    test_maze = generate_maze(21, 21)
    
    # Count walkable tiles
    walkable = sum(1 for row in test_maze for tile in row if tile == 0)
    total = len(test_maze) * len(test_maze[0])
    print(f"Generated maze: {walkable}/{total} walkable tiles ({walkable/total*100:.1f}%)")
    
    # Test position finding
    global MAZE
    MAZE = test_maze
    
    key_pos, exit_pos = get_non_overlapping_positions()
    print(f"Key position: {key_pos}")
    print(f"Exit position: {exit_pos}")
    
    # Test pathfinding
    path = a_star(key_pos, exit_pos)
    print(f"Path length: {len(path)} steps")
    
    print("Maze test completed successfully!")

if __name__ == "__main__":
    # Run test if script is executed directly
    test_maze()

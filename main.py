import pygame
import random

# Constants
WIDTH = 800  # Width of the grid
HEIGHT = 600  # Height of the grid
GRID_SIZE = 20  # Size of each grid cell
NUM_ROWS = HEIGHT // GRID_SIZE
NUM_COLS = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Rover:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.trail = []

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.trail.append((self.x, self.y))  # Add current position to the trail

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for trail_pos in self.trail:
            pygame.draw.rect(screen, BLUE, (trail_pos[0] * GRID_SIZE, trail_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


class EndGoal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, YELLOW, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))


def generate_obstacles(num_obstacles, exclude_positions):
    obstacles = []
    for _ in range(num_obstacles):
        while True:
            x = random.randint(0, NUM_COLS - 1)
            y = random.randint(0, NUM_ROWS - 1)
            if (x, y) not in exclude_positions:
                break
        obstacles.append(Obstacle(x, y))
    return obstacles


def is_collision(rover, obstacles):
    for obstacle in obstacles:
        if rover.x == obstacle.x and rover.y == obstacle.y:
            return True
    return False


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, end, obstacles):
    # The set of discovered nodes that may need to be (re-)expanded
    open_set = set([start])
    
    # For node n, came_from[n] is the node immediately preceding it on the cheapest path from start to n currently known.
    came_from = {}
    
    # For node n, came_dir[n] stores the delta coordinates (dx, dy) from its parent node to itself.
    came_dir = {}

    # For node n, gscore[n] is the cost of the cheapest path from start to end.
    gscore = {start: 0}

    # For node n, fscore[n] := gscore[n] + h(n).
    fscore = {start: heuristic(start, end)}

    while open_set:
        # the node in openSet having the lowest fScore[] value
        current = min(open_set, key=lambda x: fscore.get(x, float('inf')))

        if current == end:
            delta_path = []
            while current in came_from:
                delta_path.append(came_dir[current])
                current = came_from[current]
            return delta_path[::-1]

        open_set.remove(current)

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = current[0] + dx, current[1] + dy
            tentative_gscore = gscore[current] + 1

            if 0 <= neighbor[0] < NUM_COLS and 0 <= neighbor[1] < NUM_ROWS:
                if neighbor in obstacles or tentative_gscore >= gscore.get(neighbor, float('inf')):
                    continue

                came_from[neighbor] = current
                came_dir[neighbor] = (dx, dy)  # store delta coordinates
                gscore[neighbor] = tentative_gscore
                fscore[neighbor] = tentative_gscore + heuristic(neighbor, end)
                open_set.add(neighbor)

    return []  # Return an empty list if there is no path to the end


def main():
    start_x = random.randint(0, NUM_COLS - 1)
    start_y = random.randint(0, NUM_ROWS - 1)
    rover = Rover(start_x, start_y)

    while True:
        end_x = random.randint(0, NUM_COLS - 1)
        end_y = random.randint(0, NUM_ROWS - 1)
        if end_x != start_x or end_y != start_y:
            break
    end = EndGoal(end_x, end_y)

    obstacles = generate_obstacles(50, exclude_positions=[(start_x, start_y), (end_x, end_y)])

    # Create a set with obstacle positions for easy lookup
    obstacle_positions = set((obstacle.x, obstacle.y) for obstacle in obstacles)
    
    # Calculate the path using A* algorithm
    delta_path = astar(None, (rover.x, rover.y), (end.x, end.y), obstacle_positions)
    
    # Iterator for delta_path
    delta_path_iter = iter(delta_path)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        # Make the rover follow the path
        try:
            delta_position = next(delta_path_iter)
            new_x = rover.x + delta_position[0]
            new_y = rover.y + delta_position[1]
            if 0 <= new_x < NUM_COLS and 0 <= new_y < NUM_ROWS and not is_collision(Rover(new_x, new_y), obstacles):
                rover.move(delta_position[0], delta_position[1])
        except StopIteration:
            pass

        # check if the rover reached the end goal
        if rover.x == end.x and rover.y == end.y:
            print("End goal reached!")

        screen.fill(WHITE)
        draw_grid()
        for obstacle in obstacles:
            obstacle.draw()
        end.draw()
        rover.draw()
        pygame.display.flip()
        clock.tick(5)


if __name__ == '__main__':
    main()

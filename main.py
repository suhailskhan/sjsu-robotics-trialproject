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

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1
        elif keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1

        new_x = rover.x + dx
        new_y = rover.y + dy
        if 0 <= new_x < NUM_COLS and 0 <= new_y < NUM_ROWS and not is_collision(Rover(new_x, new_y), obstacles):
            rover.move(dx, dy)

        # check if the rover reached the end goal
        if rover.x == end.x and rover.y == end.y:
            print("End goal reached!")
            pygame.quit()
            return

        screen.fill(WHITE)
        draw_grid()
        for obstacle in obstacles:
            obstacle.draw()
        end.draw()
        rover.draw()
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()

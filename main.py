import pygame
import random

# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define the dimensions of the grid
GRID_SIZE = 20
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Define the shapes of the blocks
SHAPES = [
    [[1, 1, 1], [0, 1, 0]],  # T-shape
    [[1, 1], [1, 1]],        # Square
    [[1, 1, 1, 1]],          # I-shape
    [[0, 1, 1], [1, 1, 0]],  # S-shape
    [[1, 1, 0], [0, 1, 1]],  # Z-shape
    [[1, 1, 1], [1, 0, 0]],  # L-shape
    [[1, 1, 1], [0, 0, 1]]   # J-shape
]

class Tetris:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_shape = self.get_new_shape()
        self.current_position = [0, GRID_WIDTH // 2 - len(self.current_shape[0]) // 2]
        self.next_shape = self.get_new_shape()
        self.score = 0
        self.game_over = False

    def get_new_shape(self):
        return random.choice(SHAPES)

    def rotate_shape(self):
        self.current_shape = [list(row) for row in zip(*self.current_shape[::-1])]

    def valid_move(self, shape, offset):
        off_x, off_y = offset
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    if x + off_x < 0 or x + off_x >= GRID_WIDTH or y + off_y >= GRID_HEIGHT:
                        return False
                    if self.grid[y + off_y][x + off_x]:
                        return False
        return True

    def freeze_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[y + self.current_position[0]][x + self.current_position[1]] = cell
        self.clear_lines()
        self.current_shape = self.next_shape
        self.current_position = [0, GRID_WIDTH // 2 - len(self.current_shape[0]) // 2]
        if not self.valid_move(self.current_shape, self.current_position):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        for i, row in enumerate(self.grid[::-1]):
            if all(row):
                del self.grid[GRID_HEIGHT - 1 - i]
                self.grid.insert(0, [0] * GRID_WIDTH)
                lines_cleared += 1
        self.score += lines_cleared ** 2

    def move(self, dx):
        if not self.valid_move(self.current_shape, (self.current_position[0], self.current_position[1] + dx)):
            return False
        self.current_position[1] += dx
        return True

    def drop(self):
        if not self.valid_move(self.current_shape, (self.current_position[0] + 1, self.current_position[1])):
            self.freeze_shape()
            return False
        self.current_position[0] += 1
        return True

    def draw_grid(self, screen):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, BLUE, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, GREEN, pygame.Rect((self.current_position[1] + x) * GRID_SIZE,
                                                                (self.current_position[0] + y) * GRID_SIZE,
                                                                GRID_SIZE, GRID_SIZE))

    def run(self):
        screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
        clock = pygame.time.Clock()
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move(-1)
                    if event.key == pygame.K_RIGHT:
                        self.move(1)
                    if event.key == pygame.K_DOWN:
                        self.drop()
                    if event.key == pygame.K_UP:
                        self.rotate_shape()
            if not self.drop():
                self.freeze_shape()
            screen.fill(BLACK)
            self.draw_grid(screen)
            pygame.display.flip()
            clock.tick(5)
        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set window dimensions
screen_width, screen_height = 1536, 864
screen = pygame.display.set_mode((screen_width, screen_height))

# Set window title
pygame.display.set_caption("Klotski Game")

# Define colors (RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Define the playable area
playable_width = 1000
playable_height = 800
playable_x = playable_width / 15
playable_y = (screen_height - playable_height) // 2
playable_area = pygame.Rect(playable_x, playable_y, playable_width, playable_height)

# Define grid dimensions
cols, rows = 5, 4
cell_width = playable_width // cols
cell_height = playable_height // rows

# Class for the red square (occupies 4 cells)
class RedSquare:
    def __init__(self, grid_x, grid_y, size, color):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.size = size
        self.color = color
        self.rects = []  # Store 4 rectangles for 4 grid cells
        self.update_position()

    def update_position(self):
        # Clear the existing rects
        self.rects = []

        # Define 4 rects based on the grid for the red square occupying 4 cells
        self.rects.append(pygame.Rect(playable_x + self.grid_x * cell_width,
                                      playable_y + self.grid_y * cell_height,
                                      cell_width, cell_height))
        self.rects.append(pygame.Rect(playable_x + (self.grid_x + 1) * cell_width,
                                      playable_y + self.grid_y * cell_height,
                                      cell_width, cell_height))
        self.rects.append(pygame.Rect(playable_x + self.grid_x * cell_width,
                                      playable_y + (self.grid_y + 1) * cell_height,
                                      cell_width, cell_height))
        self.rects.append(pygame.Rect(playable_x + (self.grid_x + 1) * cell_width,
                                      playable_y + (self.grid_y + 1) * cell_height,
                                      cell_width, cell_height))

    def move(self, direction, squares):
        prev_x, prev_y = self.grid_x, self.grid_y

        if direction == 'left' and self.grid_x > 0:
            self.grid_x -= 1
        elif direction == 'right' and self.grid_x < cols - 2:
            self.grid_x += 1
        elif direction == 'up' and self.grid_y > 0:
            self.grid_y -= 1
        elif direction == 'down' and self.grid_y < rows - 2:
            self.grid_y += 1

        self.update_position()
        self.prevent_overlap(squares, prev_x, prev_y)

    def prevent_overlap(self, squares, prev_x, prev_y):
        red_positions = [(self.grid_x, self.grid_y), (self.grid_x + 1, self.grid_y),
                         (self.grid_x, self.grid_y + 1), (self.grid_x + 1, self.grid_y + 1)]

        for square in squares:
            yellow_pos = (square.grid_x, square.grid_y)
            if yellow_pos in red_positions:
                self.grid_x, self.grid_y = prev_x, prev_y
                self.update_position()
                break

    def draw(self, surface):
        for rect in self.rects:
            pygame.draw.rect(surface, self.color, rect)

        main_rect = pygame.Rect(
            self.rects[0].x,
            self.rects[0].y,
            2 * self.rects[0].width,
            2 * self.rects[0].height
        )
        pygame.draw.rect(surface, (0, 0, 0), main_rect, 2)

# Class for the yellow squares
class YellowSquare:
    def __init__(self, grid_x, grid_y, size, color):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.size = size
        self.color = color
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.update_position()

    def update_position(self):
        self.rect.x = playable_x + self.grid_x * cell_width
        self.rect.y = playable_y + self.grid_y * cell_height

    def move(self, direction, squares, red_square):
        prev_x, prev_y = self.grid_x, self.grid_y

        if direction == 'left' and self.grid_x > 0:
            self.grid_x -= 1
        elif direction == 'right' and self.grid_x < cols - 1:
            self.grid_x += 1
        elif direction == 'up' and self.grid_y > 0:
            self.grid_y -= 1
        elif direction == 'down' and self.grid_y < rows - 1:
            self.grid_y += 1

        self.update_position()
        self.prevent_overlap(squares, red_square, prev_x, prev_y)

    def prevent_overlap(self, squares, red_square, prev_x, prev_y):
        # Check for collision with each other yellow square
        for square in squares:
            if square != self and self.rect.colliderect(square.rect):
                self.grid_x, self.grid_y = prev_x, prev_y
                self.update_position()
                return

        # Check for collision with the red square's cells
        red_positions = [(red_square.grid_x, red_square.grid_y), (red_square.grid_x + 1, red_square.grid_y),
                         (red_square.grid_x, red_square.grid_y + 1), (red_square.grid_x + 1, red_square.grid_y + 1)]
        yellow_pos = (self.grid_x, self.grid_y)

        if yellow_pos in red_positions:
            self.grid_x, self.grid_y = prev_x, prev_y
            self.update_position()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

# Initialize squares
# red_square = RedSquare(grid_x=cols // 2 - 1, grid_y=rows // 2 - 1, size=cell_width * 2, color=RED) #somewhat in the middle
red_square = RedSquare(grid_x=0, grid_y=1, size=cell_width * 2, color=RED)
squares = [
    YellowSquare(grid_x=0, grid_y=0, size=cell_width, color=YELLOW),
    YellowSquare(grid_x=1, grid_y=0, size=cell_width, color=YELLOW),
    YellowSquare(grid_x=2, grid_y=0, size=cell_width, color=YELLOW),
    YellowSquare(grid_x=3, grid_y=0, size=cell_width, color=YELLOW),
    YellowSquare(grid_x=4, grid_y=0, size=cell_width, color=YELLOW),
    YellowSquare(grid_x=2, grid_y=1, size=cell_width, color=YELLOW),
    YellowSquare(grid_x=2, grid_y=2, size=cell_width, color=YELLOW),
    YellowSquare(grid_x=3, grid_y=1, size=cell_width, color=YELLOW),
    YellowSquare(grid_x=3, grid_y=2, size=cell_width, color=YELLOW),
    YellowSquare(grid_x=0, grid_y=3, size=cell_width, color=YELLOW),
    YellowSquare(grid_x=1, grid_y=3, size=cell_width, color=YELLOW),
    YellowSquare(grid_x=2, grid_y=3, size=cell_width, color=YELLOW),
    YellowSquare(grid_x=3, grid_y=3, size=cell_width, color=YELLOW),
    YellowSquare(grid_x=4, grid_y=3, size=cell_width, color=YELLOW),
]

# Control variable to track selected square
selected_square = None

target_positions = [(3, 1), (4, 1), (3, 2), (4, 2)]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            for rect in red_square.rects:
                if rect.collidepoint(mouse_pos):
                    selected_square = red_square
                    break

            for square in squares:
                if square.rect.collidepoint(mouse_pos):
                    selected_square = square
                    break

        elif event.type == pygame.KEYUP:
            if selected_square:
                direction = None
                if event.key == pygame.K_LEFT:
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'
                elif event.key == pygame.K_UP:
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    direction = 'down'

                if direction:
                    # Check the instance and call the appropriate move function
                    if isinstance(selected_square, RedSquare):
                        selected_square.move(direction, squares)
                    elif isinstance(selected_square, YellowSquare):
                        selected_square.move(direction, squares, red_square)

    screen.fill(GRAY)
    pygame.draw.rect(screen, WHITE, playable_area)

    for i in range(cols):
        for j in range(rows):
            rect = pygame.Rect(playable_x + i * cell_width, playable_y + j * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, BLUE, rect, 2)

    red_square.draw(screen)

    for square in squares:
        square.draw(screen)
    
    if all((red_square.grid_x + dx, red_square.grid_y + dy) in target_positions # THIIIIIIIIIS WOOOOOOOOORKS
       for dx in range(2) for dy in range(2)):
            print("CONGRATULATIONSSS")
            running = False  # End the game if the objective is reached


    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()

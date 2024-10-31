import pygame
import sys

# Initialize Pygame
pygame.init()

# Set window dimensions
screen_width, screen_height = 1536, 864
screen = pygame.display.set_mode((screen_width, screen_height))

# Set window title
pygame.display.set_caption("Grid Movement Example")

# Define colors (RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Define the playable area
playable_width = 1000
playable_height = 800
playable_x = playable_width / 15 #(screen_width - playable_width) // 2
playable_y = (screen_height - playable_height) // 2
playable_area = pygame.Rect(playable_x, playable_y, playable_width, playable_height)

# Define grid dimensions
cols, rows = 10, 8
cell_width = playable_width // cols
cell_height = playable_height // rows

# Class for the moving red square (which occupies 4 grid cells)
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

    def move(self, direction, yellow_square):
        # Store the previous grid position
        prev_x, prev_y = self.grid_x, self.grid_y

        # Move logic for the red square
        if direction == 'left' and self.grid_x > 0:
            self.grid_x -= 1
        elif direction == 'right' and self.grid_x < cols - 2:  # Move up to 2 cells from the right edge
            self.grid_x += 1
        elif direction == 'up' and self.grid_y > 0:
            self.grid_y -= 1
        elif direction == 'down' and self.grid_y < rows - 2:  # Move up to 2 cells from the bottom edge
            self.grid_y += 1

        # Update position and check for collisions
        self.update_position()
        self.prevent_overlap(yellow_square, prev_x, prev_y)

    def prevent_overlap(self, yellow_square, prev_x, prev_y):
        # Check if any of the red square's rects collide with the yellow square's grid position
        red_positions = [(self.grid_x, self.grid_y), (self.grid_x + 1, self.grid_y),
                         (self.grid_x, self.grid_y + 1), (self.grid_x + 1, self.grid_y + 1)]
        yellow_pos = (yellow_square.grid_x, yellow_square.grid_y)

        if yellow_pos in red_positions:
            # Revert to previous position if there's a collision
            self.grid_x, self.grid_y = prev_x, prev_y
            self.update_position()

    def draw(self, surface):
        for rect in self.rects:
            pygame.draw.rect(surface, self.color, rect)

# Class for the moving yellow square
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

    def move(self, direction, red_square):
        # Store the previous grid position
        prev_x, prev_y = self.grid_x, self.grid_y

        # Move logic for the yellow square
        if direction == 'left' and self.grid_x > 0:
            self.grid_x -= 1
        elif direction == 'right' and self.grid_x < cols - 1:
            self.grid_x += 1
        elif direction == 'up' and self.grid_y > 0:
            self.grid_y -= 1
        elif direction == 'down' and self.grid_y < rows - 1:
            self.grid_y += 1

        # Update position and check for collisions
        self.update_position()
        self.prevent_overlap(red_square, prev_x, prev_y)

    def prevent_overlap(self, red_square, prev_x, prev_y):
        # Check if the yellow square's grid position overlaps with any of the red square's grid positions
        red_positions = [(red_square.grid_x, red_square.grid_y), (red_square.grid_x + 1, red_square.grid_y),
                         (red_square.grid_x, red_square.grid_y + 1), (red_square.grid_x + 1, red_square.grid_y + 1)]
        yellow_pos = (self.grid_x, self.grid_y)

        if yellow_pos in red_positions:
            # Revert to previous position if there's a collision
            self.grid_x, self.grid_y = prev_x, prev_y
            self.update_position()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# Initialize squares
red_square = RedSquare(grid_x=cols // 2 - 1, grid_y=rows // 2 - 1, size=cell_width * 2, color=RED)
yellow_square = YellowSquare(grid_x=3, grid_y=3, size=cell_width, color=YELLOW)

# Control variable to track selected square
selected_square = None

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click
            mouse_pos = pygame.mouse.get_pos()

            # Check if the click was inside any of the red square's four cells
            for rect in red_square.rects:
                if rect.collidepoint(mouse_pos):
                    selected_square = 'red'
                    break  # Exit the loop once red is selected

            # If red is not selected, check for the yellow square
            if yellow_square.rect.collidepoint(mouse_pos):
                selected_square = 'yellow'

        elif event.type == pygame.KEYUP:  # Check for key release
            if selected_square == 'red':
                if event.key == pygame.K_LEFT:
                    red_square.move('left', yellow_square)
                elif event.key == pygame.K_RIGHT:
                    red_square.move('right', yellow_square)
                elif event.key == pygame.K_UP:
                    red_square.move('up', yellow_square)
                elif event.key == pygame.K_DOWN:
                    red_square.move('down', yellow_square)
            elif selected_square == 'yellow':
                if event.key == pygame.K_LEFT:
                    yellow_square.move('left', red_square)
                elif event.key == pygame.K_RIGHT:
                    yellow_square.move('right', red_square)
                elif event.key == pygame.K_UP:
                    yellow_square.move('up', red_square)
                elif event.key == pygame.K_DOWN:
                    yellow_square.move('down', red_square)

    # Fill the screen with gray
    screen.fill(GRAY)

    # Draw the playable area (white background)
    pygame.draw.rect(screen, WHITE, playable_area)

    # Draw the grid
    for i in range(cols):
        for j in range(rows):
            rect = pygame.Rect(playable_x + i * cell_width, playable_y + j * cell_height, cell_width, cell_height)


            # Set default grid line color
            color = BLUE

            # Change color for a specific cell (for example, cell at (3, 3))
            if i == 1 and j == 2:  # Modify these indices to target another cell
                color = (0, 255, 0)  # Set it to green, or any color of your choice
            

            pygame.draw.rect(screen, color, rect, 2)  # Drawing the grid lines

    # Draw the squares
    red_square.draw(screen)
    yellow_square.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to 60 FPS
    pygame.time.Clock().tick(60)

# Quit Pygame and close the window
pygame.quit()
sys.exit()
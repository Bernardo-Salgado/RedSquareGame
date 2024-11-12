import sys
import pygame
from collections import namedtuple

# Define colors (RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Define the playable area
playable_width = 640  # 128 each block
playable_height = 512
playable_x = (1536 - playable_width) // 2
playable_y = (864 - playable_height) // 2
playable_area = pygame.Rect(playable_x, playable_y, playable_width, playable_height)

# Define grid dimensions
cols, rows = 5, 4
cell_width = playable_width // cols
cell_height = playable_height // rows

# Define a named tuple for positions
Position = namedtuple('Position', ['x', 'y'])


class Block:
    def __init__(self, grid_x, grid_y, size_x, size_y):

        self.grid_x = grid_x # block coordinates
        self.grid_y = grid_y
        self.size_x = size_x # Width of the block
        self.size_y = size_y # Height of the block
        self.color = self.assign_color() # Automatically assign color based on size

    def get_positions(self):
        # Return the space occupied by the block of size: size_x x size_y
        return [(self.grid_x + dx, self.grid_y + dy) for dx in range(self.size_x) for dy in range(self.size_y)]

    def assign_color(self):
        # Assign color based on the size of the block using predefined constants
        if self.size_x == 1 and self.size_y == 1:
            return YELLOW # Use the YELLOW constant for 1x1 blocks
        elif self.size_x == 2 and self.size_y == 2:
            return RED # Use the RED constant for 2x2 blocks
        else:
            return GRAY # Use the GRAY constant for other sizes

    def draw(self, surface):
        # Calculate the rectangle for the block based on its grid position and size
        rect = pygame.Rect(playable_x + self.grid_x * cell_width, playable_y + self.grid_y * cell_height,
                           self.size_x * cell_width, self.size_y * cell_height)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 2)


class Game:
    def __init__(self):

        pygame.init()
        self.screen_width, self.screen_height = 1536, 864
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Klotski Game")

        # Initial state of the game
        self.initial_state = [
            Block(0, 0, 2, 2),  # Red block (2x2)
            Block(1, 2, 1, 1),  # Yellow block (1x1)
            Block(4, 3, 1, 1),  # Another yellow block
            Block(3, 1, 1, 1),  # Another yellow block
        ]
        # The current state (can change as blocks move)
        self.state = list(self.initial_state)
        self.selected_block = None
        self.start_pos = None
        self.move_count = 0 # Moves counter

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_event(event)
            # Check if win and draw the board
            self.update()
            self.draw()

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.start_pos = pygame.mouse.get_pos()
            self.selected_block = self.get_selected_block(self.start_pos)

        elif event.type == pygame.MOUSEMOTION and self.selected_block is not None:
            # Update the position of the selected block based on mouse movement
            current_pos = pygame.mouse.get_pos()
            self.handle_swipe(self.start_pos, current_pos)

        elif event.type == pygame.MOUSEBUTTONUP and self.selected_block is not None:
            current_pos = pygame.mouse.get_pos()
            self.handle_swipe(self.start_pos, current_pos)
            self.selected_block = None
            self.start_pos = None

    def get_selected_block(self, mouse_pos):

        for block in self.state:
            # Create a rectangle for the block based on its grid position and size
            rect = pygame.Rect(playable_x + block.grid_x * cell_width, playable_y + block.grid_y * cell_height,
                               block.size_x * cell_width, block.size_y * cell_height)
            if rect.collidepoint(mouse_pos):
                return block
        return None

    def handle_swipe(self, start_pos, end_pos):
        # Calculate the grid positions based on mouse coordinates
        start_grid_x = (start_pos[0] - playable_x) // cell_width
        start_grid_y = (start_pos[1] - playable_y) // cell_height
        end_grid_x = (end_pos[0] - playable_x) // cell_width
        end_grid_y = (end_pos[1] - playable_y) // cell_height

        # Determine the direction of movement
        dx = end_grid_x - start_grid_x
        dy = end_grid_y - start_grid_y

        # Only allow movement of one cell
        if abs(dx) > abs(dy):
            direction = 'right' if dx == 1 else 'left' if dx == -1 else None
        else:
            direction = 'down' if dy == 1 else 'up' if dy == -1 else None

        if direction and self.selected_block:
            moved = self.move_block(self.selected_block, direction)
            if moved:  # Only increment if a move was successful
                self.move_count += 1
                self.start_pos = end_pos
                self.print_current_state() # Update start_pos to the new position

    def move_block(self, block, direction):

        prev_x, prev_y = block.grid_x, block.grid_y
        if direction == 'left' and block.grid_x > 0:
            block.grid_x -= 1
        elif direction == 'right' and block.grid_x < cols - block.size_x:
            block.grid_x += 1
        elif direction == 'up' and block.grid_y > 0:
            block.grid_y -= 1
        elif direction == 'down' and block.grid_y < rows - block.size_y:
            block.grid_y += 1
        # Check for collisions with other blocks
        if self.check_collisions(block):
            # If there is a collision, revert the position
            block.grid_x, block.grid_y = prev_x, prev_y
            print(f"Move {direction} blocked by collision.")
            return False
#        print(f"Moved {direction} to ({block.grid_x}, {block.grid_y})")
        return True

    def check_collisions(self, block):

        occupied_positions = set()
        for b in self.state:
            # Collect positions of all blocks except the one being moved
            if b != block:
                occupied_positions.update(b.get_positions())
        # Return collision detection state
        return any(pos in occupied_positions for pos in block.get_positions())

    def print_current_state(self):
        # Print current state
        print(f"Move: {self.move_count}")
        for block in self.state:
            print(f"Block at ({block.grid_x}, {block.grid_y}) with size ({block.size_x}, {block.size_y})")

    def is_goal_state(self):
        # Target position
        target_positions = [(3, 1), (4, 1), (3, 2), (4, 2)]
        red_block = self.state[0]
        # Return the win state
        return all(pos in target_positions for pos in red_block.get_positions())

    def update(self):
        # Update the game win state, if win print the info and close the window
        if self.is_goal_state():
            print("CONGRATULATIONS! You've solved the puzzle!")
            pygame.quit()
            sys.exit()

    def draw(self):

        self.screen.fill(GRAY)
        pygame.draw.rect(self.screen, WHITE, playable_area)
        # Draw the grid
        for i in range(cols):
            for j in range(rows):
                rect = pygame.Rect(playable_x + i * cell_width, playable_y + j * cell_height, cell_width, cell_height)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
        # Draw all blocks in the game state
        for block in self.state:
            block.draw(self.screen)
        # Draw the move counter
        self.draw_move_counter()
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    def draw_move_counter(self):

        font = pygame.font.SysFont(None, 40)
        move_text = font.render(f'Moves: {self.move_count}', True, (0, 0, 0))
        self.screen.blit(move_text, (self.screen_width - 150, 20))

if __name__ == "__main__":
    game = Game()
    game.run()

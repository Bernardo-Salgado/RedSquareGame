import sys
import pygame
from collections import namedtuple

# Define colors (RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Define the playable area
playable_width = 640   # 128 each block
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
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.size_x = size_x  # Width of the block
        self.size_y = size_y  # Height of the block
        self.color = self.assign_color()  # Automatically assign color based on size

    def get_positions(self):
        return [(self.grid_x + dx, self.grid_y + dy) for dx in range(self.size_x) for dy in range(self.size_y)]

    def assign_color(self):
        # Assign color based on the size of the block using predefined constants
        if self.size_x == 1 and self.size_y == 1:
            return YELLOW  # Use the YELLOW constant for 1x1 blocks
        elif self.size_x == 2 and self.size_y == 2:
            return RED  # Use the RED constant for 2x2 blocks
        else:
            return GRAY  # Use the GRAY constant for other sizes

    def draw(self, surface):
        # Calculate the rectangle for the block based on its grid position and size
        rect = pygame.Rect(playable_x + self.grid_x * cell_width, playable_y + self.grid_y * cell_height,
                           self.size_x * cell_width, self.size_y * cell_height)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 2)  # Draw border

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1536, 864
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Klotski Game")

        self.state = [
            Block(0, 0, 2, 2),  # Red block (2x2)
            Block(1, 3, 1, 1),  # Yellow block (1x1)
            Block(4, 3, 1, 1),  # Another yellow block
            Block(3, 1, 1, 1),  # Another yellow block
        ]

        self.selected_block = None
        self.start_pos = None
        self.move_count = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_event(event)

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

# [POST-SOLVER FUNCTIONS]------------------------------------------------------
    def get_piece_index(self, piece):
        for index, block in enumerate(self.state):
            # Check if the block's position matches the piece's position
            if (block.grid_x, block.grid_y) == piece:
                return index
        return None  # Return None if the piece is not found

    def get_move_direction(self, start_position, end_position):
        start_x, start_y = start_position
        end_x, end_y = end_position

        if start_x == end_x:
            if start_y < end_y:
                return 'down'  # Moving down
            elif start_y > end_y:
                return 'up'  # Moving up
        elif start_y == end_y:
            if start_x < end_x:
                return 'right'  # Moving right
            elif start_x > end_x:
                return 'left'  # Moving left

        return None  # Return None if the move is invalid
# [/POST-SOLVER FUNCTIONS]-------------------------------------------------------------
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
            if dx == 1:  # Move right
                direction = 'right'
            elif dx == -1:  # Move left
                direction = 'left'
            else:
                direction = None
        else:
            if dy == 1:  # Move down
                direction = 'down'
            elif dy == -1:  # Move up
                direction = 'up'
            else:
                direction = None

        if direction and self.selected_block:
            moved = self.move_block(self.selected_block, direction)

            if moved:  # Only increment if a move was successful
                self.move_count += 1  # Increment move counter
                self.start_pos = end_pos  # Update start_pos to the new position

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
            return False  # Move was not successful

#        print(f"Moved {direction} to ({block.grid_x}, {block.grid_y})")
        return True  # Move was successful

    def check_collisions(self, block):
        occupied_positions = set()

        # Collect positions of all blocks except the one being moved
        for b in self.state:
            if b != block:  # Exclude the block being moved
                occupied_positions.update(b.get_positions())

        # Check if the block's new positions collide with occupied positions
        for pos in block.get_positions():
            if pos in occupied_positions:
                return True  # Collision detected
        return False  # No collision

    def update(self):
        # Check for completion condition
        target_positions = [(3, 1), (4, 1), (3, 2), (4, 2)]

        # Get the positions of the red block
        red_block = self.state[0]  # Assuming the red block is always the first in the state list
        red_positions = red_block.get_positions()

        # Check if all positions of the red block are in the target positions
        if all(pos in target_positions for pos in red_positions):
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
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Draw grid lines

        # Draw all blocks in the game state
        for block in self.state:
            block.draw(self.screen)

        # Draw the move counter
        self.draw_move_counter()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    def draw_move_counter(self):
        font = pygame.font.SysFont(None, 40)
        move_text = font.render(f'Moves: {self.move_count}', True, (0, 0, 0))  # Black text
        self.screen.blit(move_text, (self.screen_width - 150, 20))  # Adjust position as needed

if __name__ == "__main__":
    game = Game()
    game.run()


import sys
import pygame
from collections import namedtuple

# Define colors (RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

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


class Block:
    def __init__(self, grid_x, grid_y, size_x, size_y, color):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.size_x = size_x  # Width of the block
        self.size_y = size_y  # Height of the block
        # self.color = self.assign_color()  # Automatically assign color based on size

    def get_positions(self):
        return [(self.grid_x + dx, self.grid_y + dy) for dx in range(self.size_x) for dy in range(self.size_y)]

    def assign_color(self):
        # Assign color based on the size of the block using predefined constants
        if self.size_x == 1 and self.size_y == 1:
            return YELLOW
        elif self.size_x == 2 and self.size_y == 2:
            return RED
        elif self.size_x == 2 and self.size_y == 1:
            return GREEN
        elif self.size_x == 1 and self.size_y == 2:
            return BLUE
        else:
            return GRAY  # Use the GRAY constant for other sizes

    # def draw(self, surface):
    #     # Calculate the rectangle for the block based on its grid position and size
    #     rect = pygame.Rect(playable_x + self.grid_x * cell_width, playable_y + self.grid_y * cell_height,
    #                        self.size_x * cell_width, self.size_y * cell_height)
    #     pygame.draw.rect(surface, self.color, rect)
    #     pygame.draw.rect(surface, BLACK, rect, 2)  # Draw border


class Game:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1536, 864
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Klotski Game")

        self.state = [
            ((0, 0), (2, 2)),  # Block at (0, 0) with size 2x2 - game.stae[0] is the RED block
            ((1, 3), (1, 1)),  # Block at (1, 3) with size 1x1
            ((4, 3), (2, 1)),  # Block at (4, 3) with size 1x1
            ((3, 1), (1, 2)),  # Block at (3, 1) with size 1x1
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
        for index, (pos, size) in enumerate(self.state):
            # Create a rectangle for the block based on its grid position and size
            rect = pygame.Rect(playable_x + pos[0] * cell_width, playable_y + pos[1] * cell_height,
                               size[0] * cell_width, size[1] * cell_height)
            if rect.collidepoint(mouse_pos):
                return index  # Return the index of the selected block
        return None

    # [POST-SOLVER FUNCTIONS]------------------------------------------------------
    def get_piece_index(self, piece):
        for index, (pos, size) in enumerate(self.state):
            # Check if the block's position matches the piece's position
            if pos == piece:  # Compare the position directly
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

        if direction and self.selected_block is not None:
            # Retrieve the block data using the selected block index
            block_data = self.state[self.selected_block]

            # Check if the new position is within the grid boundaries
            new_pos = block_data[0]  # Current position
            if direction == 'left':
                new_pos = (new_pos[0] - 1, new_pos[1])
            elif direction == 'right':
                new_pos = (new_pos[0] + 1, new_pos[1])
            elif direction == 'up':
                new_pos = (new_pos[0], new_pos[1] - 1)
            elif direction == 'down':
                new_pos = (new_pos[0], new_pos[1] + 1)

            # Check if the new position is within the grid boundaries
            if 0 <= new_pos[0] < cols and 0 <= new_pos[1] < rows:
                moved = self.move_block(block_data, direction)  # Pass the block data instead of the index

                if moved:  # Only increment if a move was successful
                    self.move_count += 1  # Increment move counter
                    self.start_pos = end_pos  # Update start_pos to the new position

    def move_block(self, block, direction):
        prev_pos = block[0]  # Get the previous position
        size = block[1]  # Get the size of the block

        # Calculate the new position based on the direction
        if direction == 'left':
            new_pos = (prev_pos[0] - 1, prev_pos[1])
        elif direction == 'right':
            new_pos = (prev_pos[0] + 1, prev_pos[1])
        elif direction == 'up':
            new_pos = (prev_pos[0], prev_pos[1] - 1)
        elif direction == 'down':
            new_pos = (prev_pos[0], prev_pos[1] + 1)
        else:
            return False  # Invalid move

        # Update the block's position
        new_block = (new_pos, size)

        # Check for collisions
        if self.check_collisions(new_block, self.get_piece_index(prev_pos)):
            print(f"Move {direction} blocked by collision.")
            return False  # Move was not successful

        # Update the state with the new position
        block_index = self.get_piece_index(prev_pos)
        self.state[block_index] = new_block
        return True  # Move was successful

    def check_collisions(self, block, block_index):
        occupied_positions = set()

        # Collect positions of all blocks except the one being moved
        for index, b in enumerate(self.state):
            if index != block_index:  # Exclude the block being moved
                pos, size = b
                for dx in range(size[0]):
                    for dy in range(size[1]):
                        occupied_positions.add((pos[0] + dx, pos[1] + dy))

        # Check if the block's new positions collide with occupied positions
        block_pos, block_size = block
        for dx in range(block_size[0]):
            for dy in range(block_size[1]):
                if (block_pos[0] + dx, block_pos[1] + dy) in occupied_positions:
                    print(f"Collision detected at {block_pos[0] + dx}, {block_pos[1] + dy}")
                    return True  # Collision detected
        return False  # No collision

    def update(self):
        # Check for completion condition
        target_positions = {(3, 1), (4, 1), (3, 2), (4, 2)}

        # Get the positions of the red block (assuming it's the first block in the state)
        red_block_position = self.state[0][0]  # This is now a tuple (grid_x, grid_y)

        # Get the positions occupied by the red block (2x2)
        red_positions = {(red_block_position[0], red_block_position[1]),
                         (red_block_position[0] + 1, red_block_position[1]),
                         (red_block_position[0], red_block_position[1] + 1),
                         (red_block_position[0] + 1, red_block_position[1] + 1)}

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

        for (pos, size) in self.state:

            if size[0] == 1 and size[1] == 1:
                color = YELLOW
            elif size[0] == 2 and size[1] == 2:
                color = RED
            elif size[0] == 2 and size[1] == 1:
                color = BLUE
            elif size[0] == 1 and size[1] == 2:
                color = GREEN

            rect = pygame.Rect(playable_x + pos[0] * cell_width, playable_y + pos[1] * cell_height,
                               size[0] * cell_width, size[1] * cell_height)
            pygame.draw.rect(self.screen, color, rect)  # Color based on size
            pygame.draw.rect(self.screen, BLACK, rect, 2)  # Draw border

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
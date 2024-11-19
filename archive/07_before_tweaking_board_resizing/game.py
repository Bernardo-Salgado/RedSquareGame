import sys
import pygame
import random
from collections import namedtuple
from end import EndMenu
from menu import setup_cols, setup_rows

# Define colors (RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Define the number of columns and rows
cols = setup_cols
rows = setup_rows

# Define a fixed tile size
tile_size = 128

# Calculate the playable area based on the number of columns and rows
playable_width = cols * tile_size
playable_height = rows * tile_size
playable_x = (1920 - playable_width) // 2
playable_y = (1080 - playable_height) // 2
playable_area = pygame.Rect(playable_x, playable_y, playable_width, playable_height)

#Define target positions.

target_positions = [(cols - 2, rows/2 - 1), (cols - 1, rows/2 - 1), (cols - 2, rows/2 ), (cols - 1, rows/2)]

# Define cell dimensions
cell_width = tile_size
cell_height = tile_size

# Define a named tuple for positions
Position = namedtuple('Position', ['x', 'y'])


class Block:

    # Class-level attributes for images
    small_duck_image = None
    red_duck_image = None

    def __init__(self, grid_x, grid_y, size_x, size_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.size_x = size_x
        self.size_y = size_y
        self.image = self.assign_image()

    @classmethod
    def load_images(cls, small_duck_image, red_duck_image, hor_duck_image, ver_duck_image):
        cls.small_duck_image = small_duck_image
        cls.red_duck_image = red_duck_image
        cls.hor_duck_image = hor_duck_image  # Add horizontal duck image
        cls.ver_duck_image = ver_duck_image  # Add vertical duck image

    def get_positions(self):
        # Return the space occupied by the block of size: size_x x size_y
        return [(self.grid_x + dx, self.grid_y + dy) for dx in range(self.size_x) for dy in range(self.size_y)]

    def assign_image(self):
        if self.size_x == 1 and self.size_y == 1:
            return self.small_duck_image
        elif self.size_x == 2 and self.size_y == 2:
            return self.red_duck_image
        elif self.size_x == 2 and self.size_y == 1:
            return Block.hor_duck_image  # Use the horizontal duck image
        elif self.size_x == 1 and self.size_y == 2:
            return Block.ver_duck_image  # Use the vertical duck image
        return None  # Return None if no image is assigned

    def draw(self, surface):
        rect = pygame.Rect(playable_x + self.grid_x * cell_width, playable_y + self.grid_y * cell_height,
                           self.size_x * cell_width, self.size_y * cell_height)
        if self.image:
            surface.blit(self.image, rect.topleft)
        else:
            pygame.draw.rect(surface, GRAY, rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 2)

    def __lt__(self, other):
        # Block comparison basing on their position (top left coordinates)
        if self.grid_x == other.grid_x: # if x is the same
            return self.grid_y < other.grid_y
        return self.grid_x < other.grid_x

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1920, 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption("Klotski Game")

        # Load the duck images
        self.red_duck_image = pygame.image.load('img/redduck.png').convert_alpha()
        self.red_duck_image = pygame.transform.scale(self.red_duck_image, (cell_width * 2, cell_height * 2))
        self.small_duck_image = pygame.image.load('img/smallduck.png').convert_alpha()
        self.small_duck_image = pygame.transform.scale(self.small_duck_image, (cell_width * 1, cell_height * 1))

        # Load horizontal and vertical duck images
        self.hor_duck_image = pygame.image.load('img/horduck.png').convert_alpha()
        self.hor_duck_image = pygame.transform.scale(self.hor_duck_image, (cell_width * 2, cell_height * 1))
        self.ver_duck_image = pygame.image.load('img/verduck.png').convert_alpha()
        self.ver_duck_image = pygame.transform.scale(self.ver_duck_image, (cell_width * 1, cell_height * 2))

        # Load images into Block class
        Block.load_images(self.small_duck_image, self.red_duck_image, self.hor_duck_image, self.ver_duck_image)

        # Load sounds
        self.quack_sounds = [pygame.mixer.Sound(f'audio/quack_{i}.wav') for i in range(10)]
        self.sick_quack_sounds = [pygame.mixer.Sound(f'audio/sick_quack_{i}.wav') for i in range(10)]
        self.swirl_sounds = [pygame.mixer.Sound(f'audio/swirl_{i}.wav') for i in range(25)]  # Load swirl sounds

        # Load and play music
        pygame.mixer.music.load('audio/duckmusic.mp3')  # Load the music file
        pygame.mixer.music.play(-1)  # Play the music on loop (-1 means loop indefinitely)

        self.initial_state = self.create_initial_state()  # Create initial state
        self.reset()  # Call reset to initialize the game state

        self.cols = cols
        self.rows = rows
        self.target_positions = [(self.cols - 2, self.rows // 2 - 1),
                                 (self.cols - 1, self.rows // 2 - 1),
                                 (self.cols - 2, self.rows // 2),
                                 (self.cols - 1, self.rows // 2)]

    def create_initial_state(self):
        # Define the initial state of the game
        return [
            Block(0, 1, 2, 2),  # Sick red duck
            Block(3, 2, 1, 1),  # Healthy small duck
            Block(1, 0, 2, 1),  # Horizontal duck
            Block(4, 0, 1, 2)  # Vertical duck
            # Add other blocks as needed
        ]

    def reset(self):
        # Reset the current state to the initial state
        self.state = [Block(block.grid_x, block.grid_y, block.size_x, block.size_y) for block in self.initial_state]
        self.selected_block = None
        self.start_pos = None
        self.move_count = 0
        self.game_won = False

    def run(self):
        end_menu = EndMenu(self.screen, self)  # Pass the Game instance to EndMenu
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_event(event)

            # Check for win and draw the board
            self.update()
            self.draw()

            # If the game is won, show the end menu
            if self.game_won:
                result = end_menu.show_end_menu()  # Use the end_menu instance
                if result == "back_to_menu":
                    self.reset()  # Reset the game state to return to the main menu
                    return  # Go back to the main menu

            # If the game is won, delay a bit before quitting to show the last move
            if self.game_won:
                pygame.time.wait(500)  # Wait for 0.5 second before quitting
                pygame.quit()
                sys.exit()

    def update(self):
        if self.is_goal_state():
            print("CONGRATULATIONS! You've solved the puzzle!")
            self.game_won = True  # Set the game_won flag

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
                self.print_current_state()  # Update start_pos to the new position

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

        # Play sounds based on the block index
        block_index = self.state.index(block)
        if block_index == 0:  # If it's the first block (2x2)
            sound_to_play = random.choice(self.sick_quack_sounds)
        else:  # For blocks with index > 0
            sound_to_play = random.choice(self.quack_sounds)

        # Play the selected sound
        sound_to_play.play()
        # Play a random swirl sound
        random.choice(self.swirl_sounds).play()

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
        red_block = self.state[0]
        # Return the win state
        return all(pos in target_positions for pos in red_block.get_positions())


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
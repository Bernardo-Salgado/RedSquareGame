from dis import Positions
import sys
import pygame
from utilities import *
import time

# <Michal> [importing the random library to allow to play random duck sounds]-----------------------
import random
# </Michal> ---------------------------------------------------------------------------------------

# Define colors (RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Define the playable area
# <Michal> [experimenting with the playable area to fit the board, was : width 1000, height 800]-------------
playable_width = 1000
playable_height = 800
playable_x = playable_width / 15
playable_y = (864 - playable_height) // 2  # Use a fixed height of 864 for the window
playable_area = pygame.Rect(playable_x, playable_y, playable_width, playable_height)

# Define grid dimensions
cols, rows = 5, 4
cell_width = playable_width // cols
cell_height = playable_height // rows

# </Michal> ---------------------------------------------------------------------------

class Game:
    def __init__(self):
        # Set window dimensions
        self.screen_width, self.screen_height = 1536, 864
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Klotski Game")

# <Michal> [loading images and sounds, playing music] -----------------------------------------------------
        # Load the animated water frames
        self.water_frames = [pygame.image.load(f'img/water_{i}.png').convert() for i in range(4)]
        self.current_frame = 0  # Index for the current frame
        self.frame_delay = 100  # Delay in milliseconds between frames
        self.last_frame_update = pygame.time.get_ticks()  # Track time for frame updates

        # Load the red duck image
        self.red_duck_image = pygame.image.load('img/redduck.png').convert_alpha()  # Load the red duck image with alpha
        self.red_duck_image = pygame.transform.scale(self.red_duck_image, (cell_width * 2, cell_height * 2))  # Scale to occupy 4 cells

        # Load the small duck image
        self.small_duck_image = pygame.image.load('img/smallduck.png').convert_alpha()
        self.small_duck_image = pygame.transform.scale(self.small_duck_image, (cell_width * 1, cell_height * 1))

        # Load sounds
        self.quack_sounds = [pygame.mixer.Sound(f'audio/quack_{i}.wav') for i in range(10)]
        self.sick_quack_sounds = [pygame.mixer.Sound(f'audio/sick_quack_{i}.wav') for i in range(10)]
        self.swirl_sounds = [pygame.mixer.Sound(f'audio/swirl_{i}.wav') for i in range(25)]  # Load swirl sounds

        # Load and play music
        pygame.mixer.music.load('audio/duckmusic.mp3')  # Load the music file
        pygame.mixer.music.play(-1)  # Play the music on loop (-1 means loop indefinitely)
# </Michal> ---------------------------------------------------------------------

# <Michal> [Added the game instance to facilitate the playing of sounds]--------------------
        # Initialize squares
        self.red_square = RedSquare(grid_x=0, grid_y=1, size=cell_width * 2, color=RED, game=self)
# </Michal>-------------------------------------------------------------------------------

        self.squares = self.create_yellow_squares()

        self.selected_square = None
        self.start_pos = None  # To track the starting position for swipe

        self.move_count = 0  # Initialize move counter

# <Michal> [adding the game=self reference to allow for the sound to play]------------------------------
    def create_yellow_squares(self):
        return [
            YellowSquare(grid_x=0, grid_y=0, size=cell_width, color=YELLOW, game=self),
            YellowSquare(grid_x=1, grid_y=0, size=cell_width, color=YELLOW, game=self),
            YellowSquare(grid_x=2, grid_y=0, size=cell_width, color=YELLOW, game=self),
            YellowSquare(grid_x=3, grid_y=0, size=cell_width, color=YELLOW, game=self),
            YellowSquare(grid_x=4, grid_y=0, size=cell_width, color=YELLOW, game=self),
            YellowSquare(grid_x=2, grid_y=1, size=cell_width, color=YELLOW, game=self),
            YellowSquare(grid_x=2, grid_y=2, size=cell_width, color=YELLOW, game=self),
            YellowSquare(grid_x=3, grid_y=1, size=cell_width, color=YELLOW, game=self),
            YellowSquare(grid_x=3, grid_y=2, size=cell_width, color=YELLOW, game=self),
            YellowSquare(grid_x=0, grid_y=3, size=cell_width, color=YELLOW, game=self),
            YellowSquare(grid_x=1, grid_y=3, size=cell_width, color=YELLOW, game=self),
            YellowSquare(grid_x=2, grid_y=3, size=cell_width, color=YELLOW, game=self),
            YellowSquare(grid_x=3, grid_y=3, size=cell_width, color=YELLOW, game=self),
            YellowSquare(grid_x=4, grid_y=3, size=cell_width, color=YELLOW, game=self),
        ]

    # </Michal> -----------------------------------------------------
    def get_board(self):
        # Create a board representation
        return Board(self.red_square, self.squares)  # Adjust based on your Board implementation

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            self.start_pos = mouse_pos  # Store the starting position for swipe
            
            for rect in self.red_square.rects:
                if rect.collidepoint(mouse_pos):
                    self.selected_square = self.red_square
                    break
            for square in self.squares:
                if square.rect.collidepoint(mouse_pos):
                    self.selected_square = square
                    break

        elif event.type == pygame.MOUSEMOTION and self.selected_square is not None:
            pass  # You could implement hover effect if desired

        elif event.type == pygame.MOUSEBUTTONUP and self.selected_square is not None:
            current_pos = pygame.mouse.get_pos()
            self.handle_swipe(self.start_pos, current_pos)

            # Reset the selection after moving
            self.selected_square = None
            self.start_pos = None

    def handle_swipe(self, start_pos, end_pos):
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]

        direction = None
        if abs(dx) > abs(dy):  # More horizontal movement
            if dx > 0:
                direction = 'right'
            else:
                direction = 'left'
        else:  # More vertical movement
            if dy > 0:
                direction = 'down'
            else:
                direction = 'up'

        if direction:
            moved = False
            if isinstance(self.selected_square, RedSquare):
                moved = self.selected_square.move(direction, self.squares)  # Now expects a return value
            elif isinstance(self.selected_square, YellowSquare):
                moved = self.selected_square.move(direction, self.squares, self.red_square)  # Now expects a return value
            
            if moved:  # Only increment if a move was successful
                self.move_count += 1  # Increment move counter

    def update(self):

# <Michal> ---------------------------------------------------------------------
        # Update the current frame based on the frame delay
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_update > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.water_frames)  # Loop through frames
            self.last_frame_update = current_time  # Reset the timer
# </Michal> ---------------------------------------------------------------------

        # Check for completion condition
        target_positions = [(3, 1), (4, 1), (3, 2), (4, 2)]
        if all((self.red_square.grid_x + dx, self.red_square.grid_y + dy) in target_positions
               for dx in range(2) for dy in range(2)):
            print("CONGRATULATIONSSS")
            pygame.quit()
            sys.exit()

    def draw(self):
        self.screen.fill(GRAY)  # Fill the background with gray
        pygame.draw.rect(self.screen, WHITE, playable_area)  # Draw the white playable area

# <Michal> [drawing images]-----------------------------------------------------
        # Draw the animated water image on each grid cell
        for i in range(cols):
            for j in range(rows):
                # Calculate the position for each tile
                tile_rect = pygame.Rect(playable_x + i * cell_width, playable_y + j * cell_height, cell_width,
                                        cell_height)

                # Scale the water frame to the desired size (e.g., cell_width, cell_height)
                scaled_water_frame = pygame.transform.scale(self.water_frames[self.current_frame],(cell_width, cell_height ))

                self.screen.blit(scaled_water_frame, tile_rect.topleft)  # Draw the current frame

        # Draw the red duck image occupying 4 cells
        red_duck_x = self.red_square.grid_x  # Get the grid x position of the red square
        red_duck_y = self.red_square.grid_y  # Get the grid y position of the red square
        self.screen.blit(self.red_duck_image, (
        playable_x + red_duck_x * cell_width, playable_y + red_duck_y * cell_height))  # Draw the red duck image


# I removed the old method
#        self.red_square.draw(self.screen)



        # Draw the small duck images for yellow squares
        for square in self.squares:
            square.update_position()  # Ensure the position is updated
            self.screen.blit(self.small_duck_image, (playable_x + square.grid_x * cell_width,
                                                     playable_y + square.grid_y * cell_height))  # Draw the small duck image

# </Michal> ---------------------------------------------------------------------
        # Draw the move counter
        self.draw_move_counter()

        pygame.display.flip()  # Update the display
        pygame.time.Clock().tick(60)  # Control the frame rate


    def draw_move_counter(self):
        font = pygame.font.SysFont(None, 40)
        move_text = font.render(f'Moves: {self.move_count}', True, (255, 255, 255))  # White text
        self.screen.blit(move_text, (self.screen_width - 150, 20))  # Adjust position as needed

    def play_solution(self, solution_moves):
        """Plays the sequence of moves generated by the BFS solver."""
        for piece, direction in solution_moves:
            # Check which piece is being moved and apply the move
            if piece == self.red_square:
                self.red_square.move(direction, self.squares)
            else:
                piece.move(direction, self.squares, self.red_square)

            # Update display after each move
            self.draw()  # Draw updated positions of all pieces
            pygame.display.flip()  # Refresh the display

            # Add a delay to slow down the visualization
            pygame.time.delay(500)  # 500 ms delay per move (adjust as needed)

            # Optionally, you can check for quit events to exit while visualizing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
# <Michal> [stopping the music when quitting]----------------------------------------------
                    pygame.mixer.music.stop()  # Stop the music
# </Michal> ------------------------------------------------------------------------------
                    pygame.quit()
                    return

# Class for the red square (occupies 4 cells)

# <Michal> [adding the game parameter to allow for playing of sounds]-------------------------
class RedSquare:
    def __init__(self, grid_x, grid_y, size, color, game):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.size = size
        self.color = color
        self.rects = []  # Store 4 rectangles for 4 grid cells
        self.update_position()
        self.game = game #Store the reference to the game instance

# </Michal>--------------------------------------------------------------------------------

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
        moved = self.prevent_overlap(squares, prev_x, prev_y)

# <Michal> [Added a sound played during movement]----------------------------------------------
        # Play a random sick quack sound if the move was successful
        if moved and (self.grid_x != prev_x or self.grid_y != prev_y):
            # Play a random sick quack sound
            random_sick_sound = random.choice(self.game.sick_quack_sounds)  # Access the sick quack sounds
            random_sick_sound.play()

            # Play a random swirl sound
            random_swirl_sound = random.choice(self.game.swirl_sounds)
            random_swirl_sound.play()

            return True  # Return True if a valid move occurred
# </Michal> -----------------------------------------------------------------------------------
        
        # Incrementa o contador de movimentos apenas se a posição mudou
        if moved and (self.grid_x != prev_x or self.grid_y != prev_y):
            return True  # Retorna True se houve movimento válido

        return False  # Retorna False se o movimento foi bloqueado ou inválido
    

    def prevent_overlap(self, squares, prev_x, prev_y):
        red_positions = [(self.grid_x, self.grid_y), (self.grid_x + 1, self.grid_y),
                         (self.grid_x, self.grid_y + 1), (self.grid_x + 1, self.grid_y + 1)]

        for square in squares:
            yellow_pos = (square.grid_x, square.grid_y)
            if yellow_pos in red_positions:
                self.grid_x, self.grid_y = prev_x, prev_y
                self.update_position()
                return False  # Return False indicating an overlap occurred
        return True  # Return True indicating no overlap occurred

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
    
    def possible_moves(self, empty_positions):
        moves = []
        # Check all four directions
        if (self.grid_x - 1, self.grid_y) in empty_positions:  # Left
            moves.append((self.grid_x - 1, self.grid_y))
        if (self.grid_x + 2, self.grid_y) in empty_positions:  # Right
            moves.append((self.grid_x + 2, self.grid_y))
        if (self.grid_x, self.grid_y - 1) in empty_positions:  # Up
            moves.append((self.grid_x, self.grid_y - 1))
        if (self.grid_x, self.grid_y + 2) in empty_positions:  # Down
            moves.append((self.grid_x, self.grid_y + 2))
        return moves

# Class for the yellow squares

# <Michal> [Adding the game parameter to allow for the sound to play]-----------------------
class YellowSquare:
    def __init__(self, grid_x, grid_y, size, color, game):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.size = size
        self.color = color
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.update_position()
        self.game = game  # Store the reference to the Game instance

# </Michal>---------------------------------------------------------------------------------
    def update_position(self):
        self.rect.x = playable_x + self.grid_x * cell_width
        self.rect.y = playable_y + self.grid_y * cell_height

    def move(self, direction, squares, red_square):
        prev_x, prev_y = self.grid_x, self.grid_y
        moved = False

        if direction == 'left' and self.grid_x > 0:
            self.grid_x -= 1
        elif direction == 'right' and self.grid_x < cols - 1:
            self.grid_x += 1
        elif direction == 'up' and self.grid_y > 0:
            self.grid_y -= 1
        elif direction == 'down' and self.grid_y < rows - 1:
            self.grid_y += 1

        self.update_position()
        moved = self.prevent_overlap(squares, red_square, prev_x, prev_y)

# <Michal> [Playing a sound when the yellow duck moves]---------------------------------------------------
        # Play a random quack sound if the move was successful
        if moved and (self.grid_x != prev_x or self.grid_y != prev_y):
            # Play a random quack sound
            random_sound = random.choice(self.game.quack_sounds)
            random_sound.play()

            # Play a random swirl sound
            random_swirl_sound = random.choice(self.game.swirl_sounds)
            random_swirl_sound.play()

            return True  # Return True if a valid move occurred
# </Michal> ----------------------------------------------------------------------------------------------
        # Incrementa o contador de movimentos apenas se a posição mudou
        if moved and (self.grid_x != prev_x or self.grid_y != prev_y):
            return True  # Retorna True se houve movimento válido

        return False  # Retorna False se o movimento foi bloqueado ou inválido

    def prevent_overlap(self, squares, red_square, prev_x, prev_y):
        # Check for collision with each other yellow square
        for square in squares:
            if square != self and self.rect.colliderect(square.rect):
                self.grid_x, self.grid_y = prev_x, prev_y
                self.update_position()
                return False

        # Check for collision with the red square's cells
        red_positions = [(red_square.grid_x, red_square.grid_y), (red_square.grid_x + 1, red_square.grid_y),
                         (red_square.grid_x, red_square.grid_y + 1), (red_square.grid_x + 1, red_square.grid_y + 1)]
        yellow_pos = (self.grid_x, self.grid_y)

        if yellow_pos in red_positions:
            self.grid_x, self.grid_y = prev_x, prev_y
            self.update_position()
        
        return True

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

    def possible_moves(self, empty_positions):
        moves = []
        # Check all four directions
        if (self.grid_x - 1, self.grid_y) in empty_positions:  # Left
            moves.append((self.grid_x - 1, self.grid_y))
        if (self.grid_x + 1, self.grid_y) in empty_positions:  # Right
            moves.append((self.grid_x + 1, self.grid_y))
        if (self.grid_x, self.grid_y - 1) in empty_positions:  # Up
            moves.append((self.grid_x, self.grid_y - 1))
        if (self.grid_x, self.grid_y + 1) in empty_positions:  # Down
            moves.append((self.grid_x, self.grid_y + 1))
        return moves

class Board:
    def __init__(self, red_square, yellow_squares):
        self.red_square = red_square
        self.yellow_squares = yellow_squares
        self.squares = [red_square] + yellow_squares  # Combine for easy access

    @property
    def number_of_steps(self):
        return self.history_insert

    @classmethod
    def from_game(cls, red_square, yellow_squares):
        """Create a Board instance from the game state."""
        return cls(red_square, yellow_squares)
    
    def potential_moves(self):
        moves = []
        empty_positions = self.empty_positions()
    
        # Check moves for the red square
        for position in self.red_square.possible_moves(empty_positions):  # You need to implement this
            moves.append((self.red_square, position))

        # Check moves for each yellow square
        for yellow in self.yellow_squares:
            for position in yellow.possible_moves(empty_positions):  # Implement this in YellowSquare
                moves.append((yellow, position))

        return moves


    def empty_positions(self):
        # Create a set of all positions
        positions = {(x, y) for x in range(cols) for y in range(rows)}
        
        # Remove positions occupied by the yellow squares
        for yellow in self.yellow_squares:
            positions.remove((yellow.grid_x, yellow.grid_y))
        
        # Remove positions occupied by the red square
        red_positions = [
            (self.red_square.grid_x, self.red_square.grid_y),
            (self.red_square.grid_x + 1, self.red_square.grid_y),
            (self.red_square.grid_x, self.red_square.grid_y + 1),
            (self.red_square.grid_x + 1, self.red_square.grid_y + 1)
        ]
        
        for pos in red_positions:
            if pos in positions:
                positions.remove(pos)

        return positions  # Return empty positions

    @property
    def is_solved(self):
        # Check if the red square is in the expected finish position
        return (self.red_square.grid_x, self.red_square.grid_y) == (3, 1)

    def draw(self, surface):
        # Draw the squares on the board
        self.red_square.draw(surface)
        for yellow in self.yellow_squares:
            yellow.draw(surface)

    def can_move(self, piece, click_position):
        empty_positions = self.empty_positions()
        # Logic to determine if the move can be made based on click_position
        pass  # Implement logic as needed

    def move(self, piece, position):
        # Check if the move is valid and update positions accordingly
        pass  # Implement logic to perform the move

import sys
import pygame
from collections import namedtuple
Position = namedtuple('Position', ['x', 'y'])

# Define colors (RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Define the playable area
playable_width = 640   # 128 each block
playable_height = 512
playable_x = playable_width / 15
playable_y = (864 - playable_height) // 2  # Use a fixed height of 864 for the window
playable_area = pygame.Rect(playable_x, playable_y, playable_width, playable_height)

# Define grid dimensions
cols, rows = 5, 4
cell_width = playable_width // cols
cell_height = playable_height // rows

class Game:
    def __init__(self):
        # Set window dimensions
        self.screen_width, self.screen_height = 1536, 864
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Klotski Game")

        # Initialize squares
        self.red_square = RedSquare(grid_x=0, grid_y=1, size=cell_width * 2, color=RED)  # RedSquare instance
        self.squares = self.create_yellow_squares()  # YellowSquare instances

        self.selected_square = None
        self.start_pos = None  # To track the starting position for swipe
        self.move_count = 0  # Initialize move counter

        self.pieces = self.squares + [self.red_square]  # Combine the lists
        self.board = self.get_board()  # Initialize the board

    def create_yellow_squares(self):
        return [
            YellowSquare(grid_x=0, grid_y=0, size=cell_width, color=YELLOW),
            YellowSquare(grid_x=1, grid_y=0, size=cell_width, color=YELLOW),
            YellowSquare(grid_x=2, grid_y=0, size=cell_width, color=YELLOW),
            YellowSquare(grid_x=3, grid_y=0, size=cell_width, color=YELLOW),
            # YellowSquare(grid_x=4, grid_y=0, size=cell_width, color=YELLOW),
            # YellowSquare(grid_x=2, grid_y=1, size=cell_width, color=YELLOW),
            # YellowSquare(grid_x=2, grid_y=2, size=cell_width, color=YELLOW),
            # YellowSquare(grid_x=3, grid_y=1, size=cell_width, color=YELLOW),
            # YellowSquare(grid_x=3, grid_y=2, size=cell_width, color=YELLOW),
            # YellowSquare(grid_x=0, grid_y=3, size=cell_width, color=YELLOW),
            # YellowSquare(grid_x=1, grid_y=3, size=cell_width, color=YELLOW),
            # YellowSquare(grid_x=2, grid_y=3, size=cell_width, color=YELLOW),
            # YellowSquare(grid_x=3, grid_y=3, size=cell_width, color=YELLOW),
            # YellowSquare(grid_x=4, grid_y=3, size=cell_width, color=YELLOW),
        ]
    
    def get_board(self):
        # Create and return the Board instance with the pieces list
        return Board(self.pieces)  # Adjust based on your Board implementation

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
        # Check for completion condition
        target_positions = [(3, 1), (4, 1), (3, 2), (4, 2)]
        if all((self.red_square.grid_x + dx, self.red_square.grid_y + dy) in target_positions
               for dx in range(2) for dy in range(2)):
            print("CONGRATULATIONSSS")
            pygame.quit()
            sys.exit()

    def draw(self):
        self.screen.fill(GRAY)
        pygame.draw.rect(self.screen, WHITE, playable_area)

        for i in range(cols):
            for j in range(rows):
                rect = pygame.Rect(playable_x + i * cell_width, playable_y + j * cell_height, cell_width, cell_height)
                pygame.draw.rect(self.screen, BLUE, rect, 2)

        self.red_square.draw(self.screen)
        for square in self.squares:
            square.draw(self.screen)

        # Draw the move counter
        self.draw_move_counter()

        pygame.display.flip()
        pygame.time.Clock().tick(60)


    def draw_move_counter(self):
        font = pygame.font.SysFont(None, 40)
        move_text = font.render(f'Moves: {self.move_count}', True, (255, 255, 255))  # White text
        self.screen.blit(move_text, (self.screen_width - 150, 20))  # Adjust position as needed

# Class for the red square (occupies 4 cells)
class RedSquare:
    def __init__(self, grid_x, grid_y, size, color):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.size = size
        self.color = color
        self.rects = []  # Store 4 rectangles for 4 grid cells
        self.position = [
            Position(x=grid_x, y=grid_y),
            Position(x=grid_x + 1, y=grid_y),
            Position(x=grid_x, y=grid_y + 1),
            Position(x=grid_x + 1, y=grid_y + 1),
        ]
        self.update_position()

    @classmethod
    def from_piece(cls, piece):
        return cls(piece.grid_x, piece.grid_y, piece.size, piece.color)  # Adjust attributes as necessary

    def update_position(self, position=None):
        if position:
            self.grid_x, self.grid_y = position

        self.rects = [
            pygame.Rect(playable_x + self.grid_x * cell_width,
                        playable_y + self.grid_y * cell_height,
                        cell_width, cell_height),
            pygame.Rect(playable_x + (self.grid_x + 1) * cell_width,
                        playable_y + self.grid_y * cell_height,
                        cell_width, cell_height),
            pygame.Rect(playable_x + self.grid_x * cell_width,
                        playable_y + (self.grid_y + 1) * cell_height,
                        cell_width, cell_height),
            pygame.Rect(playable_x + (self.grid_x + 1) * cell_width,
                        playable_y + (self.grid_y + 1) * cell_height,
                        cell_width, cell_height)
        ]
        self.position = [
            Position(x=self.grid_x, y=self.grid_y),
            Position(x=self.grid_x + 1, y=self.grid_y),
            Position(x=self.grid_x, y=self.grid_y + 1),
            Position(x=self.grid_x + 1, y=self.grid_y + 1),
        ]

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
        
        # Incrementa o contador de movimentos apenas se a posição mudou
        if self.grid_x != prev_x or self.grid_y != prev_y:
            return True  # Retorna True se houve movimento válido

        return False  # Retorna False se o movimento foi bloqueado ou inválido
    
    def possible_moves(self, empty_positions):
        moves = []

        # Left
        if (self.position[0].x - 1, self.position[0].y) in empty_positions and \
           (self.position[2].x - 1, self.position[2].y) in empty_positions:
            moves.append((self.position[0].x - 1, self.position[0].y))

        # Right
        if (self.position[1].x + 1, self.position[1].y) in empty_positions and \
           (self.position[3].x + 1, self.position[3].y) in empty_positions:
            moves.append((self.position[0].x + 1, self.position[0].y))

        # Up
        if (self.position[0].x, self.position[0].y - 1) in empty_positions and \
           (self.position[1].x, self.position[1].y - 1) in empty_positions:
            moves.append((self.position[0].x, self.position[0].y - 1))

        # Down
        if (self.position[2].x, self.position[2].y + 1) in empty_positions and \
           (self.position[3].x, self.position[3].y + 1) in empty_positions:
            moves.append((self.position[0].x, self.position[0].y + 1))
        
        print('possible moves for red: ', moves)
        return moves

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
    

# Class for the yellow squares
class YellowSquare:
    def __init__(self, grid_x, grid_y, size, color):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.size = size
        self.color = color
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        # self.position = [grid_x, grid_y]
        self.position = Position(x=grid_x, y=grid_y)
        self.update_position()

    @classmethod
    def from_piece(cls, piece):
        return cls(piece.grid_x, piece.grid_y, piece.size, piece.color)  # Adjust attributes as necessary

    def update_position(self, position=None):
        if position:
            self.grid_x, self.grid_y = position
        self.rect.x = playable_x + self.grid_x * cell_width
        self.rect.y = playable_y + self.grid_y * cell_height
        self.position = Position(x=self.grid_x, y=self.grid_y)

    def move(self, direction, squares, red_square):
        prev_x, prev_y = self.grid_x, self.grid_y
        moved = False  # Initialize moved to False

        # Determine the potential new position based on the direction
        if direction == 'left' and self.grid_x > 0:
            self.grid_x -= 1
            moved = True  # Mark as moved if we attempt to move left
        elif direction == 'right' and self.grid_x < cols - 1:
            self.grid_x += 1
            moved = True  # Mark as moved if we attempt to move right
        elif direction == 'up' and self.grid_y > 0:
            self.grid_y -= 1
            moved = True  # Mark as moved if we attempt to move up
        elif direction == 'down' and self.grid_y < rows - 1:
            self.grid_y += 1
            moved = True  # Mark as moved if we attempt to move down

        # Now, update the position in the object after potentially moving
        self.update_position()

        # Check for overlap with other squares and the red square
        if moved and not self.prevent_overlap(squares, red_square, prev_x, prev_y):
            # If there was a move but overlap occurs, revert the position
            self.grid_x, self.grid_y = prev_x, prev_y
            self.update_position()  # Update position to revert
            return False  # Return False since the move was blocked

        # If we moved successfully and did not encounter overlap
        return moved  # Return True since there was a valid move

    
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
        print('YELLOW moves')
        print(moves)
        return moves

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


class Board:   # JUST FOR THE SOLVER
    def __init__(self, pieces):
        # pieces is the list of pieces on the board, with the last piece being the main piece (expectation)
        # assert isinstance(pieces[-1], RedSquare)
        self.pieces = pieces
        self.main_piece = pieces[-1]
        self.history = []
        self.history_insert = 0

    @property
    def number_of_steps(self):
        return self.history_insert

    @classmethod
    def from_start_position(cls):
        return cls([
            YellowSquare(0, 0, size=cell_width, color=YELLOW), YellowSquare(1, 0, size=cell_width, color=YELLOW),
            YellowSquare(2, 0, size=cell_width, color=YELLOW), YellowSquare(3, 0, size=cell_width, color=YELLOW),
            RedSquare(1, 0, size=cell_width * 2, color=RED)
        ])


    def empty_positions(self):
        # Initially store all positions on the board
        positions = {Position(x, y) for x in range(5) for y in range(4)}
        # print('positions: ', positions)
        for piece in self.pieces:
            if isinstance(piece, RedSquare):
                for occupied_position in piece.position:
                    positions.remove(occupied_position)
            elif isinstance(piece, YellowSquare):
                positions.remove(piece.position)
        return positions

    @property
    def is_solved(self):
        # Check if main piece is in the expected finish position
        return self.main_piece.position == Position(1, 3)

    def get_piece(self, position):
        # Gets the piece in the specified position
        for piece in self.pieces:
            if position in piece.positions:
                return piece
        return None

    def draw(self, surf, size):
        for piece in self.pieces:
            piece.draw(surf, size)

    def can_move(self, piece, click_position):
        # Click position is one of the empty positions to which the user drags a piece
        empty_positions = self.empty_positions()
        possible_positions, click_positions = piece.possible_moves_ui(empty_positions)
        for possible_pos, click_pos in zip(possible_positions, click_positions):
            if click_position in click_pos:
                return possible_pos
        return None

    def _can_move(self, piece, position):
        # Verify if a piece can move to the specified position
        empty_positions = self.empty_positions()
        possible_positions = piece.possible_moves(empty_positions)
        return position in possible_positions

    def move(self, piece, position):
        print('ERRRRRRRRRRRRRRRRRRORRRR')
        # Current move logic
        assert self._can_move(piece, position)  #IN THE FINAL VERSION KEEP THIS UNCOMMENTED
        # Insert into history the previous position
        self.history = self.history[:self.history_insert]
        self.history.append((piece, piece.position))
        self.history_insert += 1
        piece.update_position(position)

    def history_back(self):
        # Undo the previous move
        if self.history[:self.history_insert]:
            self.history_insert -= 1
            piece, position = self.history[self.history_insert]
            self.history[self.history_insert] = (piece, piece.position)
            piece.update_position(position)

    def history_forward(self):
        # Redo a move
        if self.history_insert < len(self.history):
            piece, position = self.history[self.history_insert]
            self.history[self.history_insert] = (piece, piece.position)
            self.history_insert += 1
            piece.update_position(position)


























# import sys
# import pygame
# from collections import namedtuple
# Position = namedtuple('Position', ['x', 'y'])

# # Define colors (RGB)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# YELLOW = (255, 255, 0)
# BLUE = (0, 0, 255)
# GRAY = (200, 200, 200)

# # Define the playable area
# playable_width = 640   # 128 each block
# playable_height = 512
# playable_x = playable_width / 15
# playable_y = (864 - playable_height) // 2  # Use a fixed height of 864 for the window
# playable_area = pygame.Rect(playable_x, playable_y, playable_width, playable_height)

# # Define grid dimensions
# cols, rows = 5, 4
# cell_width = playable_width // cols
# cell_height = playable_height // rows

# class Game:
#     def __init__(self):
#         # Set window dimensions
#         self.screen_width, self.screen_height = 1536, 864
#         self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
#         pygame.display.set_caption("Klotski Game")

#         # Initialize squares
#         self.red_square = RedSquare(grid_x=0, grid_y=1, size=cell_width * 2, color=RED)  # RedSquare instance
#         self.squares = self.create_yellow_squares()  # YellowSquare instances

#         self.selected_square = None
#         self.start_pos = None  # To track the starting position for swipe
#         self.move_count = 0  # Initialize move counter

#         self.pieces = self.squares + [self.red_square]  # Combine the lists
#         self.board = self.get_board()  # Initialize the board

#     def create_yellow_squares(self):
#         return [
#             YellowSquare(grid_x=0, grid_y=0, size=cell_width, color=YELLOW),
#             YellowSquare(grid_x=1, grid_y=0, size=cell_width, color=YELLOW),
#             YellowSquare(grid_x=2, grid_y=0, size=cell_width, color=YELLOW),
#             YellowSquare(grid_x=3, grid_y=0, size=cell_width, color=YELLOW),
#             # YellowSquare(grid_x=4, grid_y=0, size=cell_width, color=YELLOW),
#             # YellowSquare(grid_x=2, grid_y=1, size=cell_width, color=YELLOW),
#             # YellowSquare(grid_x=2, grid_y=2, size=cell_width, color=YELLOW),
#             # YellowSquare(grid_x=3, grid_y=1, size=cell_width, color=YELLOW),
#             # YellowSquare(grid_x=3, grid_y=2, size=cell_width, color=YELLOW),
#             # YellowSquare(grid_x=0, grid_y=3, size=cell_width, color=YELLOW),
#             # YellowSquare(grid_x=1, grid_y=3, size=cell_width, color=YELLOW),
#             # YellowSquare(grid_x=2, grid_y=3, size=cell_width, color=YELLOW),
#             # YellowSquare(grid_x=3, grid_y=3, size=cell_width, color=YELLOW),
#             # YellowSquare(grid_x=4, grid_y=3, size=cell_width, color=YELLOW),
#         ]
    
#     def get_board(self):
#         # Create and return the Board instance with the pieces list
#         return Board(self.pieces)  # Adjust based on your Board implementation

#     # def get_board(self):
#     #     # Create a list of pieces that includes all yellow squares followed by the red square
#     #     pieces = [
#     #         YellowSquare(grid_x=0, grid_y=0, size=cell_width, color=YELLOW),  # Yellow Square at (0, 0)
#     #         YellowSquare(grid_x=1, grid_y=0, size=cell_width, color=YELLOW),  # Yellow Square at (1, 0)
#     #         YellowSquare(grid_x=2, grid_y=0, size=cell_width, color=YELLOW),  # Yellow Square at (2, 0)
#     #         RedSquare(grid_x=0, grid_y=1, size=cell_width * 2, color=RED)   # Red Square at (0, 1)
#     #     ]
    
#     #     # Create and return the Board instance with the list of pieces
#     #     return Board(pieces)  # Adjust based on your Board implementation

#     # def get_board(self):
#     #     # Create a board representation
#     #     return Board([self.squares, self.red_square])  # Adjust based on your Board implementation

#     def handle_event(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             mouse_pos = pygame.mouse.get_pos()
#             self.start_pos = mouse_pos  # Store the starting position for swipe
            
#             for rect in self.red_square.rects:
#                 if rect.collidepoint(mouse_pos):
#                     self.selected_square = self.red_square
#                     break
#             for square in self.squares:
#                 if square.rect.collidepoint(mouse_pos):
#                     self.selected_square = square
#                     break

#         elif event.type == pygame.MOUSEMOTION and self.selected_square is not None:
#             pass  # You could implement hover effect if desired

#         elif event.type == pygame.MOUSEBUTTONUP and self.selected_square is not None:
#             current_pos = pygame.mouse.get_pos()
#             self.handle_swipe(self.start_pos, current_pos)

#             # Reset the selection after moving
#             self.selected_square = None
#             self.start_pos = None

#     def handle_swipe(self, start_pos, end_pos):
#         dx = end_pos[0] - start_pos[0]
#         dy = end_pos[1] - start_pos[1]

#         direction = None
#         if abs(dx) > abs(dy):  # More horizontal movement
#             if dx > 0:
#                 direction = 'right'
#             else:
#                 direction = 'left'
#         else:  # More vertical movement
#             if dy > 0:
#                 direction = 'down'
#             else:
#                 direction = 'up'

#         if direction:
#             moved = False
#             if isinstance(self.selected_square, RedSquare):
#                 moved = self.selected_square.move(direction, self.squares)  # Now expects a return value
#             elif isinstance(self.selected_square, YellowSquare):
#                 moved = self.selected_square.move(direction, self.squares, self.red_square)  # Now expects a return value
            
#             if moved:  # Only increment if a move was successful
#                 self.move_count += 1  # Increment move counter

#     def update(self):
#         # Check for completion condition
#         target_positions = [(3, 1), (4, 1), (3, 2), (4, 2)]
#         if all((self.red_square.grid_x + dx, self.red_square.grid_y + dy) in target_positions
#                for dx in range(2) for dy in range(2)):
#             print("CONGRATULATIONSSS")
#             pygame.quit()
#             sys.exit()

#     def draw(self):
#         self.screen.fill(GRAY)
#         pygame.draw.rect(self.screen, WHITE, playable_area)

#         for i in range(cols):
#             for j in range(rows):
#                 rect = pygame.Rect(playable_x + i * cell_width, playable_y + j * cell_height, cell_width, cell_height)
#                 pygame.draw.rect(self.screen, BLUE, rect, 2)

#         self.red_square.draw(self.screen)
#         for square in self.squares:
#             square.draw(self.screen)

#         # Draw the move counter
#         self.draw_move_counter()

#         pygame.display.flip()
#         pygame.time.Clock().tick(60)


#     def draw_move_counter(self):
#         font = pygame.font.SysFont(None, 40)
#         move_text = font.render(f'Moves: {self.move_count}', True, (255, 255, 255))  # White text
#         self.screen.blit(move_text, (self.screen_width - 150, 20))  # Adjust position as needed


#     # def play_solution(self, solution_moves):
#     #     """Plays the sequence of moves generated by the BFS solver."""
#     #     for piece, direction in solution_moves:
#     #         # Check which piece is being moved and apply the move
#     #         if piece == self.red_square:
#     #             self.red_square.move(direction, self.squares)
#     #         else:
#     #             piece.move(direction, self.squares, self.red_square)

#     #         # Update display after each move
#     #         self.draw()  # Draw updated positions of all pieces
#     #         pygame.display.flip()  # Refresh the display

#     #         # Add a delay to slow down the visualization
#     #         pygame.time.delay(500)  # 500 ms delay per move (adjust as needed)

#     #         # Optionally, you can check for quit events to exit while visualizing
#     #         for event in pygame.event.get():
#     #             if event.type == pygame.QUIT:
#     #                 pygame.quit()
#     #                 return

# # Class for the red square (occupies 4 cells)
# class RedSquare:
#     def __init__(self, grid_x, grid_y, size, color):
#         self.grid_x = grid_x
#         self.grid_y = grid_y
#         self.size = size
#         self.color = color
#         self.rects = []  # Store 4 rectangles for 4 grid cells
#         # self.position = [(grid_x, grid_y), (grid_x + 1, grid_y), 
#         #                  (grid_x, grid_y + 1), (grid_x + 1, grid_y + 1)]  # NAO DA [] NEM ()
#         self.position = [
#             Position(x=grid_x, y=grid_y),
#             Position(x=grid_x + 1, y=grid_y),
#             Position(x=grid_x, y=grid_y + 1),
#             Position(x=grid_x + 1, y=grid_y + 1),
#         ]
#         self.update_position()

#     @classmethod
#     def from_piece(cls, piece):
#         return cls(piece.grid_x, piece.grid_y, piece.size, piece.color)  # Adjust attributes as necessary

#     def update_position(self, position=None):
#         if position:
#             self.grid_x, self.grid_y = position

#         self.rects = [
#             pygame.Rect(playable_x + self.grid_x * cell_width,
#                         playable_y + self.grid_y * cell_height,
#                         cell_width, cell_height),
#             pygame.Rect(playable_x + (self.grid_x + 1) * cell_width,
#                         playable_y + self.grid_y * cell_height,
#                         cell_width, cell_height),
#             pygame.Rect(playable_x + self.grid_x * cell_width,
#                         playable_y + (self.grid_y + 1) * cell_height,
#                         cell_width, cell_height),
#             pygame.Rect(playable_x + (self.grid_x + 1) * cell_width,
#                         playable_y + (self.grid_y + 1) * cell_height,
#                         cell_width, cell_height)
#         ]
#         self.position = [
#             Position(x=self.grid_x, y=self.grid_y),
#             Position(x=self.grid_x + 1, y=self.grid_y),
#             Position(x=self.grid_x, y=self.grid_y + 1),
#             Position(x=self.grid_x + 1, y=self.grid_y + 1),
#         ]

#     def move(self, direction, squares):
#         prev_x, prev_y = self.grid_x, self.grid_y

#         if direction == 'left' and self.grid_x > 0:
#             self.grid_x -= 1
#         elif direction == 'right' and self.grid_x < cols - 2:
#             self.grid_x += 1
#         elif direction == 'up' and self.grid_y > 0:
#             self.grid_y -= 1
#         elif direction == 'down' and self.grid_y < rows - 2:
#             self.grid_y += 1

#         self.update_position()
#         moved = self.prevent_overlap(squares, prev_x, prev_y)
        
#         # Incrementa o contador de movimentos apenas se a posição mudou
#         if self.grid_x != prev_x or self.grid_y != prev_y:
#             return True  # Retorna True se houve movimento válido

#         return False  # Retorna False se o movimento foi bloqueado ou inválido
    
#     def possible_moves(self, empty_positions):
#         moves = []
#         # Check all four directions for the 2x2 RedSquare
#         # print('self.position[0].x: ')
#         # print(self.position[0].x)
#         # print('self.position')
#         # print(self.position)
#         # print('empty_positions')
#         # print(empty_positions)

#         # Left
#         if (self.position[0].x - 1, self.position[0].y) in empty_positions and \
#            (self.position[2].x - 1, self.position[2].y) in empty_positions:
#             moves.append((self.position[0].x - 1, self.position[0].y))

#         # Right
#         if (self.position[1].x + 1, self.position[1].y) in empty_positions and \
#            (self.position[3].x + 1, self.position[3].y) in empty_positions:
#             moves.append((self.position[0].x + 1, self.position[0].y))

#         # Up
#         if (self.position[0].x, self.position[0].y - 1) in empty_positions and \
#            (self.position[1].x, self.position[1].y - 1) in empty_positions:
#             moves.append((self.position[0].x, self.position[0].y - 1))

#         # Down
#         if (self.position[2].x, self.position[2].y + 1) in empty_positions and \
#            (self.position[3].x, self.position[3].y + 1) in empty_positions:
#             moves.append((self.position[0].x, self.position[0].y + 1))
        
#         # print('possible moves for red: ', moves)
#         return moves

#     def prevent_overlap(self, squares, prev_x, prev_y):
#         red_positions = [(self.grid_x, self.grid_y), (self.grid_x + 1, self.grid_y),
#                          (self.grid_x, self.grid_y + 1), (self.grid_x + 1, self.grid_y + 1)]

#         for square in squares:
#             yellow_pos = (square.grid_x, square.grid_y)
#             if yellow_pos in red_positions:
#                 self.grid_x, self.grid_y = prev_x, prev_y
#                 self.update_position()
#                 return False  # Return False indicating an overlap occurred
#         return True  # Return True indicating no overlap occurred

#     def draw(self, surface):
#         for rect in self.rects:
#             pygame.draw.rect(surface, self.color, rect)

#         main_rect = pygame.Rect(
#             self.rects[0].x,
#             self.rects[0].y,
#             2 * self.rects[0].width,
#             2 * self.rects[0].height
#         )
#         pygame.draw.rect(surface, (0, 0, 0), main_rect, 2)
    
#     # def possible_moves(self, empty_positions):
#     #     moves = []
#     #     # Check all four directions
#     #     if (self.grid_x - 1, self.grid_y) in empty_positions:  # Left
#     #         moves.append((self.grid_x - 1, self.grid_y))
#     #     if (self.grid_x + 2, self.grid_y) in empty_positions:  # Right
#     #         moves.append((self.grid_x + 2, self.grid_y))
#     #     if (self.grid_x, self.grid_y - 1) in empty_positions:  # Up
#     #         moves.append((self.grid_x, self.grid_y - 1))
#     #     if (self.grid_x, self.grid_y + 2) in empty_positions:  # Down
#     #         moves.append((self.grid_x, self.grid_y + 2))
#     #     return moves

# # Class for the yellow squares
# class YellowSquare:
#     def __init__(self, grid_x, grid_y, size, color):
#         self.grid_x = grid_x
#         self.grid_y = grid_y
#         self.size = size
#         self.color = color
#         self.rect = pygame.Rect(0, 0, self.size, self.size)
#         # self.position = [grid_x, grid_y]
#         self.position = Position(x=grid_x, y=grid_y)
#         self.update_position()

#     @classmethod
#     def from_piece(cls, piece):
#         return cls(piece.grid_x, piece.grid_y, piece.size, piece.color)  # Adjust attributes as necessary

#     def update_position(self, position=None):
#         if position:
#             self.grid_x, self.grid_y = position
#         self.rect.x = playable_x + self.grid_x * cell_width
#         self.rect.y = playable_y + self.grid_y * cell_height
#         self.position = Position(x=self.grid_x, y=self.grid_y)

#     def move(self, direction, squares, red_square):
#         prev_x, prev_y = self.grid_x, self.grid_y
#         moved = False  # Initialize moved to False

#         # Determine the potential new position based on the direction
#         if direction == 'left' and self.grid_x > 0:
#             self.grid_x -= 1
#             moved = True  # Mark as moved if we attempt to move left
#         elif direction == 'right' and self.grid_x < cols - 1:
#             self.grid_x += 1
#             moved = True  # Mark as moved if we attempt to move right
#         elif direction == 'up' and self.grid_y > 0:
#             self.grid_y -= 1
#             moved = True  # Mark as moved if we attempt to move up
#         elif direction == 'down' and self.grid_y < rows - 1:
#             self.grid_y += 1
#             moved = True  # Mark as moved if we attempt to move down

#         # Now, update the position in the object after potentially moving
#         self.update_position()

#         # Check for overlap with other squares and the red square
#         if moved and not self.prevent_overlap(squares, red_square, prev_x, prev_y):
#             # If there was a move but overlap occurs, revert the position
#             self.grid_x, self.grid_y = prev_x, prev_y
#             self.update_position()  # Update position to revert
#             return False  # Return False since the move was blocked

#         # If we moved successfully and did not encounter overlap
#         return moved  # Return True since there was a valid move


#     # def move(self, direction, squares, red_square):
#     #     prev_x, prev_y = self.grid_x, self.grid_y

#     #     if direction == 'left' and self.grid_x > 0:
#     #         self.grid_x -= 1
#     #     elif direction == 'right' and self.grid_x < cols - 1:
#     #         self.grid_x += 1
#     #     elif direction == 'up' and self.grid_y > 0:
#     #         self.grid_y -= 1
#     #     elif direction == 'down' and self.grid_y < rows - 1:
#     #         self.grid_y += 1

#     #     self.update_position()
#     #     moved = self.prevent_overlap(squares, red_square, prev_x, prev_y)

#     #     # Incrementa o contador de movimentos apenas se a posição mudou
#     #     if moved and (self.grid_x != prev_x or self.grid_y != prev_y):
#     #         return True  # Retorna True se houve movimento válido

#     #     return False  # Retorna False se o movimento foi bloqueado ou inválido
    
#     def possible_moves(self, empty_positions):
#         moves = []
#         # Check all four directions
#         if (self.grid_x - 1, self.grid_y) in empty_positions:  # Left
#             moves.append((self.grid_x - 1, self.grid_y))
#         if (self.grid_x + 1, self.grid_y) in empty_positions:  # Right
#             moves.append((self.grid_x + 1, self.grid_y))
#         if (self.grid_x, self.grid_y - 1) in empty_positions:  # Up
#             moves.append((self.grid_x, self.grid_y - 1))
#         if (self.grid_x, self.grid_y + 1) in empty_positions:  # Down
#             moves.append((self.grid_x, self.grid_y + 1))
#         return moves

#     def prevent_overlap(self, squares, red_square, prev_x, prev_y):
#         # Check for collision with each other yellow square
#         for square in squares:
#             if square != self and self.rect.colliderect(square.rect):
#                 self.grid_x, self.grid_y = prev_x, prev_y
#                 self.update_position()
#                 return False

#         # Check for collision with the red square's cells
#         red_positions = [(red_square.grid_x, red_square.grid_y), (red_square.grid_x + 1, red_square.grid_y),
#                          (red_square.grid_x, red_square.grid_y + 1), (red_square.grid_x + 1, red_square.grid_y + 1)]
#         yellow_pos = (self.grid_x, self.grid_y)

#         if yellow_pos in red_positions:
#             self.grid_x, self.grid_y = prev_x, prev_y
#             self.update_position()
        
#         return True

#     def draw(self, surface):
#         pygame.draw.rect(surface, self.color, self.rect)
#         pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

#     # def possible_moves(self, empty_positions):
#     #     moves = []
#     #     # Check all four directions
#     #     if (self.grid_x - 1, self.grid_y) in empty_positions:  # Left
#     #         moves.append((self.grid_x - 1, self.grid_y))
#     #     if (self.grid_x + 1, self.grid_y) in empty_positions:  # Right
#     #         moves.append((self.grid_x + 1, self.grid_y))
#     #     if (self.grid_x, self.grid_y - 1) in empty_positions:  # Up
#     #         moves.append((self.grid_x, self.grid_y - 1))
#     #     if (self.grid_x, self.grid_y + 1) in empty_positions:  # Down
#     #         moves.append((self.grid_x, self.grid_y + 1))
#     #     return moves


# class Board:   # JUST FOR THE SOLVER
#     def __init__(self, pieces):
#         # pieces is the list of pieces on the board, with the last piece being the main piece (expectation)
#         # assert isinstance(pieces[-1], RedSquare)
#         self.pieces = pieces
#         self.main_piece = pieces[-1]
#         self.history = []
#         self.history_insert = 0

#     @property
#     def number_of_steps(self):
#         return self.history_insert

#     @classmethod
#     def from_start_position(cls):
#         return cls([
#             YellowSquare(0, 0, size=cell_width, color=YELLOW), YellowSquare(1, 0, size=cell_width, color=YELLOW),
#             YellowSquare(2, 0, size=cell_width, color=YELLOW), YellowSquare(3, 0, size=cell_width, color=YELLOW),
#             RedSquare(1, 0, size=cell_width * 2, color=RED)
#         ])

#     # @classmethod
#     # def from_pieces(cls, pieces: tuple):
#     #     return cls(pieces)

#     # @classmethod
#     # def from_board(cls, _board):
#     #     pieces = []
#     #     for piece in _board.pieces:
#     #         if isinstance(piece, YellowSquare):
#     #             pieces.append(YellowSquare.from_piece(piece))
#     #         elif isinstance(piece, RedSquare):
#     #             pieces.append(RedSquare.from_piece(piece))
#     #         else:
#     #             raise NotImplementedError("Unknown piece type")
#     #     # return cls(pieces)
#     #     return cls.from_pieces(tuple(pieces))


#     def empty_positions(self):
#         # Initially store all positions on the board
#         positions = {Position(x, y) for x in range(5) for y in range(4)}
#         # print('positions: ', positions)
#         for piece in self.pieces:
#             if isinstance(piece, RedSquare):
#                 for occupied_position in piece.position:
#                     # print('ocuppied positionsRED: ', occupied_position)
#                     # print('ocuppied positionsRED: ', type(occupied_position))
#                     positions.remove(occupied_position)
#             else:
#                 # Remove positions occupied by each of the pieces
#                 # print('ocuppied positionsYELLOW: ', piece.position)
#                 # print('ocuppied positionsYELLOW: ', type(piece.position))
#                 positions.remove(piece.position)

#         # assert len(positions) == 2   # NUM JOGO NORMAL SO HAVERIAM 2 POSICOES LIVRES, MAS AGORA EM FASE DE TESTES NÃO

#         # Positions with no piece are empty
#         # print ('positions left: ', positions)
#         return positions

#     @property
#     def is_solved(self):
#         # Check if main piece is in the expected finish position
#         return self.main_piece.position == Position(1, 3)

#     def get_piece(self, position):
#         # Gets the piece in the specified position
#         for piece in self.pieces:
#             if position in piece.positions:
#                 return piece
#         return None

#     def draw(self, surf, size):
#         for piece in self.pieces:
#             piece.draw(surf, size)

#     def can_move(self, piece, click_position):
#         # Click position is one of the empty positions to which the user drags a piece
#         empty_positions = self.empty_positions()
#         possible_positions, click_positions = piece.possible_moves_ui(empty_positions)
#         for possible_pos, click_pos in zip(possible_positions, click_positions):
#             if click_position in click_pos:
#                 return possible_pos
#         return None

#     def _can_move(self, piece, position):
#         # Verify if a piece can move to the specified position
#         empty_positions = self.empty_positions()
#         possible_positions = piece.possible_moves(empty_positions)
#         return position in possible_positions

#     def move(self, piece, position):
#         print('ERRRRRRRRRRRRRRRRRRORRRR')
#         # Current move logic
#         assert self._can_move(piece, position)  #IN THE FINAL VERSION KEEP THIS UNCOMMENTED
#         # Insert into history the previous position
#         self.history = self.history[:self.history_insert]
#         self.history.append((piece, piece.position))
#         self.history_insert += 1
#         piece.update_position(position)
    

#     # def move(self, piece, position):
#     #     # Move piece to the specified position
#     #     # assert self._can_move(piece, position)
#     #     # Insert into history the previous position
#     #     self.history = self.history[:self.history_insert]
#     #     self.history.append((piece, piece.position))
#     #     self.history_insert += 1
#     #     piece.update_position(position)

#     # def move(self, piece, position):
#     #     # print('pppppppppppiece')
#     #     # print(piece)
#     #     # print('positionnnnnnnnnn')
#     #     # print(position)
#     #     pieces = tuple(
#     #         _piece if _piece != piece
#     #         else piece.update_position(position)
#     #         for _piece in self.pieces
#     #     )
#     #     return Board.from_pieces(pieces)




#     # def potential_moves(self):
#     #     # Generate a list of possible moves for all pieces
#     #     moves = []
#     #     empty_positions = self.empty_positions()
#     #     for piece in self.pieces:
#     #         for position in piece.possible_moves(empty_positions):
#     #             moves.append((piece, position))
#     #     return moves

#     def history_back(self):
#         # Undo the previous move
#         if self.history[:self.history_insert]:
#             self.history_insert -= 1
#             piece, position = self.history[self.history_insert]
#             self.history[self.history_insert] = (piece, piece.position)
#             piece.update_position(position)

#     def history_forward(self):
#         # Redo a move
#         if self.history_insert < len(self.history):
#             piece, position = self.history[self.history_insert]
#             self.history[self.history_insert] = (piece, piece.position)
#             self.history_insert += 1
#             piece.update_position(position)

#     # def map_piece(self, piece, _board):
#     #     # Returns the corresponding piece in another board
#     #     return _board.pieces[self.pieces.index(piece)]
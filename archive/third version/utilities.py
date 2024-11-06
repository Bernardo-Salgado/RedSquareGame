# import pygame

# # Define colors (RGB)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# YELLOW = (255, 255, 0)
# BLUE = (0, 0, 255)
# GRAY = (200, 200, 200)

# # Define the playable area
# playable_width = 1000
# playable_height = 800
# playable_x = playable_width / 15
# playable_y = (864 - playable_height) // 2  # Use a fixed height of 864 for the window
# playable_area = pygame.Rect(playable_x, playable_y, playable_width, playable_height)

# # Define grid dimensions
# cols, rows = 5, 4
# cell_width = playable_width // cols
# cell_height = playable_height // rows

# # Class for the red square (occupies 4 cells)
# class RedSquare:
#     def __init__(self, grid_x, grid_y, size, color):
#         self.grid_x = grid_x
#         self.grid_y = grid_y
#         self.size = size
#         self.color = color
#         self.rects = []  # Store 4 rectangles for 4 grid cells
#         self.update_position()

#     def update_position(self):
#         # Clear the existing rects
#         self.rects = []

#         # Define 4 rects based on the grid for the red square occupying 4 cells
#         self.rects.append(pygame.Rect(playable_x + self.grid_x * cell_width,
#                                       playable_y + self.grid_y * cell_height,
#                                       cell_width, cell_height))
#         self.rects.append(pygame.Rect(playable_x + (self.grid_x + 1) * cell_width,
#                                       playable_y + self.grid_y * cell_height,
#                                       cell_width, cell_height))
#         self.rects.append(pygame.Rect(playable_x + self.grid_x * cell_width,
#                                       playable_y + (self.grid_y + 1) * cell_height,
#                                       cell_width, cell_height))
#         self.rects.append(pygame.Rect(playable_x + (self.grid_x + 1) * cell_width,
#                                       playable_y + (self.grid_y + 1) * cell_height,
#                                       cell_width, cell_height))

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
#         if moved and (self.grid_x != prev_x or self.grid_y != prev_y):
#             return True  # Retorna True se houve movimento válido

#         return False  # Retorna False se o movimento foi bloqueado ou inválido
    

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

# # Class for the yellow squares
# class YellowSquare:
#     def __init__(self, grid_x, grid_y, size, color):
#         self.grid_x = grid_x
#         self.grid_y = grid_y
#         self.size = size
#         self.color = color
#         self.rect = pygame.Rect(0, 0, self.size, self.size)
#         self.update_position()

#     def update_position(self):
#         self.rect.x = playable_x + self.grid_x * cell_width
#         self.rect.y = playable_y + self.grid_y * cell_height

#     def move(self, direction, squares, red_square):
#         prev_x, prev_y = self.grid_x, self.grid_y
#         moved = False

#         if direction == 'left' and self.grid_x > 0:
#             self.grid_x -= 1
#         elif direction == 'right' and self.grid_x < cols - 1:
#             self.grid_x += 1
#         elif direction == 'up' and self.grid_y > 0:
#             self.grid_y -= 1
#         elif direction == 'down' and self.grid_y < rows - 1:
#             self.grid_y += 1

#         self.update_position()
#         moved = self.prevent_overlap(squares, red_square, prev_x, prev_y)
        
#         # Incrementa o contador de movimentos apenas se a posição mudou
#         if moved and (self.grid_x != prev_x or self.grid_y != prev_y):
#             return True  # Retorna True se houve movimento válido

#         return False  # Retorna False se o movimento foi bloqueado ou inválido

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

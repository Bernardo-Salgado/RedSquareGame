import pygame
import sys

# Define configuration variables
setup_cols = 6
setup_rows = 4


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 55)
        self.options = ["Start", "Solve", "Board size: 4 x 6", "Music: ON", "Exit"]
        self.selected_option = 0

        # Load the image
        self.menu_image = pygame.image.load('img/menuimg.png')
        self.menu_image = pygame.transform.scale(self.menu_image, (1920, 1080))  # Fitting the screen

        # Define the board sizes
        self.board_sizes = [(6, 4), (10, 6), (12, 6)]
        self.current_board_size_index = 0

        # Music state
        self.music_on = True  # Music starts as ON

    def draw(self):
        self.screen.fill((255, 222, 89))  # Fill with yellow
        # Blit the image
        self.screen.blit(self.menu_image, (0, 0))  # Draw the image at the top-left corner

        for i, option in enumerate(self.options):
            if i == 2:  # Update the board size option text
                cols, rows = self.board_sizes[self.current_board_size_index]
                option = f"Board size: {cols} x {rows}"
            elif i == 3:  # Update the music option text
                option = "Music: ON" if self.music_on else "Music: OFF"

            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 650 + i * 60))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            for i in range(len(self.options)):
                # Check if mouse is hovering over an option
                if 650 + i * 60 - 30 < mouse_y < 650 + i * 60 + 30:  # Adjust for height of text
                    self.selected_option = i
                    break

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.selected_option == 0:  # Start
                    return "start"
                elif self.selected_option == 1:  # Solve
                    return "solve"
                elif self.selected_option == 2:  # Board size
                    # Cycle through board sizes
                    self.current_board_size_index = (self.current_board_size_index + 1) % len(self.board_sizes)
                    return None  # No action needed, just update the display
                elif self.selected_option == 3:  # Music
                    self.music_on = not self.music_on  # Toggle music state
                    if self.music_on:
                        pygame.mixer.music.set_volume(1.0)  # Set volume to max
                    else:
                        pygame.mixer.music.set_volume(0.0)  # Mute music
                    return None  # No action needed, just update the display
                elif self.selected_option == 4:  # Exit
                    pygame.quit()
                    sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:  # Start
                    return "start"
                elif self.selected_option == 1:  # Solve
                    return "solve"
                elif self.selected_option == 2:  # Board size
                    # Cycle through board sizes
                    self.current_board_size_index = (self.current_board_size_index + 1) % len(self.board_sizes)
                    return None  # No action needed, just update the display
                elif self.selected_option == 3:  # Music
                    self.music_on = not self.music_on  # Toggle music state
                    if self.music_on:
                        pygame.mixer.music.set_volume(1.0)  # Set volume to max
                    else:
                        pygame.mixer.music.set_volume(0.0)  # Mute music
                    return None  # No action needed, just update the display
                elif self.selected_option == 4:  # Exit
                    pygame.quit()
                    sys.exit()

        return None

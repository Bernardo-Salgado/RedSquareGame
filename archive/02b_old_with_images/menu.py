import pygame
import sys

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 55)
        self.options = ["Start", "Solve", "Exit"]
        self.selected_option = 0

# <Michal> [loading the menu image]---------------------------------------------------
        # Load the image
        self.menu_image = pygame.image.load('img/menuimg.png')
        self.menu_image = pygame.transform.scale(self.menu_image, (self.screen.get_width(), self.screen.get_height()))  # Fitting the screen

# </Michal> --------------------------------------------------------------------------
    def draw(self):
# <Michal> [changed the colour and added the image]------------------------------------
        self.screen.fill((255, 222, 89))  # Fill with yellow


        # Blit the image
        self.screen.blit(self.menu_image, (0, 0))  # Draw the image at the top-left corner
# </Michal> ---------------------------------------------------------------------------

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            text_surface = self.font.render(option, True, color)
# <Michal> [changed the positioning of the text from 200 to 650]----------------------------------
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 650 + i * 60))
# </Michal> --------------------------------------------------------------------------------------
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            for i in range(len(self.options)):
                # Check if mouse is hovering over an option
# <Michal> [changed the value from 200 to 650 to modify positioning]-------------
                if 650 + i * 60 - 30 < mouse_y < 650 + i * 60 + 30:  # Adjust for height of text
# </Michal> ---------------------------------------------------------------------
                    self.selected_option = i
                    break
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.selected_option == 0:  # Start
                    return "start"
                elif self.selected_option == 1:  # Solve
                    return "solve"  # Added solve option here
                elif self.selected_option == 2:  # Exit
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
                    return "solve"  # Added solve option here
                elif self.selected_option == 2:  # Exit
                    pygame.quit()
                    sys.exit()

        return None

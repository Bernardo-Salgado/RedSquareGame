# [5/5 END.PY]

import pygame
import sys


class EndMenu:
    def __init__(self, screen, game):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 55)
        self.options = ["Back to Menu", "Exit"]
        self.selected_option = 0
        self.game = game  # Store the Game instance

    def show_end_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                action = self.handle_event(event)
                if action == "back_to_menu":
                    return "back_to_menu"  # Return to indicate back to menu
                elif action == "exit":
                    pygame.quit()
                    sys.exit()

            self.draw()

    def draw(self):
        self.screen.fill((169, 169, 169))  # Fill with grey

        # Draw the solved message using move_count from the Game instance
        if (self.game.move_count == 0):
            solved_text = 'Unsolved!'
            text_surface = self.font.render(solved_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 100))  # Adjust the position as needed
            self.screen.blit(text_surface, text_rect)
        else:
            solved_text = f"Solved in {self.game.move_count} moves"
            text_surface = self.font.render(solved_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 100))  # Adjust here too the position as needed
            self.screen.blit(text_surface, text_rect)

        # Draw the options
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 200 + i * 60))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            for i in range(len(self.options)):
                if 200 + i * 60 - 30 < mouse_y < 200 + i * 60 + 30:
                    self.selected_option = i
                    break

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.selected_option == 0:  # Back to Menu
                    return "back_to_menu"
                elif self.selected_option == 1:  # Exit
                    pygame.quit()
                    sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:  # Back to Menu
                    return "back_to_menu"
                elif self.selected_option == 1:  # Exit
                    pygame.quit()
                    sys.exit()

        return None

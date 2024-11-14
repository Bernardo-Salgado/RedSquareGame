import pygame
import sys
from game import Game
from solver import Solver


def main():
    pygame.init()

    screen_width, screen_height = 1536, 864
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Red Duck Game")

    menu = Menu(screen)
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            menu_action = menu.handle_event(event)
            if menu_action == "start":
                game.reset()  # Reset the game state
                game.run()

            elif menu_action == "solve":
                print('Solving...')
                game.reset()  # Reset the game state before solving
                solver = Solver(game)
                solver.greedy_search()  # You can uncomment other solvers as needed

            elif menu_action is None:
                pass

        menu.draw()


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 55)
        self.options = ["Start", "Solve", "Exit"]
        self.selected_option = 0

    def draw(self):
        self.screen.fill((169, 169, 169))  # Fill with grey

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
                # Check if mouse is hovering over an option
                if 200 + i * 60 - 30 < mouse_y < 200 + i * 60 + 30:  # Adjust for height of text
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

if __name__ == "__main__":
    main()

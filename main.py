import pygame
import sys
from menu import Menu
from game import Game
from solver import Solver

def main():
    pygame.init()

    screen_width, screen_height = 1536, 864
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Klotski Game")

    menu = Menu(screen)
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            menu_action = menu.handle_event(event)
            if menu_action == "start":
                # Run the game (player solver)
                game.run()

            elif menu_action == "solve":
                print('Solving...')
                # Initialize the game and the solver
                solver = Solver(game)
                # UNCOMMENT A SPECIFIC SOLVER

                # Run the BFS solver to find the solution path
                solver.bfs()

                # Run the DFS solver to find the solution path
                #max_depth = 6
                #solver.dfs(max_depth)

                # Run the IDS solver to find the solution path
                # solver.ids()

                # Run the greedy solver to find the solution path with different heuristics
                # solver.greedy_search(solver.manhattan)
                #solver.greedy_search(solver.euclidean)
                # solver.greedy_search(solver.manhattan)

                # Run A* solver to find the solution path with different heuristics
                # solver.a_star_search(solver.manhattan)
                # solver.a_star_search(solver.euclidean)
                # solver.a_star_search(solver.chebyshev)

            elif menu_action is None:
                pass

        menu.draw()

if __name__ == "__main__":
    main()
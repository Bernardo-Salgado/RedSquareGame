# [2/5 MENU.PY]

import pygame
import sys
from game import Game
from solver import Solver

# Define configuration variables
setup_cols = 6
setup_rows = 4


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 35)
        self.options = ["Start", "BFS", "DFS", "IDS", "Greedy Search", "A*", "Board size: 4 x 6", "Music: ON", "Exit"]
        self.greedy_options = ["Greedy Search with Manhattan", "Greedy Search with Euclidean", "Greedy Search with Chebyshev"]
        self.astar_options = ["A* with Manhattan", "A* with Euclidean", "A* with Chebyshev"]
        self.selected_option = 0

        # Load the image
        self.menu_image = pygame.image.load('img/menuimg.png')
        self.menu_image = pygame.transform.scale(self.menu_image, (1920, 1080))  # Fitting the screen

        # Define the board sizes
        self.board_sizes = [(6, 4), (10, 6), (12, 6)]
        self.current_board_size_index = 0

        # Music state
        self.music_on = True  # Music starts as ON

        # Input fields for max_depth of DFS

        self.max_depth = None  # Variable to store max_depth input

        # self.input_active = False  # Flag to track if input is active

        # # self.input_box = pygame.Rect(self.screen.get_width() // 2 - 100, 650 + 3 * 48 - 20, 200, 45)  # Position of the input box

        self.input_text = ""  # To store the input text

    def draw(self):
        self.screen.fill((255, 222, 89))  # Fill with yellow
        # Blit the image
        self.screen.blit(self.menu_image, (0, 0))  # Draw the image at the top-left corner
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # print("pygame.mouse.get_posssssssssssssss: ", pygame.mouse.get_pos())

        for i, option in enumerate(self.options):
            # Draw input popup for DFS max_depth

            if i == 2 and self.selected_option == 2: # If DFS is selected and input is active

                self.draw_input_popup(mouse_x, mouse_y)
            
            elif i == 4 and self.selected_option == 4:  # Greedy Search
                self.draw_popup(self.screen.get_width() // 2 + 150, 650 + i * 48 - 20, self.greedy_options, mouse_x, mouse_y)
            elif i == 5 and self.selected_option == 5:  # A*
                self.draw_popup(self.screen.get_width() // 2 + 150, 650 + i * 48 - 20, self.astar_options, mouse_x, mouse_y)
            elif i == 6:  # Update the board size option text
                cols, rows = self.board_sizes[self.current_board_size_index]
                option = f"Board size: {cols} x {rows}"
            elif i == 7:  # Update the music option text
                option = "Music: ON" if self.music_on else "Music: OFF"

            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 650 + i * 48))
            self.screen.blit(text_surface, text_rect)
        pygame.display.flip()


    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            for i in range(len(self.options)):
                # Check if mouse is hovering over an option
                if (self.screen.get_width() // 2 - 100 < mouse_x < self.screen.get_width() // 2 + 100 and 
                        650 + i * 48 - 20 < mouse_y < 650 + i * 48 + 20):  # Adjust for height of text
                    self.selected_option = i
                    break

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.selected_option == 0:  # Start
                    return "start"
                elif self.selected_option == 1:  # BFS
                    return "BFS"
                # elif self.selected_option == 2:  # DFS


                    # if event.type == pygame.KEYDOWN:
                    #     if event.key == pygame.K_BACKSPACE:
                    #         self.input_text = self.input_text[:-1]  # Remove last character
                    #     elif event.unicode.isdigit():
                    #         self.input_text += event.unicode  # Add digit to input text

                    # # Check if the submit button for DFS was clicked
                    # submit_button_rect = pygame.Rect(self.screen.get_width() // 2 + 200, 650 + 2 * 48 + 90, 100, 40)
                    # if submit_button_rect.collidepoint(event.pos):  # Submit button click
                    #     try:
                    #         # Parse the input value as an integer and update max_depth
                    #         self.max_depth = int(self.input_text)
                    #         print(f"Max Depth for DFS: {self.max_depth}")  # Debug print
                    #         return "DFS"  # Trigger DFS action
                    #     except ValueError:
                    #         print("Invalid input. Please enter an integer.")


                elif self.selected_option == 3:  # IDS
                    return "IDS"
                

                elif self.selected_option == 4:  # Greedy Search, handle nested options

                    # Check which greedy option is selected

                    for i, option in enumerate(self.greedy_options):

                        option_rect = pygame.Rect(self.screen.get_width() // 2 + 150, 650 + 4 * 48 - 20 + i * 45, 369, 45)

                        if option_rect.collidepoint(event.pos):  # Check if mouse is over a specific option
                            print (option)
                            return option  # Return the specific greedy search option selected

                elif self.selected_option == 5:  # A*, handle nested options

                    # Check which A* option is selected

                    for i, option in enumerate(self.astar_options):

                        option_rect = pygame.Rect(self.screen.get_width() // 2 + 150, 650 + 5 * 48 - 20 + i * 45, 223, 45)

                        if option_rect.collidepoint(event.pos):  # Check if mouse is over a specific option

                            print (option)
                            return option  # Return the specific A* option selected
                        

                elif self.selected_option == 6:  # Board size
                    # Cycle through board sizes
                    self.current_board_size_index = (self.current_board_size_index + 1) % len(self.board_sizes)
                    return None  # No action needed, just update the display
                elif self.selected_option == 7:  # Music
                    self.music_on = not self.music_on  # Toggle music state
                    if self.music_on:
                        pygame.mixer.music.set_volume(1.0)  # Set volume to max
                    else:
                        pygame.mixer.music.set_volume(0.0)  # Mute music
                    return None  # No action needed, just update the display
                elif self.selected_option == 8:  # Exit
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
                elif self.selected_option == 1:  # BFS
                    return "BFS"
                # elif self.selected_option == 2:  # DFS

                #     if event.type == pygame.KEYDOWN:
                #         if event.key == pygame.K_BACKSPACE:
                #             self.input_text = self.input_text[:-1]  # Remove last character
                #         elif event.unicode.isdigit():
                #             self.input_text += event.unicode  # Add digit to input text

                #     # Check if the submit button for DFS was clicked
                #     submit_button_rect = pygame.Rect(self.screen.get_width() // 2 + 200, 650 + 2 * 48 + 90, 100, 40)
                #     if submit_button_rect.collidepoint(event.pos):  # Submit button click
                #         try:
                #             cols, rows = self.board_sizes[self.current_board_size_index]
                #             game = Game(cols, rows)  # Pass the selected board size to the Game instance

                #             self.show_solving_message() # Solving window

                #             # Initialize the game and the solver
                #             solver = Solver(game)

                #             max_depth = self.get_dfs_depth()
                #             # Run the BFS solver to find the solution path
                #             solver.track_solver(lambda: solver.dfs(max_depth), 'BFS')

                #         except ValueError:
                #             print("Invalid input. Please enter an integer.")
                    
                    # if event.type == pygame.KEYDOWN:
                    #     if event.key == pygame.K_RETURN:
                    #         if self.dfs_depth_input:  # If there's input
                    #             self.current_action = "DFS"
                    #             return self.current_action
                    #     elif event.key == pygame.K_BACKSPACE:
                    #         self.dfs_depth_input = self.dfs_depth_input[:-1]
                    #     else:
                    #         self.dfs_depth_input += event.unicode

                        # if event.type == pygame.KEYDOWN:
                        #     if event.key == pygame.K_BACKSPACE:
                        #         self.input_text = self.input_text[:-1]  # Remove last character
                        #     elif event.key == pygame.K_RETURN:
                        #         try:
                        #             # Parse the input value as an integer and update max_depth
                        #             self.max_depth = int(self.input_text)
                        #             print(f"Max Depth for DFS: {self.max_depth}")  # Debug print
                        #             return "DFS"
                        #             # self.input_active = False  # Disable input after entering value
                        #             # return self.max_depth  # Return the max_depth to use in the DFS algorithm
                        #         except ValueError:
                        #             print("Invalid input. Please enter an integer.")
                        #     elif event.unicode.isdigit():
                        #         self.input_text += event.unicode  # Add digit to input text
                    
                    return "DFS"
                    
                    
                    # if not self.input_active:

                    #     self.input_active = True  # Enable input for max_depth

                    # else:
                    #     print("self.get_dfs_depth()MMMMMMMMMMMMM: ", self.get_dfs_depth())
                    #     return self.get_dfs_depth()  # Return the max_depth after input is given
                    
                elif self.selected_option == 3:  # IDS
                    return "IDS"
                

                elif self.selected_option == 4:  # Greedy Search, handle nested options

                    # Check which greedy option is selected

                    for i, option in enumerate(self.greedy_options):

                        option_rect = pygame.Rect(self.screen.get_width() // 2 + 150, 650 + 4 * 48 - 20 + i * 45, 369, 45)

                        if option_rect.collidepoint(event.pos):  # Check if mouse is over a specific option
                            print (option)
                            return option  # Return the specific greedy search option selected

                elif self.selected_option == 5:  # A*, handle nested options

                    # Check which A* option is selected

                    for i, option in enumerate(self.astar_options):

                        option_rect = pygame.Rect(self.screen.get_width() // 2 + 150, 650 + 5 * 48 - 20 + i * 45, 223, 45)

                        if option_rect.collidepoint(event.pos):  # Check if mouse is over a specific option

                            print (option)
                            return option  # Return the specific A* option selected
                        
                        
                elif self.selected_option == 6:  # Board size
                    # Cycle through board sizes
                    self.current_board_size_index = (self.current_board_size_index + 1) % len(self.board_sizes)
                    return None  # No action needed, just update the display
                elif self.selected_option == 7:  # Music
                    self.music_on = not self.music_on  # Toggle music state
                    if self.music_on:
                        pygame.mixer.music.set_volume(1.0)  # Set volume to max
                    else:
                        pygame.mixer.music.set_volume(0.0)  # Mute music
                    return None  # No action needed, just update the display
                elif self.selected_option == 8:  # Exit
                    pygame.quit()
                    sys.exit()

        return None
    
    def draw_popup(self, x, y, options, mouse_x, mouse_y):
        """Draws a popup box with given options at (x, y) and highlights the hovered option."""
        # Calculate the width of the longest option
        max_text_width = max(self.font.size(option)[0] for option in options)
        box_width = max_text_width + 20  # Add padding to the width
        
        # print("max width: ", max_text_width)
        
        box_height = len(options) * 45 + 5  # Calculate height based on number of options

        # Popup background color and text color
        popup_color = (255, 165, 0)
        text_color = (255, 255, 255)  # White

        # Draw the popup background
        popup_rect = pygame.Rect(x, y, box_width, box_height)
        pygame.draw.rect(self.screen, popup_color, popup_rect, border_radius=10)

        # Render and position each option
        for i, option in enumerate(options):
            # Check if the mouse is hovering over this option
            option_rect = pygame.Rect(x + 10, y + 10 + i * 45, box_width - 20, 45)  # Adjust dimensions
            
            # Change the color if hovering over the option
            if option_rect.collidepoint(mouse_x, mouse_y):
                color = (255, 255, 255)  # White for the hovered option
            else:
                color = (0, 0, 0)  # Grey for the non-hovered options

            # Render the option with the selected color
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(topleft=(x + 10, y + 10 + i * 45))  # Add padding
            self.screen.blit(text_surface, text_rect)


    def draw_input_popup(self, mouse_x, mouse_y):
        """Draws a popup input box for entering the max_depth of DFS."""
        # Define the dimensions of the input popup
        box_width = 300
        box_height = 100

        # Popup background color and text color
        popup_color = (255, 165, 0)  # Orange
        text_color = (0, 0, 0)  # Black

        # Draw the popup background
        popup_rect = pygame.Rect(self.screen.get_width() // 2 + 150 - 10, 650 + 2 * 48 - 10, box_width + 20, box_height+50)
        pygame.draw.rect(self.screen, popup_color, popup_rect, border_radius=10)

        # Render the label asking for max_depth
        font = pygame.font.SysFont(None, 35)
        label_surface = font.render("Enter Max Depth for DFS:", True, text_color)
        label_rect = label_surface.get_rect(center=(self.screen.get_width() // 2 + 300, 650 + 2 * 48 + 10))
        self.screen.blit(label_surface, label_rect)

        # Render the input text (current value)
        input_surface = font.render(self.input_text, True, text_color)
        input_rect = input_surface.get_rect(center=(self.screen.get_width() // 2 + 300, 650 + 2 * 48 + 60))
        self.screen.blit(input_surface, input_rect)

        # Draw the input box border
        input_box_rect = pygame.Rect(self.screen.get_width() // 2 + 200, 650 + 2 * 48 + 40, 200, 40)
        pygame.draw.rect(self.screen, text_color, input_box_rect, 2)  # Border for the input box

        # Define the Submit button
        submit_button_rect = pygame.Rect(self.screen.get_width() // 2 + 250, 650 + 2 * 48 + 90, 100, 40)
        pygame.draw.rect(self.screen, (0, 255, 0), submit_button_rect, border_radius=5)  # Green button

        # Render Submit text on the button
        submit_text = font.render("Submit", True, text_color)
        submit_text_rect = submit_text.get_rect(center=submit_button_rect.center)
        self.screen.blit(submit_text, submit_text_rect)

        # Handle user input for the max_depth
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]  # Remove last character
                elif event.unicode.isdigit():
                    self.input_text += event.unicode  # Add digit to input text

            # Check if the Submit button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if submit_button_rect.collidepoint(mouse_x, mouse_y):
                        try:

                            cols, rows = self.board_sizes[self.current_board_size_index]
                            game = Game(cols, rows)  # Pass the selected board size to the Game instance

                            self.show_solving_message() # Solving window

                            # Initialize the game and the solver
                            solver = Solver(game)

                            self.max_depth = int(self.input_text)

                            # max_depth = self.get_dfs_depth()
                            # Run the BFS solver to find the solution path
                            solver.track_solver(lambda: solver.dfs(self.max_depth), 'DFS')


                            # # Parse the input value as an integer and update max_depth
                            # self.max_depth = int(self.input_text)
                            # print(f"Max Depth for DFS: {self.max_depth}")  # Debug print
                            # return "DFS"  # Submit the action
                        except ValueError:
                            print("Invalid input. Please enter an integer.")

            if event.type == pygame.KEYDOWN:  # Check if a key is pressed
                if event.key == pygame.K_RETURN:  # Check if the Enter key is pressed
                    try:
                        cols, rows = self.board_sizes[self.current_board_size_index]
                        game = Game(cols, rows)  # Pass the selected board size to the Game instance

                        self.show_solving_message()  # Solving window

                        # Initialize the game and the solver
                        solver = Solver(game)

                        # Parse the input value as an integer and set max_depth
                        self.max_depth = int(self.input_text)

                        # Run the DFS solver with the specified max depth
                        solver.track_solver(lambda: solver.dfs(self.max_depth), 'DFS')

                        print(f"Max Depth for DFS: {self.max_depth}")  # Debug print
                    except ValueError:
                        print("Invalid input. Please enter an integer.")

        
        # Highlight the input box if the mouse is over it
        if input_box_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(self.screen, (255, 255, 255), input_box_rect, 2)  # White border on hover

        # Highlight the submit button if the mouse is over it
        if submit_button_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(self.screen, (0, 200, 0), submit_button_rect, 2)  # Darker green on hover


    ##PROLLY UNCOMMENT THIS -->
    # def get_dfs_depth(self):
    #     # Try to convert the input to an integer
    #     try:
    #         return int(self.dfs_depth_input) if self.dfs_depth_input else None
    #     except ValueError:
    #         return None
    ##PROLLY UNCOMMENT THIS^^


    def show_solving_message(self):
        font = pygame.font.SysFont(None, 60)
        solving_text = font.render("Solving...", True, (100, 100, 100))
        text_rect = solving_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.fill((246, 221, 100))
        self.screen.blit(solving_text, text_rect)
        pygame.display.flip()
from collections import deque
from game import Game, Block
import pygame
import time
import sys

cols, rows = 5, 4 # Grid size

class Solver:

    def __init__(self, game):

        self.game = game
        self.initial_state = game.state
        self.target_positions = [(3, 1), (4, 1), (3, 2), (4, 2)]

    def bfs(self):
        # Perform BFS to find the shortest path to the goal state
        initial_state_tuple = self.state_to_tuple(self.initial_state)
        if self.is_goal_state(self.initial_state):
            print("Goal reached with 0 moves.")
            return []

        visited = set([initial_state_tuple])
        queue = deque([(self.initial_state, [])])  # Queue stores state and path

        while queue:
            current_state, path = queue.popleft()
            new_path = path + [current_state]
            # Check all possible moves for each block
            for block in current_state:
                for direction in ['left', 'right', 'up', 'down']:
                    new_state = self.move_block(block, direction, current_state)
                    if new_state:
                        state_tuple = self.state_to_tuple(new_state)
                        if state_tuple not in visited:
                            visited.add(state_tuple)
                            if self.is_goal_state(new_state):
                                # Prints solution step by step
                                self.print_solution(new_path)
                                print(f"Solution found!!! In {len(new_path) - 1} moves")
                                # Pass the initial state to animate the solution steps from there
                                self.animate_solution(new_path)
                                return new_path  # Return the list of moves

                            queue.append((new_state, new_path))

        print("No solution found.")
        return []

    def move_block(self, block, direction, current_state):
        # Moves a block in a specific direction if it's valid.
        cloned_block = Block(block.grid_x, block.grid_y, block.size_x, block.size_y)
        new_state = [Block(b.grid_x, b.grid_y, b.size_x, b.size_y) for b in current_state]

        if direction == 'left' and cloned_block.grid_x > 0:
            cloned_block.grid_x -= 1
        elif direction == 'right' and cloned_block.grid_x < cols - cloned_block.size_x:
            cloned_block.grid_x += 1
        elif direction == 'up' and cloned_block.grid_y > 0:
            cloned_block.grid_y -= 1
        elif direction == 'down' and cloned_block.grid_y < rows - cloned_block.size_y:
            cloned_block.grid_y += 1
        else:
            return False
        # Updates a block position in the new board state
        for idx, b in enumerate(new_state):
            if b.grid_x == block.grid_x and b.grid_y == block.grid_y:
                new_state[idx] = cloned_block
                break
        # Checks collisions after the move
        if self.check_collisions(cloned_block, new_state):
            return False

        return new_state

    def check_collisions(self, block, current_state):
        # Checks if a block collides with any other blocks
        occupied_positions = set()
        for b in current_state:
            if b != block:
                occupied_positions.update(b.get_positions())
        return any(pos in occupied_positions for pos in block.get_positions())

    def is_goal_state(self, state):
        # Checks if the current state is the goal state.
        red_block = state[0]  # Assuming red block is the first block
        return all(pos in self.target_positions for pos in red_block.get_positions())

    def state_to_tuple(self, state):
        # Converts the current state to a tuple for immutability
        return tuple(sorted((block.grid_x, block.grid_y, block.size_x, block.size_y) for block in state))

    def print_solution(self, solution_path):
        for step, state in enumerate(solution_path, start=0):
            # Prints each step of the final solution
            print(f"Step {step}:")
            for block in state:
                print(f"Block at ({block.grid_x}, {block.grid_y}) with size ({block.size_x}, {block.size_y})")
            print("-" * 30)

    def animate_solution(self, solution_path):
        for _, state in enumerate(solution_path):
            # Apply each step from the solution path
            self.game.state = state
            self.game.draw()  # Draw the updated game state on the screen
            time.sleep(0.5)  # Delay for animation
        sys.exit()  # Exit the game after animation
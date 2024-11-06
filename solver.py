from game import Game

class Boardd:
    def __init__(self, state):
        # state is now a tuple of positions (grid_x, grid_y)
        self.state = state  # No need to convert to tuple again

    def move(self, block_index, new_position):
        new_state = list(self.state)
        new_state[block_index] = new_position  # Update the position of the block
        return Boardd(tuple(new_state))  # Return a new Boardd with a tuple state

    def potential_moves(self):
        moves = []
        empty_positions = self.empty_positions()
        for index, position in enumerate(self.state):
            for new_position in self.get_possible_moves(position, empty_positions):
                moves.append((index, new_position))  # Append the block index and new position
        return moves

    def get_possible_moves(self, position, empty_positions):
        row, col = position
        possible_moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (new_row, new_col) in empty_positions:
                possible_moves.append((new_row, new_col))

        return possible_moves

    def empty_positions(self):
        occupied_positions = set(self.state)
        all_positions = {(r, c) for r in range(4) for c in range(5)}  # Assuming a 4x5 grid
        return list(all_positions - occupied_positions)

    def __hash__(self):
        return hash(frozenset(self.state))

    def __eq__(self, other):
        return hash(self) == hash(other)

    @classmethod
    def from_board(cls, state):
        return cls(state)  # Directly accept the state

    def is_solved(self):
        # Define the target positions for the red block (2x2)
        target_positions = {(3, 1), (4, 1), (3, 2), (4, 2)}  # Adjust based on your winning condition

        # Get the positions of the red block (assuming it's the first block in the state)
        red_block_position = self.state[0]  # This is now a tuple (grid_x, grid_y)

        # Get the positions occupied by the red block (2x2)
        red_positions = {(red_block_position[0], red_block_position[1]),
                         (red_block_position[0] + 1, red_block_position[1]),
                         (red_block_position[0], red_block_position[1] + 1),
                         (red_block_position[0] + 1, red_block_position[1] + 1)}

        # Check if all positions of the red block are in the target positions
        return red_positions == target_positions

def bfs_solver(game_state):
    # Extract positions from Block objects
    initial_state = [(block.grid_x, block.grid_y) for block in game_state]
    start_board = Boardd(initial_state)

    visited_boards = set()
    new_boards = [start_board]
    new_boards_set = {start_board}
    transitions = {}
    board = None

    while new_boards:
        board = new_boards.pop(0)
        new_boards_set.remove(board)

        if board.is_solved():
            break

        visited_boards.add(board)

        for block_index, new_position in board.potential_moves():
            new_board = board.move(block_index, new_position)

            if new_board not in visited_boards and new_board not in new_boards_set:
                new_boards.append(new_board)
                new_boards_set.add(new_board)
                transitions[new_board] = (board, block_index, new_position)

    # Backtrack to construct the solution path
    moves_taken = []
    while board != start_board:
        board, block_index, new_position = transitions[board]
        moves_taken.insert(0, (block_index, new_position))

    print("Moves found:", moves_taken)
    return moves_taken

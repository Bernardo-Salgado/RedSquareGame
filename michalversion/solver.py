from game import Game

class Boardd:
    def __init__(self, state):
        self.state = state  # state is a list of tuples (row, col) for each block

    def move(self, block_index, new_position):
        # Create a new state with the block moved to the new position
        new_state = list(self.state)
        new_state[block_index] = new_position  # Update the position of the block
        return Boardd(new_state)

    def potential_moves(self):
        moves = []
        empty_positions = self.empty_positions()  # Implement this method to find empty positions
        for index, position in enumerate(self.state):
            for new_position in self.get_possible_moves(position, empty_positions):
                moves.append((index, new_position))  # Append the block index and new position
        return moves

    def get_possible_moves(self, position, empty_positions):
        # Generate possible moves for a block based on its current position
        row, col = position
        possible_moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (new_row, new_col) in empty_positions:
                possible_moves.append((new_row, new_col))

        return possible_moves

    def empty_positions(self):
        # Determine empty positions in the grid based on the current state
        occupied_positions = set(self.state)
        all_positions = {(r, c) for r in range(4) for c in range(5)}  # Assuming a 4x5 grid
        return list(all_positions - occupied_positions)

    def __hash__(self):
        return hash(frozenset(self.state))

    def __eq__(self, other):
        return hash(self) == hash(other)

    @classmethod
    def from_board(cls, game_state):
        return cls(game_state)

def bfs_solver(game_state):
    start_board = Boardd.from_board(game_state)

    visited_boards = set()
    new_boards = [start_board]
    new_boards_set = {start_board}
    transitions = {}
    board = None

    while new_boards:
        board = new_boards.pop(0)
        new_boards_set.remove(board)

        if board.is_solved():  # Implement this method to check if the game is solved
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

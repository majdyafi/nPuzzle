import numpy as np
from collections import deque


class Puzzle:
    # store the 2d array
    #
    def __init__(self, a):
        self.a = a
        self.zero_pos = np.where(self.a == 0)
        self.zero = (self.zero_pos[0][0], self.zero_pos[1][0])

    def get_valid_moves(self):
        row, col = self.zero
        rows, cols = self.a.shape
        valid_moves = []
        if row > 0:
            valid_moves.append("UP")
        if row < rows - 1:
            valid_moves.append("DOWN")
        if col > 0:
            valid_moves.append("LEFT")
        if col < cols - 1:
            valid_moves.append("RIGHT")

        return valid_moves

    def make_move(self, direction):
        new_array = self.a.copy()
        row, col = self.zero
        if direction == "UP":
            new_row, new_col = row - 1, col
        elif direction == "DOWN":
            new_row, new_col = row + 1, col
        elif direction == "RIGHT":
            new_row, new_col = row, col + 1
        elif direction == "LEFT":
            new_row, new_col = row, col - 1
        else:
            raise ("invlaid direction")

        new_array[row, col], new_array[new_row, new_col] = (
            new_array[new_row, new_col],
            new_array[row, col],
        )

        return Puzzle(new_array)

    def is_goal(self):
        rows, cols = self.a.shape
        x = 0
        for row in range(rows):
            for col in range(cols):
                if row == rows - 1 and col == cols - 1:
                    if self.a[row][col] != 0:
                        return False
                    else:
                        return True
                x += 1
                if x == self.a[row][col]:
                    pass
                else:
                    return False

        return True

    def __hash__(self):
        return hash(self.a.tobytes())

    def __eq__(self, other):
        return np.array_equal(self.a, other.a)


def solve_puzzle(initial_puzzle):
    # If already solved, return empty path
    if initial_puzzle.is_goal():
        return []

    # Initialize BFS
    queue = deque([(initial_puzzle, [])])
    visited = set()
    visited.add(initial_puzzle)

    # BFS loop
    while queue:
        current_puzzle, path_to_current = queue.popleft()

        # Try all valid moves from current state
        for move in current_puzzle.get_valid_moves():
            # Make the move
            new_puzzle = current_puzzle.make_move(move)

            # Check if we reached the goal
            if new_puzzle.is_goal():
                return path_to_current + [move]

            # If not visited, add to queue
            if new_puzzle not in visited:
                visited.add(new_puzzle)
                new_path = path_to_current + [move]
                queue.append((new_puzzle, new_path))

    # No solution found
    return None


# Test with a scrambled puzzle
print("\n" + "=" * 50)
print("Testing with scrambled puzzle:")
scrambled = np.array([[1, 2, 3], [4, 0, 6], [7, 5, 8]])
scrambled_puzzle = Puzzle(scrambled)
print(scrambled_puzzle.a)
solution = solve_puzzle(scrambled_puzzle)
if solution is not None:
    print(f"Solution found in {len(solution)} moves: {solution}")
else:
    print("No solution found")

import numpy as np
from collections import deque
import heapq


class Puzzle:
    def __init__(self, grid):
        self.grid = np.array(grid)
        self.size = self.grid.shape[0]
        zero_pos = np.where(self.grid == 0)
        self.zero_row = zero_pos[0][0]
        self.zero_col = zero_pos[1][0]

    def manhattan_distance(self):
        distance = 0

        for row in range(self.size):
            for col in range(self.size):
                value = self.grid[row, col]
                if value != 0:
                    target_row = (value - 1) // self.size
                    target_col = (value - 1) % self.size

                    distance += abs(row - target_row) + abs(col - target_col)

        return distance

    def is_goal(self):
        expected = 1
        for r in range(self.size):
            for c in range(self.size):
                if r == self.size - 1 and c == self.size - 1:
                    return self.grid[r][c] == 0
                if self.grid[r][c] != expected:
                    return False
                expected += 1
        return True

    def get_valid_moves(self):
        """Just return which moves are possible"""
        moves = []
        if self.zero_row > 0:
            moves.append("UP")
        if self.zero_row < self.size - 1:
            moves.append("DOWN")
        if self.zero_col > 0:
            moves.append("LEFT")
        if self.zero_col < self.size - 1:
            moves.append("RIGHT")
        return moves

    def make_move(self, direction):
        """Apply a move and return new Puzzle"""
        new_grid = self.grid.copy()

        if direction == "UP":
            new_grid[self.zero_row][self.zero_col] = new_grid[self.zero_row - 1][
                self.zero_col
            ]
            new_grid[self.zero_row - 1][self.zero_col] = 0
        elif direction == "DOWN":
            new_grid[self.zero_row][self.zero_col] = new_grid[self.zero_row + 1][
                self.zero_col
            ]
            new_grid[self.zero_row + 1][self.zero_col] = 0
        elif direction == "LEFT":
            new_grid[self.zero_row][self.zero_col] = new_grid[self.zero_row][
                self.zero_col - 1
            ]
            new_grid[self.zero_row][self.zero_col - 1] = 0
        elif direction == "RIGHT":
            new_grid[self.zero_row][self.zero_col] = new_grid[self.zero_row][
                self.zero_col + 1
            ]
            new_grid[self.zero_row][self.zero_col + 1] = 0

        return Puzzle(new_grid)

    def __hash__(self):
        return hash(self.grid.tobytes())

    def __eq__(self, other):
        return np.array_equal(self.grid, other.grid)


def solve_astar(initial_puzzle):
    if initial_puzzle.is_goal():
        return []

    g_score = 0
    h_score = initial_puzzle.manhattan_distance()
    f_score = g_score + h_score

    counter = 0
    heap = [(f_score, counter, g_score, initial_puzzle, [])]
    visited = set()

    iterations = 0

    while heap:
        iterations += 1
        f_score, _, g_score, puzzle, path = heapq.heappop(heap)

        if puzzle in visited:
            continue

        visited.add(puzzle)

        if puzzle.is_goal():
            print(f"Goal found after {iterations} iterations!")
            return path

        for move in puzzle.get_valid_moves():
            new_puzzle = puzzle.make_move(move)
            if new_puzzle not in visited:
                new_g_score = g_score + 1
                h_score = new_puzzle.manhattan_distance()
                new_f_score = new_g_score + h_score

                counter += 1
                heapq.heappush(
                    heap, (new_f_score, counter, new_g_score, new_puzzle, path + [move])
                )

    return None


print("Testing A* solver:")
test = np.array([[1, 2, 3], [4, 0, 6], [7, 5, 8]])
puzzle = Puzzle(test)
print("Initial state:")
print(puzzle.grid)
print(f"Manhattan distance: {puzzle.manhattan_distance()}")

print("Testing equality:")
p1 = Puzzle([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
p2 = Puzzle([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
print(f"p1 == p2: {p1 == p2}")
print(f"p1 in {p2}: {p1 in {p2}}")

goal_state = Puzzle([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
print(f"Goal state is_goal(): {goal_state.is_goal()}")

solution = solve_astar(puzzle)
print(f"\nSolution: {solution}")


print("\nLet's manually check the moves:")
print("Move DOWN:")
p1 = puzzle.make_move("DOWN")
print(p1.grid)
print(f"Is goal? {p1.is_goal()}")

print("\nThen move RIGHT:")
p2 = p1.make_move("RIGHT")
print(p2.grid)
print(f"Is goal? {p2.is_goal()}")

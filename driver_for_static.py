from manhattan_misplaced_handler import ManhattanMisplacedHandler
from uniform_cost_search_handler import UniformCostSearch

# Goal state for reference
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# 8-Puzzle examples by depth (minimum number of moves to goal_state)
# 0 represents the blank space

# Depth 2
# Original:
# 1 2 3
# 4 X 6
# 7 5 8
puzzle_depth_2 = [1, 2, 3, 4, 0, 6, 7, 5, 8]

# Depth 5
# An example of an "easy" puzzle, precise depth would need verification by a solver.
# Original:
# 1 2 3
# X 5 6
# 4 7 8
puzzle_depth_5_example = [
    1,
    2,
    3,
    0,
    5,
    6,
    4,
    7,
    8,
]  # Exact depth of 5 not guaranteed without solving

# Depth 10
# No specific example was readily available for an exact depth of 10.
# Puzzles of "medium" difficulty might have solution lengths around this depth.
puzzle_depth_10_example = (
    None  # Placeholder, specific instance would require generation/solving
)

# Depth 15
# No specific example was readily available for an exact depth of 15.
puzzle_depth_15_example = (
    None  # Placeholder, specific instance would require generation/solving
)

# Depth 20
# Original:
# 6 1 8
# 4 X 2
# 7 3 5
puzzle_depth_20 = [6, 1, 8, 4, 0, 2, 7, 3, 5]

# Depth 25
# No specific example was readily available for an exact depth of 25.
# Puzzles with depths around 25 are considered quite difficult.
puzzle_depth_25_example = (
    None  # Placeholder, specific instance would require generation/solving
)

# Depth 30
# Original:
# 8 6 4
# 2 1 3
# 5 7 X
puzzle_depth_30 = [8, 6, 4, 2, 1, 3, 5, 7, 0]

# Depth 31 (Maximum Depth)
# This is one of the "hardest" 8-puzzle configurations.
# Original:
# 8 6 7
# 2 5 4
# 3 X 1
puzzle_depth_31 = [8, 6, 7, 2, 5, 4, 3, 0, 1]

# --- Outputting the examples ---
print(f"Goal State: {goal_state}\n")

print(f"Puzzle (Depth 2): {puzzle_depth_2}")
# To verify, you would typically use an A* search algorithm with the Manhattan distance heuristic.
# Example moves for puzzle_depth_2 to reach goal_state:
# [1, 2, 3, 4, 0, 6, 7, 5, 8] -> move 5 right
# [1, 2, 3, 4, 5, 6, 7, 0, 8] -> move 8 up
# [1, 2, 3, 4, 5, 6, 7, 8, 0] (Goal!)

print(f"Puzzle (Depth 5 Example): {puzzle_depth_5_example}")
print(
    f"Puzzle (Depth 10 Example): {puzzle_depth_10_example if puzzle_depth_10_example else 'Specific example not provided, requires generation.'}"
)
print(
    f"Puzzle (Depth 15 Example): {puzzle_depth_15_example if puzzle_depth_15_example else 'Specific example not provided, requires generation.'}"
)
print(f"Puzzle (Depth 20): {puzzle_depth_20}")
print(
    f"Puzzle (Depth 25 Example): {puzzle_depth_25_example if puzzle_depth_25_example else 'Specific example not provided, requires generation.'}"
)
print(f"Puzzle (Depth 30): {puzzle_depth_30}")
print(f"Puzzle (Depth 31 - Max): {puzzle_depth_31}")

# Note:
# The blank space is 0. The tiles are numbered 1-8.
# A 1D list represents the 3x3 grid row by row.
# For example, [a, b, c, d, e, f, g, h, i] corresponds to:
# a b c
# d e f
# g h i
#
# Finding or verifying the exact depth of a given 8-puzzle state typically requires
# a search algorithm (like A* with an appropriate heuristic, e.g., Manhattan distance)
# to find the shortest path to the goal state.

puzzle_lists = [
    puzzle_depth_2,
    puzzle_depth_5_example,
    puzzle_depth_10_example,
    puzzle_depth_15_example,
    puzzle_depth_20,
    puzzle_depth_25_example,
    puzzle_depth_30,
    puzzle_depth_31,
]

list_of_depths = {
    2: 0,
    5: 0,
    10: 0,
    15: 0,
    20: 0,
    25: 0,
    30: 0,
    31: 0,
}
list_of_nodes_expanded = {
    2: 0,
    5: 0,
    10: 0,
    15: 0,
    20: 0,
    25: 0,
    30: 0,
    31: 0,
}
list_of_max_queue_size = {
    2: 0,
    5: 0,
    10: 0,
    15: 0,
    20: 0,
    25: 0,
    30: 0,
    31: 0,
}

for puzzle in puzzle_lists:
    if puzzle:
        print(f"Testing puzzle: {puzzle}")
        solver = UniformCostSearch(puzzle, goal_state)
        # solver = ManhattanMisplacedHandler(puzzle, goal_state, "misplaced")
        results = solver.solve()
        (
            path,
            depth,
            max_queue,
            expanded_nodes,
        ) = results
        results = solver.solve()
        # (path, depth, max_queue, expanded_nodes, _, _, _, _) = results
        if path:
            print("Solved!")
            print("------------------------------")
            for i in range(len(path)):
                print(f"Step: {i + 1}")
                print(path[i])  # Print the state grid
            print(f"Depth for the Solution Was: {depth}")
            print(f"Number of Nodes Expanded: {expanded_nodes}")
            print(f"Max Queue Size: {max_queue}")
            print()
            list_of_depths[depth] = depth
            list_of_nodes_expanded[depth] = expanded_nodes
            list_of_max_queue_size[depth] = max_queue

        else:
            print("No solution")
    else:
        print("No specific example provided for this depth.")
#     print()
#     print("====================================")
print("Summary of Results:")

# for depth in list_of_depths:
#     if list_of_depths[depth] != 0:
#         print(f"Depth: {depth}")
#         print(f"Nodes Expanded: {list_of_nodes_expanded[depth]}")
#         print(f"Max Queue Size: {list_of_max_queue_size[depth]}")
#         print()
# Collect actual solved depths for which we have data (expanded_nodes > 0)
# The keys of list_of_nodes_expanded will be the actual depths that were solved.
solved_depth_keys = []
for depth_key, nodes_count in list_of_nodes_expanded.items():
    # A puzzle is considered solved and data recorded if nodes_count > 0.
    # (Assuming a solved puzzle always expands at least one node,
    # or depth 0 goal state match is handled such that nodes_count reflects activity)
    # Also, the corresponding entry in list_of_depths should reflect the depth.
    if nodes_count > 0 and list_of_depths.get(depth_key) == depth_key:
        solved_depth_keys.append(depth_key)

# Sort these collected depth keys in ascending order
sorted_actual_depths = sorted(solved_depth_keys)

if not sorted_actual_depths:
    print("No puzzles were solved or no valid results to display.")
else:
    for solved_depth in sorted_actual_depths:
        print(f"Depth: {solved_depth}")
        print(f"Nodes Expanded: {list_of_nodes_expanded[solved_depth]}")
        print(f"Max Queue Size: {list_of_max_queue_size[solved_depth]}")
        print("--------------------")
print("====================================")

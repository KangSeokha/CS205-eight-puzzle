from uniform_cost_search_handler import UniformCostSearch
# from misplaced_tile_search_handler import PuzzleSolver


def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print("------------------------------")


if __name__ == '__main__':
    start_state = [2, 4, 3,
                   5, 1, 8,
                   7, 6, 0]
    goal_state = [1, 2, 3,
                  4, 5, 6,
                  7, 8, 0]

    solver = UniformCostSearch(start_state, goal_state)
    results = solver.solve()
    path, depth, max_queue, expanded_nodes,  = results

    if path:
        print("Solved!")
        print("------------------------------")
        for state in path:
            print_state(state)  # Print the state grid
        print(f"Depth for the Solution Was: {depth}")
        print(f"Number of Nodes Expanded: {expanded_nodes}")
        print(f"Max Queue Size: {max_queue}")
    else:
        print("No solution")

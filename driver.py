from uniform_cost_search_handler import UniformCostSearch

# from misplaced_tile_search_handler import PuzzleSolver
from manhattan_misplaced_handler import ManhattanMisplacedHandler


def print_state(state):
    for i in range(0, 9, 3):
        print(state[i : i + 3])
    print("------------------------------")


if __name__ == "__main__":
    start_state = [2, 4, 3, 5, 1, 8, 7, 6, 0]
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    choice = input(
        "Enter \n"
        "1 for Uniform Cost Search, \n"
        "2 for Misplaced Tile Heuristic, \n"
        "3 for Manhattan Distance Heuristic: \n"
        "Your choice: "
    )
    if choice == "1":
        print("Using Uniform Cost Search")
        print()
        solver = UniformCostSearch(start_state, goal_state)
        results = solver.solve()
        (
            path,
            depth,
            max_queue,
            expanded_nodes,
        ) = results
        if path:
            print("Solved!")
            print("------------------------------")
            # for state in path:
            for i in range(len(path)):
                print(f"Step: {i + 1}")
                print_state(path[i])  # Print the state grid
            print(f"Depth for the Solution Was: {depth}")
            print(f"Number of Nodes Expanded: {expanded_nodes}")
            print(f"Max Queue Size: {max_queue}")
            print()
            print()
        else:
            print("No solution")
    elif choice == "2" or choice == "3":
        if choice == "2":
            solver = ManhattanMisplacedHandler(start_state, goal_state, "misplaced")
            print("Using Misplaced Tile Heuristic")
            print()
        elif choice == "3":
            solver = ManhattanMisplacedHandler(start_state, goal_state, "manhattan")
            print("Using Manhattan Distance Heuristic")
            print()

        results = solver.solve()
        (
            path,
            depth,
            max_queue,
            expanded_nodes,
            time_cost,
            gh_cost,
            g_n_values_path,
            h_n_values_path,
        ) = results

        # if path:
        #     print("Solved!")
        #     print("------------------------------")
        #     for state in path:
        #         # print("g(n) values: ", g_n_values_path)
        #         # print("h(n) values: ", h_n_values_path)
        #         print("gh(n) values: ", gh_cost[tuple(state)])
        #         print_state(state)  # Print the state grid
        #     print()
        #     print(f"Depth for the Solution Was: {depth}")
        #     print(f"Number of Nodes Expanded: {expanded_nodes}")
        #     print(f"Max Queue Size: {max_queue}")
        if path:
            print("Solved!")
            print("------------------------------")
            for i in range(len(path)):
                print("g(n) values: ", g_n_values_path[i])
                print("h(n) values: ", h_n_values_path[i])
                print_state(path[i])  # Print the state grid
            print(f"Depth for the Solution Was: {depth}")
            print(f"Number of Nodes Expanded: {expanded_nodes}")
            print(f"Max Queue Size: {max_queue}")
        else:
            print("No solution")

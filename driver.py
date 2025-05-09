from uniform_cost_search_handler import UniformCostSearch
from manhattan_misplaced_handler import ManhattanMisplacedHandler


def print_state(state):
    for i in range(0, 9, 3):
        print(state[i : i + 3])
    print("------------------------------")


if __name__ == "__main__":
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    customized_input_choice = input(
        "Enter \n"
        "1 for Choose your own array, \n"
        "2 for Default array: \n"
        "Your choice: "
    )
    if customized_input_choice == "1":
        start_state = []
        print(
            "Enter your puzzle, using a zero to represent the blank. Please only enter valid 8-puzzles. Enter the puzzle delimiting the numbers with a space. Type RET only when finished."
        )
        while len(start_state) < 9:
            row = input(f"Enter the {len(start_state)//3 + 1} row: ")
            if len(row.split()) == 3:
                start_state.extend(int(num) for num in row.split())
            else:
                print(
                    "Invalid row. Each row must consist of exactly three numbers, all between 0 and 8."
                )
            if len(start_state) == 9 and len(set(start_state)) != 9:
                print(
                    "Invalid puzzle. Ensure all numbers from 0 to 8 are present and unique."
                )
                start_state.clear()
    elif customized_input_choice == "2":
        start_state = [2, 4, 3, 5, 1, 8, 7, 6, 0]

    algorithm_choice = input(
        "Enter \n"
        "1 for Uniform Cost Search, \n"
        "2 for Misplaced Tile Heuristic, \n"
        "3 for Manhattan Distance Heuristic: \n"
        "Your choice: "
    )

    if algorithm_choice == "1":
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
    elif algorithm_choice == "2" or algorithm_choice == "3":
        if algorithm_choice == "2":
            solver = ManhattanMisplacedHandler(start_state, goal_state, "misplaced")
            print("Using Misplaced Tile Heuristic")
            print()
        elif algorithm_choice == "3":
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

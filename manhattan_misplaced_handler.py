import time
import heapq
from typing import List, Tuple, Optional, Set, Dict, Callable  # Added Callable

GridState = List[int]
GridStateTuple = Tuple[int, ...]
Position = Tuple[int, int]  # (row, col)


class ManhattanMisplacedHandler:
    """
    Calculates heuristics (Misplaced Tile, Manhattan Distance) and performs
    A* search using a selected heuristic for the 8-puzzle problem.
    Returns detailed metrics including lists of g(n) and h(n) for the solution path.
    """

    def __init__(
        self,
        start_state: GridState,
        goal_state: GridState,
        heuristic_type: str = "misplaced",
    ):
        """
        Initializes the solver with start/goal states and selects the heuristic.

        Args:
            start_state: The initial puzzle configuration (list of 9 ints).
            goal_state: The target configuration of the puzzle (list of 9 ints).
            heuristic_type: The heuristic to use ('misplaced' or 'manhattan').
                            Defaults to 'misplaced'.

        Raises:
            ValueError: If states are invalid or heuristic_type is unknown.
        """
        if not isinstance(start_state, list) or len(start_state) != 9:
            raise ValueError("start_state must be a list of 9 integers.")
        if not isinstance(goal_state, list) or len(goal_state) != 9:
            raise ValueError("goal_state must be a list of 9 integers.")

        valid_heuristics = ["misplaced", "manhattan"]
        if heuristic_type not in valid_heuristics:
            raise ValueError(f"Invalid heuristic_type. Choose from: {valid_heuristics}")

        self.start_state: GridState = start_state
        self.goal_state: GridState = goal_state
        self.goal_state_tuple: GridStateTuple = tuple(goal_state)
        self.heuristic_type: str = heuristic_type

        # Pre-calculate goal positions for Manhattan distance efficiency
        self._goal_pos_map: Dict[int, Position] = self._calculate_positions(
            self.goal_state_tuple
        )

        # Assign the chosen heuristic function
        if self.heuristic_type == "misplaced":
            self.heuristic_func: Callable[[GridState], int] = self.calculate_misplaced
        elif self.heuristic_type == "manhattan":
            self.heuristic_func: Callable[[GridState], int] = self.calculate_manhattan
        # No else needed due to validation above

    def _calculate_positions(self, state_tuple: GridStateTuple) -> Dict[int, Position]:
        pos_map: Dict[int, Position] = {}
        for i, tile in enumerate(state_tuple):
            if tile != 0:
                pos_map[tile] = divmod(i, 3)
        return pos_map

    def calculate_misplaced(self, current_state: GridState) -> int:
        if not isinstance(current_state, list) or len(current_state) != 9:
            raise ValueError("current_state must be a list of 9 integers.")

        misplaced_count = 0
        current_state_tuple = tuple(current_state)
        for i in range(len(current_state_tuple)):
            current_tile = current_state_tuple[i]
            goal_tile = self.goal_state_tuple[i]
            if current_tile != 0 and current_tile != goal_tile:
                misplaced_count += 1
        return misplaced_count

    def calculate_manhattan(self, current_state: GridState) -> int:
        if not isinstance(current_state, list) or len(current_state) != 9:
            raise ValueError("current_state must be a list of 9 integers.")

        h_cost = 0
        current_state_tuple = tuple(current_state)
        current_pos_map = self._calculate_positions(current_state_tuple)

        for tile, current_pos in current_pos_map.items():
            goal_pos = self._goal_pos_map[tile]
            h_cost += abs(current_pos[0] - goal_pos[0]) + abs(
                current_pos[1] - goal_pos[1]
            )
        return h_cost

    def __call__(self, current_state: GridState) -> int:
        """Calls the selected heuristic function."""
        return self.heuristic_func(current_state)

    def _get_neighbors(self, state: GridState) -> List[GridState]:
        neighbors: List[GridState] = []
        try:
            zero_index = state.index(0)
        except ValueError:
            return []

        row, col = divmod(zero_index, 3)
        potential_moves = [(-3, row > 0), (3, row < 2), (-1, col > 0), (1, col < 2)]
        for delta_index, is_valid_move in potential_moves:
            if is_valid_move:
                neighbor_index = zero_index + delta_index
                next_state = list(state)
                next_state[zero_index], next_state[neighbor_index] = (
                    next_state[neighbor_index],
                    next_state[zero_index],
                )
                neighbors.append(next_state)
        return neighbors

    def _reconstruct_path(
        self,
        parent_map: Dict[GridStateTuple, Optional[GridState]],
        current_state: GridState,
    ) -> List[GridState]:
        path: List[GridState] = []
        state_list: Optional[GridState] = current_state
        while state_list is not None:
            path.append(state_list)
            state_tuple = tuple(state_list)
            state_list = parent_map.get(state_tuple)
        return path[::-1]

    def solve(
        self,
    ) -> Tuple[
        Optional[List[GridState]],
        Optional[int],
        int,
        int,
        str,
        Dict[GridStateTuple, Tuple[int, int]],
        List[int],
        List[int],
    ]:
        """
        Performs A* search using the heuristic selected during initialization.
        Returns the path, metrics, the full gh_map, and lists of g(n) and h(n)
        values specifically for the states in the solution path.
        """
        start_state = self.start_state
        start_state_tuple = tuple(start_state)

        pq: List[Tuple[int, GridState]] = []
        visited_set: Set[GridStateTuple] = set()
        parent_map: Dict[GridStateTuple, Optional[GridState]] = {}
        cost_map: Dict[GridStateTuple, int] = {}  # Stores g(n) cost
        # Stores (g(n), h(n))
        gh_map: Dict[GridStateTuple, Tuple[int, int]] = {}

        solution_depth: Optional[int] = None
        max_q_size: int = 0
        num_expanded_nodes: int = 0
        start_time = time.time()

        g_n_start = 0
        h_n_start = self.heuristic_func(start_state)
        f_n_start = g_n_start + h_n_start

        heapq.heappush(pq, (f_n_start, start_state))
        visited_set.add(start_state_tuple)
        parent_map[start_state_tuple] = None
        cost_map[start_state_tuple] = g_n_start
        gh_map[start_state_tuple] = (g_n_start, h_n_start)
        max_q_size = 1

        while pq:
            max_q_size = max(len(pq), max_q_size)

            f_current, current_state = heapq.heappop(pq)
            current_state_tuple = tuple(current_state)

            if current_state_tuple in cost_map and f_current > cost_map[
                current_state_tuple
            ] + self.heuristic_func(current_state):
                continue

            g_n_current = cost_map.get(current_state_tuple, 0)
            num_expanded_nodes += 1

            if current_state_tuple == self.goal_state_tuple:
                solution_path = self._reconstruct_path(parent_map, current_state)
                solution_depth = len(solution_path) - 1
                end_time = time.time()
                time_cost = f"{(end_time - start_time):.4f}"

                # --- Extract g(n) and h(n) for the solution path ---
                g_n_values_path: List[int] = []
                h_n_values_path: List[int] = []
                if solution_path:
                    for state in solution_path:
                        state_tuple_path = tuple(state)
                        g_val, h_val = gh_map.get(
                            state_tuple_path, (-1, -1)
                        )  # Get g,h from map
                        g_n_values_path.append(g_val)
                        h_n_values_path.append(h_val)
                # ----------------------------------------------------

                return (
                    solution_path,
                    solution_depth,
                    max_q_size,
                    num_expanded_nodes,
                    time_cost,
                    gh_map,  # Return the full map
                    g_n_values_path,  # Return list of g(n) for the path
                    h_n_values_path,  # Return list of h(n) for the path
                )

            neighbors = self._get_neighbors(current_state)
            move_cost = 1

            for neighbor_state in neighbors:
                neighbor_state_tuple = tuple(neighbor_state)
                tentative_g_n = g_n_current + move_cost

                if tentative_g_n < cost_map.get(neighbor_state_tuple, float("inf")):
                    h_n_neighbor = self.heuristic_func(neighbor_state)
                    f_n_neighbor = tentative_g_n + h_n_neighbor

                    cost_map[neighbor_state_tuple] = tentative_g_n
                    parent_map[neighbor_state_tuple] = current_state
                    gh_map[neighbor_state_tuple] = (
                        tentative_g_n,
                        h_n_neighbor,
                    )  # Store g and h
                    visited_set.add(neighbor_state_tuple)

                    heapq.heappush(pq, (f_n_neighbor, neighbor_state))

        # --- No Solution Found ---
        end_time = time.time()
        time_cost = f"{(end_time - start_time):.4f}"
        return (
            None,  # No path
            None,  # No depth
            max_q_size,
            num_expanded_nodes,
            time_cost,
            gh_map,  # Still return the map of explored states
            [],  # Empty list for g(n) path values
            [],  # Empty list for h(n) path values
        )


# if __name__ == '__main__':
#     start_state = [2, 4, 3,
#                    5, 1, 8,
#                    7, 6, 0]
#     goal_state = [1, 2, 3,
#                   4, 5, 6,
#                   7, 8, 0]

#     solver = PuzzleSolver(start_state, goal_state, "manhattan")
#     results = solver.solve()
#     path, depth, max_queue, expanded_nodes, elpased_time, g_n, h_n = results

#     new_result = (path, g_n, h_n)

#     if path:
#         print("Solved!")
#         print("------------------------------")
#         for state, g_val, h_val in zip(path, g_n, h_n):
#             print(f"f(n): {g_val + h_val}, g(n): {g_val}, h(n): {h_val}")
#             print_state(state)  # Print the state grid
#         print(f"Depth for the Solution Was: {depth}")
#         print(f"Number of Nodes Expanded: {expanded_nodes}")
#         print(f"Max Queue Size: {max_queue}")
#         print(f"Elpased Time : {elpased_time} sec")
#     else:
#         print("No solution")

from collections import deque
from typing import List, Tuple, Optional, Set, Dict, Deque

# Type aliases for clarity
GridState = List[int]
GridStateTuple = Tuple[int, ...]


class UniformCostSearch:
    """
    Solves the 8-puzzle problem using Uniform Cost Search (UCS).

    Since all moves have a uniform cost (assumed to be 1), this implementation
    uses Breadth-First Search (BFS), which is equivalent to UCS in this specific case.

    It finds the shortest path in terms of the number of moves from a start
    state to a goal state.
    """

    def __init__(self, start_state: GridState, goal_state: GridState):
        """
        Initializes the search problem.

        Args:
            start_state: The initial configuration of the puzzle (list of 9 ints, 0 represents blank).
            goal_state: The target configuration of the puzzle (list of 9 ints).

        Raises:
            ValueError: If start_state or goal_state are not lists of 9 integers.
        """
        if not isinstance(start_state, list) or len(start_state) != 9:
            raise ValueError("start_state must be a list of 9 integers.")
        if not isinstance(goal_state, list) or len(goal_state) != 9:
            raise ValueError("goal_state must be a list of 9 integers.")

        self.start_state: GridState = start_state
        self.goal_state: GridState = goal_state
        self.goal_state_tuple: GridStateTuple = tuple(
            goal_state)

        self.queue: Deque[GridState] = deque()
        self.visited_states: Set[GridStateTuple] = set()

        self.parent_map: Dict[GridStateTuple, Optional[GridState]] = {}

        self.solution_path: Optional[List[GridState]] = None
        self.solution_depth: Optional[int] = None
        self.max_queue_size: int = 0
        self.num_expanded_nodes: int = 0
        # self.elapsed_time: float = 0.0

    def _get_neighbors(self, state: GridState) -> List[GridState]:
        """
        Generates valid neighbor states by moving the blank tile (0).

        Args:
            state: The current state list.

        Returns:
            A list of valid neighbor state lists.
        """
        neighbors: List[GridState] = []
        try:
            zero_index = state.index(0)
        except ValueError:
            return []

        row, col = divmod(zero_index, 3)  # 3x3 grid assumed

        potential_moves = [
            (-3, row > 0),  # Move Up
            (3, row < 2),  # Move Down
            (-1, col > 0),  # Move Left
            (1, col < 2)  # Move Right
        ]

        for delta_index, is_valid_move in potential_moves:
            if is_valid_move:
                neighbor_index = zero_index + delta_index
                next_state = list(state)
                next_state[zero_index], next_state[neighbor_index] = next_state[neighbor_index], next_state[zero_index]
                neighbors.append(next_state)

        return neighbors

    def _reconstruct_path(self, current_state: GridState) -> List[GridState]:
        """
        Backtracks from the goal state to the start state using the parent map.

        Args:
            current_state: The goal state list that was found.

        Returns:
            The path from the start state to the goal state as a list of states.
        """
        path: List[GridState] = []
        state_list: Optional[GridState] = current_state
        while state_list is not None:
            path.append(state_list)
            state_tuple = tuple(state_list)
            state_list = self.parent_map.get(state_tuple)
        return path[::-1]

    def solve(self) -> Tuple[Optional[List[GridState]], Optional[int], int, int, str]:
        """
        Executes the Breadth-First Search algorithm to find the shortest path.

        Returns:
            A tuple containing:
            - The solution path (list of states from start to goal) or None if no solution.
            - The depth of the solution (number of moves) or None.
            - The maximum size the queue reached during the search.
            - The total number of nodes expanded (popped from queue and neighbors generated).
        """

        start_state_tuple = tuple(self.start_state)

        self.queue.append(self.start_state)
        self.visited_states.add(start_state_tuple)
        self.parent_map[start_state_tuple] = None
        self.max_queue_size = 1  # Initial queue size

        while self.queue:
            self.max_queue_size = max(len(self.queue), self.max_queue_size)

            current_state: GridState = self.queue.popleft()
            current_state_tuple: GridStateTuple = tuple(current_state)

            if current_state_tuple == self.goal_state_tuple:
                self.solution_path = self._reconstruct_path(current_state)
                self.solution_depth = len(self.solution_path) - 1
                return (
                    self.solution_path,
                    self.solution_depth,
                    self.max_queue_size,
                    self.num_expanded_nodes,
                )

            neighbors = self._get_neighbors(current_state)
            node_was_expanded = False

            for neighbor_state in neighbors:
                neighbor_state_tuple = tuple(neighbor_state)

                if neighbor_state_tuple not in self.visited_states:
                    self.visited_states.add(neighbor_state_tuple)
                    self.parent_map[neighbor_state_tuple] = current_state
                    self.queue.append(neighbor_state)
                    node_was_expanded = True

            if node_was_expanded:
                self.num_expanded_nodes += 1

        return (
            None,
            None,
            None,
            None
        )

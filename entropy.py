import math
import itertools

# GAME CONSTANTS
GRID_SIZE = 5
SHIP_LENGTH = 3
NUM_SHIPS = 3

class EntropyEngine:
    """
    For handling the mathematical backend for the game.
    It generates the State Space (S) and calculates Entropy (H).
    """
    def __init__(self):
        # 1. Generating the 'Universe' of all valid ship placements
        self.all_valid_boards = self._generate_all_possible_states()
        
        # 2. This list will shrink as the player receives information (Hits/Misses)
        self.current_possible_boards = self.all_valid_boards.copy()

    def _generate_all_possible_states(self):
        # 1. Generates every possible valid configuration of the board
        print("Initializing Game Engine and Calculating State Space")
        
        # Finding every possible single ship placement (Horizontal & Vertical)
        single_ship_positions = []
        
        # Horizontal placements
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE - SHIP_LENGTH + 1):
                # Create a set of coordinates for this ship
                ship_coords = frozenset((r, c + i) for i in range(SHIP_LENGTH))
                single_ship_positions.append(ship_coords)

        # Vertical placements
        for c in range(GRID_SIZE):
            for r in range(GRID_SIZE - SHIP_LENGTH + 1):
                ship_coords = frozenset((r + i, c) for i in range(SHIP_LENGTH))
                single_ship_positions.append(ship_coords)

        # 2. Find all combinations of 3 ships that do not overlap
        valid_states = []
        
        for ships in itertools.combinations(single_ship_positions, NUM_SHIPS):
            # Check for overlap: intersection of sets should be empty
            s1, s2, s3 = ships
            if s1.isdisjoint(s2) and s1.isdisjoint(s3) and s2.isdisjoint(s3):
                # Combine into one master set of occupied coordinates for the board
                full_board = s1 | s2 | s3
                valid_states.append(full_board)
                
        print(f"Game Initialization Completed. Total unique board states: {len(valid_states)}")
        return valid_states

    def update_entropy_state(self, guess_coord, is_hit):
        """
        Filters the state space based on new evidence.
        Equation: S' = { s in S | s is consistent with Observation }
        """
        new_states = []
        for board_set in self.current_possible_boards:
            has_ship = guess_coord in board_set
            
            # If hit, keep boards that HAVE a ship there.
            # If miss, keep boards that do NOT have a ship there.
            if is_hit and has_ship:
                new_states.append(board_set)
            elif not is_hit and not has_ship:
                new_states.append(board_set)
                
        self.current_possible_boards = new_states

    def calculate_entropy(self):
        """
        For calculating Entropy of the current state space.
        Assumption: Uniform distribution (Principle of Independence).
        Formula: H(S) = log2(|S|)
        """
        count = len(self.current_possible_boards)
        if count == 0:
            return 0.0
        return math.log2(count)

    def get_best_move(self, played_moves):
        """
        Determines the move with the highest Expected Information Gain (EIG).
        Strategy: Find the cell where the probability of a hit is closest to 0.5.
        """
        total = len(self.current_possible_boards)
        if total <= 1:
            return None

        best_move = None
        min_diff_from_half = float('inf') # We want to minimize |P(hit) - 0.5|

        # Check every cell in the grid
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if (r, c) in played_moves:
                    continue
                
                # Count how many remaining boards have a ship at (r, c)
                hit_count = sum(1 for board in self.current_possible_boards if (r, c) in board)
                p_hit = hit_count / total
                
                # We maximize information when uncertainty is highest (P near 0.5)
                diff = abs(p_hit - 0.5)
                
                if diff < min_diff_from_half:
                    min_diff_from_half = diff
                    best_move = (r, c)
        
        return best_move
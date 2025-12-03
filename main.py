"""
Entropy-Based Battleship Game
Exam Project for Mathematical Foundations for Data Science
"""

import sys
from entropy import EntropyEngine, GRID_SIZE
from game_engine import BattleshipGame

def print_header():
    print("\n" + "="*50)
    print("      📐 ENTROPY BATTLESHIP 🛳️: 5x5 EDITION 📐")
    print("="*50)
    print("Objective: Sink 3 ships (each Length 3) using Entropy.")
    print("Legend:    [.] Not guessed  [O] Hit  [X] Miss")
    print("-" * 50)

def render_board(game):
    """
    For visualizing the current game state in the CLI.
    """
    print("\n   " + " ".join([str(i) for i in range(GRID_SIZE)]))  # Column headers
    print("  +" + "-" * (GRID_SIZE * 2 - 1) + "+")
    
    for r in range(GRID_SIZE):
        row_str = f"{r} |"
        for c in range(GRID_SIZE):
            if (r, c) in game.played_moves:
                if (r, c) in game.secret_board:
                    row_str += "O "  # HIT
                else:
                    row_str += "X "  # MISS
            else:
                row_str += ". "      # UNKNOWN
        print(row_str + "|")
    
    print("  +" + "-" * (GRID_SIZE * 2 - 1) + "+")

def main():
    # 1. Initialize the Mathematical Engine
    print("Get Ready to Play Battleship!\n")
    ai = EntropyEngine()
    
    # 2. Initialize the Game Board (Secret Code)
    game = BattleshipGame(ai)
    
    print_header()

    choice = input("Would you like strategy tips to win in the least number of turns? (y/n): ")

    # Main Game Loop
    turn_counter = 1
    while not game.is_game_over():
        
        # 3. Render Board & Display Stats
        render_board(game)
        
        current_entropy = ai.calculate_entropy()
        remaining_boards = len(ai.current_possible_boards)
        
        print(f"\n--- Turn {turn_counter} ---")
        print(f"Current Entropy: {current_entropy:.4f} bits")
        print(f"Remaining Possible Configurations: {remaining_boards}")
        
        # 4. Suggest Best Strategy (if opted in)
        if choice.lower() == 'y':
            best_move = ai.get_best_move(game.played_moves)
            if best_move:
                print(f"Strategy Tip 💡 : Guess {best_move} to maximize information gain.")
            else:
                print("No more tips needed! Can you guess where the last battleships are? 🛳️")
        
        # 5. User Input
        try:
            user_input = input("Enter coordinates (row col): ").strip()
            if user_input.lower() == 'exit':
                sys.exit()
                
            parts = user_input.split()
            if len(parts) != 2:
                print("⚠️  Error: Please enter two numbers separated by a space.")
                continue
                
            r, c = int(parts[0]), int(parts[1])
            
            if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
                print(f"⚠️  Error: Coordinates must be between 0 and {GRID_SIZE-1}.")
                continue
                
            # 6. Process Logic ---
            is_hit = game.process_guess(r, c)
            
            # 7. Update Entropy State ---
            ai.update_entropy_state((r, c), is_hit)
            
            # Feedback
            if is_hit:
                print(f"HIT 💥 at ({r}, {c})!")
            else:
                print(f"MISS 🌊 at ({r}, {c}).")
                
            turn_counter += 1

        except ValueError as e:
            print(f"⚠️  {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    # End Game
    render_board(game) # Show final state
    print("\n" + "="*50)
    print(f"🎉 VICTORY! Fleet destroyed in {turn_counter} turns!! 🎉")
    print("="*50)

if __name__ == "__main__":
    main()
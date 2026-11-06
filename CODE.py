
import random
import math
import time
import os

# ==========================================
# SIMULATED ANNEALING - N QUEENS
# Terminal-based animated simulation
# ==========================================

N = 8
TEMP = 20.0
COOLING_RATE = 0.995
MIN_TEMP = 0.01
DELAY = 0.12

# ANSI terminal colours
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def count_conflicts(board):
    conflicts = 0

    for i in range(N):
        for j in range(i + 1, N):
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1

    return conflicts


def attacking_queens(board):
    attacking = set()

    for i in range(N):
        for j in range(i + 1, N):
            if abs(board[i] - board[j]) == abs(i - j):
                attacking.add(i)
                attacking.add(j)

    return attacking


def display_board(board, temperature, iteration, best):
    attacking = attacking_queens(board)
    conflicts = count_conflicts(board)

    clear_screen()

    print(CYAN + BOLD)
    print("=" * 48)
    print("       SIMULATED ANNEALING - N QUEENS")
    print("=" * 48 + RESET)

    print(f"\n{YELLOW}Iteration:{RESET} {iteration}")
    print(f"{YELLOW}Temperature:{RESET} {temperature:.4f}")
    print(f"{YELLOW}Current Conflicts:{RESET} {conflicts}")
    print(f"{YELLOW}Best Conflicts:{RESET} {best}")

    print("\n       CHESSBOARD\n")

    for row in range(N - 1, -1, -1):
        print(f"   {row + 1} ", end="")

        for col in range(N):

            if board[col] == row:

                if conflicts == 0:
                    symbol = GREEN + BOLD + " ♛ " + RESET
                elif col in attacking:
                    symbol = RED + BOLD + " ♛ " + RESET
                else:
                    symbol = GREEN + " ♛ " + RESET

            else:
                if (row + col) % 2 == 0:
                    symbol = " ░ "
                else:
                    symbol = " ▒ "

            print(symbol, end="")

        print()

    print("      " + " ".join(str(i+1) for i in range(N)))

    # Temperature progress bar
    bar_length = 25
    progress = max(0, min(1, temperature / 20))
    filled = int(bar_length * progress)

    print("\n" + MAGENTA + "Cooling: [" +
          "█" * filled +
          "░" * (bar_length - filled) +
          "]" + RESET)

    if conflicts == 0:
        print(GREEN + BOLD)
        print("\n       ★ SOLUTION FOUND! ★")
        print("       ALL QUEENS ARE SAFE!")
        print(RESET)

    elif temperature > 10:
        print(YELLOW + "\n🔥 High temperature: Exploring moves" + RESET)

    elif temperature > 2:
        print(CYAN + "\n❄ Cooling: Improving the solution" + RESET)

    else:
        print(MAGENTA + "\n🎯 Low temperature: Fine tuning" + RESET)


def simulated_annealing():

    global TEMP

    # One queen in each column and row
    board = list(range(N))
    random.shuffle(board)

    best_board = board.copy()
    best_conflicts = count_conflicts(board)

    iteration = 0
    temperature = TEMP

    while True:

        current_conflicts = count_conflicts(board)

        # Stop when solution is found
        if current_conflicts == 0:
            display_board(
                board, temperature, iteration, 0
            )
            break

        # Restart if temperature becomes too low
        if temperature < MIN_TEMP:

            board = list(range(N))
            random.shuffle(board)

            temperature = TEMP
            continue

        # Select two columns and swap their queens
        new_board = board.copy()

        col1, col2 = random.sample(range(N), 2)

        new_board[col1], new_board[col2] = (
            new_board[col2],
            new_board[col1]
        )

        new_conflicts = count_conflicts(new_board)

        delta = new_conflicts - current_conflicts

        # Acceptance probability
        probability = math.exp(
            -delta / temperature
        ) if delta > 0 else 1

        # Accept or reject the new state
        if random.random() < probability:
            board = new_board

        # Update best solution
        current = count_conflicts(board)

        if current < best_conflicts:
            best_conflicts = current
            best_board = board.copy()

        iteration += 1

        # Reduce temperature
        temperature *= COOLING_RATE

        # Display animation
        display_board(
            board,
            temperature,
            iteration,
            best_conflicts
        )

        time.sleep(DELAY)

    print(CYAN + BOLD)
    print("\nFinal Board Configuration:")
    print(best_board)
    print("\nTotal Iterations:", iteration)
    print("Final Conflicts:", count_conflicts(board))
    print(RESET)


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print(CYAN + BOLD)
    print("WELCOME TO N-QUEENS SIMULATION")
    print("=" * 40)
    print(RESET)

    input("Press ENTER to start simulation...")

    simulated_annealing()

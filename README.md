# Battleship with Entropy Calculation
**EGN 5447 - Mathematical Foundations for Data Science - Exam Project**

**Student Name:** Sibi Seenivasan  
**Date:** November 2025

## 📹 Video Deliverables
* **Demonstration Video:**
* **Conceptual Video:**

---

## 📖 Project Overview
This project implements a modified version of the **Battleship** game to demonstrate the concept of **Entropy** in an information-seeking context. 

The game features a CLI (Command Line Interface) that visually updates a $6 \times 6$ grid after every turn. Hits are marked as `O`, Misses as `X`, and unexplored cells as `.`.

### The Game Parameters
* **Grid:** 6x6
* **Ships:** 3 Ships, each of length 3.
* **Objective:** Find all ship coordinates in the fewest turns.

---

## 🧮 Mathematical Foundations

### 1. State Space ($S$)
Because standard Battleship ($10 \times 10$) has too many permutations for real-time calculation, this project uses a $6 \times 6$ grid. This allows us to **exactly enumerate** every valid board configuration at the start of the game using combinatorial logic.

### 2. Entropy Calculation ($H$)
After each guess, the code filters the list of valid boards ($S$) to create a new subset ($S'$) containing only boards consistent with the clues (Hits/Misses).
The entropy is calculated as:

$$H(S') = \log_2(|S'|)$$

*Where $|S'|$ is the count of currently valid board configurations.*

### 3. Best Strategy (Expected Information Gain)
The AI suggests a move based on maximizing **Expected Information Gain (EIG)**.
* For every un-guessed cell $(r, c)$, the system calculates the probability of a Hit ($P_{hit}$) across all valid boards in $S'$.
* The Strategy suggests the cell where $P_{hit} \approx 0.5$.
* **Why?** An outcome with $0.5$ probability has the highest entropy ($1$ bit). Resolving this uncertainty cuts the search space (roughly) in half, which is the mathematically optimal way to reduce uncertainty.

---

## 🚀 How to Run
1. Make sure to have Python 3 installed.
2. Navigate to the project directory.
3. Run the main script:

```bash
python main.py
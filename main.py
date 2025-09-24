# N-Queens Solver with GUI, Animated Backtracking, Genetic Algorithm, and CSP (Step-by-step)
import tkinter as tk
import random
import time

class NQueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Solver")

        self.label = tk.Label(root, text="Enter N (Size of Board):")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.genetic_btn = tk.Button(root, text="Solve with Genetic Algorithm", command=self.solve_genetic)
        self.genetic_btn.pack()

        self.backtracking_btn = tk.Button(root, text="Solve with Backtracking (Animated)", command=self.solve_backtracking_animated)
        self.backtracking_btn.pack()

        self.csp_btn = tk.Button(root, text="Solve with CSP (Animated)", command=self.solve_csp_animated)
        self.csp_btn.pack()

        self.sequence_label = tk.Label(root, text="Solution Sequence:")
        self.sequence_label.pack()

        self.sequence_text = tk.Text(root, height=2, width=50)
        self.sequence_text.pack()

        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()

        self.delay = 200  # milliseconds

    def draw_board(self, positions, highlight=None):
        self.canvas.delete("all")
        N = len(positions)
        cell_size = 500 // N
        for row in range(N):
            for col in range(N):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                fill = "white" if (row + col) % 2 == 0 else "gray"
                if highlight and row == highlight[0] and col == highlight[1]:
                    fill = "yellow"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill)
                if positions[row] == col:
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="red")

        self.sequence_text.delete("1.0", tk.END)
        self.sequence_text.insert(tk.END, f"{positions}")
        self.root.update()
        time.sleep(self.delay / 1000.0)

    def solve_genetic(self):
        N = int(self.entry.get())
        result = genetic_algorithm(N)
        if result:
            self.draw_board(result)
        else:
            self.sequence_text.delete("1.0", tk.END)
            self.sequence_text.insert(tk.END, "No solution found.")

    def solve_backtracking_animated(self):
        N = int(self.entry.get())
        board = [-1] * N
        self.backtracking_helper(board, 0, N)

    def backtracking_helper(self, board, row, N):
        if row == N:
            self.draw_board(board)
            return True
        for col in range(N):
            board[row] = col
            self.draw_board(board, highlight=(row, col))
            if self.is_safe(board, row):
                if self.backtracking_helper(board[:], row + 1, N):
                    return True
            board[row] = -1
        return False

    def is_safe(self, board, row):
        for i in range(row):
            if board[i] == board[row] or abs(board[i] - board[row]) == row - i:
                return False
        return True

    def solve_csp_animated(self):
        N = int(self.entry.get())
        assignment = [-1] * N
        self.csp_backtrack(assignment, 0, N)

    def csp_backtrack(self, assignment, row, N):
        if row == N:
            self.draw_board(assignment)
            return True
        for col in range(N):
            if self.csp_is_valid(assignment, row, col):
                assignment[row] = col
                self.draw_board(assignment, highlight=(row, col))
                if self.csp_backtrack(assignment[:], row + 1, N):
                    return True
                assignment[row] = -1
        return False

    def csp_is_valid(self, assignment, row, col):
        for r in range(row):
            c = assignment[r]
            if c == col or abs(c - col) == row - r:
                return False
        return True

# Genetic Algorithm Implementation (Improved)
def genetic_algorithm(N, population_size=500, mutation_rate=0.1, max_generations=5000):
    def fitness(board):
        non_attacking = 0
        for i in range(N):
            for j in range(i + 1, N):
                if board[i] != board[j] and abs(board[i] - board[j]) != j - i:
                    non_attacking += 1
        return non_attacking

    def mutate(board):
        if random.random() < mutation_rate:
            i, j = random.sample(range(N), 2)
            board[i], board[j] = board[j], board[i]
        return board

    def crossover(parent1, parent2):
        cut = random.randint(0, N - 1)
        child = parent1[:cut] + parent2[cut:]
        # Repair: fix duplicate values
        seen = set()
        for i in range(N):
            if child[i] in seen:
                for val in range(N):
                    if val not in child:
                        child[i] = val
                        break
            seen.add(child[i])
        return child

    population = [random.sample(range(N), N) for _ in range(population_size)]
    max_fitness = (N * (N - 1)) // 2

    for generation in range(max_generations):
        population.sort(key=lambda x: -fitness(x))
        if fitness(population[0]) == max_fitness:
            return population[0]
        new_population = population[:20]
        while len(new_population) < population_size:
            parent1 = random.choice(population[:100])
            parent2 = random.choice(population[:100])
            child = mutate(crossover(parent1, parent2))
            new_population.append(child)
        population = new_population
    return None

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensGUI(root)
    root.mainloop()

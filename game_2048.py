import tkinter as tk
import random
import colorsys

class Game2048(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("2048")
        self.geometry("400x500")
        self.configure(bg='#faf8ef')
        
        # Colors for different numbers
        self.colors = {
            0: ('#cdc1b4', '#776e65'),
            2: ('#eee4da', '#776e65'),
            4: ('#ede0c8', '#776e65'),
            8: ('#f2b179', '#f9f6f2'),
            16: ('#f59563', '#f9f6f2'),
            32: ('#f67c5f', '#f9f6f2'),
            64: ('#f65e3b', '#f9f6f2'),
            128: ('#edcf72', '#f9f6f2'),
            256: ('#edcc61', '#f9f6f2'),
            512: ('#edc850', '#f9f6f2'),
            1024: ('#edc53f', '#f9f6f2'),
            2048: ('#edc22e', '#f9f6f2')
        }
        
        # Score frame
        self.score_frame = tk.Frame(self, bg='#faf8ef')
        self.score_frame.pack(pady=10)
        
        self.score_label = tk.Label(self.score_frame, text="Score:", font=("Arial", 20, "bold"), bg='#faf8ef', fg='#776e65')
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.score = 0
        self.score_value = tk.Label(self.score_frame, text="0", font=("Arial", 20, "bold"), bg='#faf8ef', fg='#776e65')
        self.score_value.pack(side=tk.LEFT)
        
        # Game grid
        self.grid_frame = tk.Frame(self, bg='#bbada0', padx=10, pady=10)
        self.grid_frame.pack()
        
        self.grid_cells = []
        self.matrix = [[0] * 4 for _ in range(4)]
        self.init_grid()
        
        # Bind arrow keys
        self.bind("<Left>", lambda event: self.move("left"))
        self.bind("<Right>", lambda event: self.move("right"))
        self.bind("<Up>", lambda event: self.move("up"))
        self.bind("<Down>", lambda event: self.move("down"))
        
        # Initialize game
        self.add_new_tile()
        self.add_new_tile()
        
    def init_grid(self):
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.grid_frame,
                    bg='#cdc1b4',
                    width=80,
                    height=80
                )
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_frame.grid_propagate(False)
                cell_number = tk.Label(
                    cell_frame,
                    text="",
                    bg='#cdc1b4',
                    font=("Arial", 25, "bold"),
                    justify=tk.CENTER
                )
                cell_number.place(relx=0.5, rely=0.5, anchor="center")
                row.append(cell_number)
            self.grid_cells.append(row)
            
    def update_grid(self):
        for i in range(4):
            for j in range(4):
                value = self.matrix[i][j]
                if value == 0:
                    self.grid_cells[i][j].configure(
                        text="",
                        bg=self.colors[0][0],
                        fg=self.colors[0][1]
                    )
                    self.grid_cells[i][j].master.configure(bg=self.colors[0][0])
                else:
                    color_key = min(value, 2048)
                    self.grid_cells[i][j].configure(
                        text=str(value),
                        bg=self.colors[color_key][0],
                        fg=self.colors[color_key][1]
                    )
                    self.grid_cells[i][j].master.configure(bg=self.colors[color_key][0])
                    
    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.matrix[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.matrix[i][j] = 2 if random.random() < 0.9 else 4
            self.animate_new_tile(i, j)
            
    def animate_new_tile(self, i, j):
        value = self.matrix[i][j]
        cell = self.grid_cells[i][j]
        color_key = min(value, 2048)
        
        def animate(scale=0.1):
            if scale <= 1.0:
                font_size = int(25 * scale)
                cell.configure(
                    text=str(value),
                    font=("Arial", font_size, "bold"),
                    bg=self.colors[color_key][0],
                    fg=self.colors[color_key][1]
                )
                cell.master.configure(bg=self.colors[color_key][0])
                self.after(20, lambda: animate(scale + 0.2))
                
        animate()
        
    def compress(self, matrix):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            pos = 0
            for j in range(4):
                if matrix[i][j] != 0:
                    new_matrix[i][pos] = matrix[i][j]
                    pos += 1
        return new_matrix
    
    def merge(self, matrix):
        score_added = 0
        for i in range(4):
            for j in range(3):
                if matrix[i][j] != 0 and matrix[i][j] == matrix[i][j + 1]:
                    matrix[i][j] *= 2
                    matrix[i][j + 1] = 0
                    score_added += matrix[i][j]
        return matrix, score_added
    
    def reverse(self, matrix):
        return [row[::-1] for row in matrix]
    
    def transpose(self, matrix):
        return [[matrix[j][i] for j in range(4)] for i in range(4)]
    
    def move(self, direction):
        changed = False
        temp_matrix = [row[:] for row in self.matrix]
        
        if direction in ["left", "right"]:
            if direction == "right":
                self.matrix = self.reverse(self.matrix)
            self.matrix = self.compress(self.matrix)
            self.matrix, score_added = self.merge(self.matrix)
            self.score += score_added
            self.matrix = self.compress(self.matrix)
            if direction == "right":
                self.matrix = self.reverse(self.matrix)
                
        else:  # up or down
            self.matrix = self.transpose(self.matrix)
            if direction == "down":
                self.matrix = self.reverse(self.matrix)
            self.matrix = self.compress(self.matrix)
            self.matrix, score_added = self.merge(self.matrix)
            self.score += score_added
            self.matrix = self.compress(self.matrix)
            if direction == "down":
                self.matrix = self.reverse(self.matrix)
            self.matrix = self.transpose(self.matrix)
            
        if self.matrix != temp_matrix:
            self.score_value.configure(text=str(self.score))
            self.add_new_tile()
        self.update_grid()
        
        if not self.moves_available():
            self.game_over()
            
    def moves_available(self):
        # Check for empty cells
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    return True
                    
        # Check for adjacent equal values
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
                    
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
                    
        return False
        
    def game_over(self):
        game_over_frame = tk.Frame(self, bg='#faf8ef')
        game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        game_over_label = tk.Label(
            game_over_frame,
            text="Game Over!",
            font=("Arial", 30, "bold"),
            bg='#faf8ef',
            fg='#776e65'
        )
        game_over_label.pack()
        
        final_score_label = tk.Label(
            game_over_frame,
            text=f"Final Score: {self.score}",
            font=("Arial", 20),
            bg='#faf8ef',
            fg='#776e65'
        )
        final_score_label.pack()
        
        restart_button = tk.Button(
            game_over_frame,
            text="Play Again",
            font=("Arial", 15),
            command=self.restart_game,
            bg='#8f7a66',
            fg='#f9f6f2',
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        restart_button.pack(pady=10)
        
    def restart_game(self):
        self.destroy()
        game = Game2048()
        game.mainloop()

if __name__ == "__main__":
    game = Game2048()
    game.mainloop()

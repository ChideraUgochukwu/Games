import tkinter as tk
from tkinter import messagebox
import random

class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Game settings
        self.GAME_WIDTH = 700
        self.GAME_HEIGHT = 600
        self.SPEED = 100
        self.SPACE_SIZE = 20
        self.BODY_PARTS = 3
        self.SNAKE_COLOR = "#00FF00"
        self.FOOD_COLOR = "#FF0000"
        self.BACKGROUND_COLOR = "#000000"
        
        # Window setup
        self.title("Snake Game")
        self.resizable(False, False)
        
        # Score label
        self.score = 0
        self.score_label = tk.Label(
            self,
            text=f"Score: {self.score}",
            font=('consolas', 20),
            fg='white',
            bg='black'
        )
        self.score_label.pack()
        
        # Game canvas
        self.canvas = tk.Canvas(
            self,
            bg=self.BACKGROUND_COLOR,
            height=self.GAME_HEIGHT,
            width=self.GAME_WIDTH
        )
        self.canvas.pack()
        
        # Center window
        self.center_window()
        
        # Game variables
        self.direction = 'right'
        self.snake_positions = []
        self.food_position = None
        self.food = None
        self.snake = None
        self.game_over = False
        
        # Bind keys
        self.bind('<Left>', lambda event: self.change_direction('left'))
        self.bind('<Right>', lambda event: self.change_direction('right'))
        self.bind('<Up>', lambda event: self.change_direction('up'))
        self.bind('<Down>', lambda event: self.change_direction('down'))
        
        # Start game
        self.start_game()
        
    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width/2) - (self.GAME_WIDTH/2))
        y = int((screen_height/2) - (self.GAME_HEIGHT/2))
        self.geometry(f"{self.GAME_WIDTH}x{self.GAME_HEIGHT+30}+{x}+{y}")
        
    def start_game(self):
        # Create snake
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.direction = 'right'
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.game_over = False
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Create snake body
        self.snake = []
        for x, y in self.snake_positions:
            snake_part = self.canvas.create_rectangle(
                x, y,
                x + self.SPACE_SIZE,
                y + self.SPACE_SIZE,
                fill=self.SNAKE_COLOR,
                tags="snake"
            )
            self.snake.append(snake_part)
            
        # Create food
        self.spawn_food()
        
        # Start game loop
        self.next_turn()
        
    def spawn_food(self):
        if self.food:
            self.canvas.delete(self.food)
            
        x = random.randint(0, (self.GAME_WIDTH - self.SPACE_SIZE) // self.SPACE_SIZE) * self.SPACE_SIZE
        y = random.randint(0, (self.GAME_HEIGHT - self.SPACE_SIZE) // self.SPACE_SIZE) * self.SPACE_SIZE
        
        # Make sure food doesn't spawn on snake
        while (x, y) in self.snake_positions:
            x = random.randint(0, (self.GAME_WIDTH - self.SPACE_SIZE) // self.SPACE_SIZE) * self.SPACE_SIZE
            y = random.randint(0, (self.GAME_HEIGHT - self.SPACE_SIZE) // self.SPACE_SIZE) * self.SPACE_SIZE
            
        self.food_position = (x, y)
        self.food = self.canvas.create_oval(
            x, y,
            x + self.SPACE_SIZE,
            y + self.SPACE_SIZE,
            fill=self.FOOD_COLOR,
            tags="food"
        )
        
    def next_turn(self):
        if not self.game_over:
            # Get current head position
            head_x, head_y = self.snake_positions[0]
            
            # Calculate new head position
            if self.direction == 'left':
                new_head_x = head_x - self.SPACE_SIZE
                new_head_y = head_y
            elif self.direction == 'right':
                new_head_x = head_x + self.SPACE_SIZE
                new_head_y = head_y
            elif self.direction == 'up':
                new_head_x = head_x
                new_head_y = head_y - self.SPACE_SIZE
            else:  # down
                new_head_x = head_x
                new_head_y = head_y + self.SPACE_SIZE
                
            # Check collisions
            if self.check_collisions(new_head_x, new_head_y):
                self.game_over = True
                self.show_game_over()
                return
                
            # Add new head
            new_head_position = (new_head_x, new_head_y)
            self.snake_positions.insert(0, new_head_position)
            
            # Create new head rectangle
            new_head = self.canvas.create_rectangle(
                new_head_x, new_head_y,
                new_head_x + self.SPACE_SIZE,
                new_head_y + self.SPACE_SIZE,
                fill=self.SNAKE_COLOR
            )
            self.snake.insert(0, new_head)
            
            # Check if food eaten
            if new_head_position == self.food_position:
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
                self.spawn_food()
            else:
                # Remove tail
                tail_position = self.snake_positions.pop()
                self.canvas.delete(self.snake.pop())
                
            # Schedule next turn
            self.after(self.SPEED, self.next_turn)
            
    def check_collisions(self, x, y):
        # Wall collisions
        if x < 0 or x >= self.GAME_WIDTH or y < 0 or y >= self.GAME_HEIGHT:
            return True
            
        # Self collision
        if (x, y) in self.snake_positions[1:]:
            return True
            
        return False
        
    def change_direction(self, new_direction):
        if (new_direction == 'left' and self.direction != 'right') or \
           (new_direction == 'right' and self.direction != 'left') or \
           (new_direction == 'up' and self.direction != 'down') or \
           (new_direction == 'down' and self.direction != 'up'):
            self.direction = new_direction
            
    def show_game_over(self):
        answer = messagebox.askquestion(
            "Game Over",
            f"Game Over! Your score was {self.score}.\nWould you like to play again?"
        )
        if answer == 'yes':
            self.start_game()
        else:
            self.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.mainloop()

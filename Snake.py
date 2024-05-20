# -*- coding: utf-8 -*-
"""
Created on Mon May 20 17:34:57 2024

@author: maxwe
"""

import tkinter ## for the graphics (graphical user interface library)
import random ## for the snake food


## constants
## each tile consists of 25px
ROWS = 25 
COLS = 25   
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


#game window
window = tkinter.Tk()
window.title("Snake Game")
window.resizable(False, False) #False for the width & height


canvas = tkinter.Canvas(window, bg = "black", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0) #define the background
canvas.pack()
window.update()


# center the window to user screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")


#init the game
snake = Tile(5*TILE_SIZE,5*TILE_SIZE) # sets the snake's head in a single tile
food = Tile(random.randint(0, COLS - 1) * TILE_SIZE, random.randint(0, ROWS - 1) * TILE_SIZE)
snake_body = [] #consists of tile objects

#change in position over time
velocity_x = 0
velocity_y = 0

game_over = False
score = 0


def reset_game():
    global velocity_x, velocity_y, game_over, score, snake_body, food, snake
    
    #reset all assets 
    velocity_x = 0
    velocity_y = 0
    game_over = False
    score = 0
    snake_body = []
    snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)  # reset snake position
    food = Tile(random.randint(0, COLS - 1) * TILE_SIZE, random.randint(0, ROWS - 1) * TILE_SIZE)  # reset food position
    return


def change_direction(event): #event = key pressed
    print(event.keysym)
    global velocity_x, velocity_y
    
    if(game_over == True and event.keysym == "space"):
        reset_game()
        return
    
    if(game_over == True): #when the game ends, the snake does not respond to key presses
        return
    
    if(event.keysym == "Up" and velocity_y != 1):
        velocity_x = 0
        velocity_y = -1
    elif(event.keysym == "Down" and velocity_y != -1):
        velocity_x = 0
        velocity_y = 1
    elif(event.keysym == "Left" and velocity_x != 1):
        velocity_x = -1
        velocity_y = 0
    elif(event.keysym == "Right" and velocity_x != -1):
        velocity_x = 1
        velocity_y = 0
    
    
def move():
    global snake, game_over, food, snake_body, score
    
    if(game_over == True):
        return
    
    #check boundaries
    if(snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y > WINDOW_HEIGHT): 
        game_over = True
        return
    
    #check colliosion with self
    for tile in snake_body:
        if(snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return
    
    #check collision with food
    if(snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        while(True):
            food.x = random.randint(0, COLS-1) * TILE_SIZE
            food.y = random.randint(0, ROWS-1) * TILE_SIZE
            if(snake.x != food.x and snake.y != food.y):
                break
        score += 1
    
    #update snake body
    for i in range (len(snake_body) - 1, -1, -1):
        tile = snake_body[i]
        if(i == 0): #this is the tile at the start of the snake's body
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
            
    
    snake.x += velocity_x * TILE_SIZE 
    snake.y += velocity_y * TILE_SIZE
    
def draw():
    global snake #references the snake variable outside the function
    global food, snake_body, game_over, score
    
    move()
    
    canvas.delete("all") #clear the previous frame every render
    
    #draw food on canvas
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = "red")
    
    #draw snake on canvas
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "lime green") #top left corner of the tile + bottom right corner
    
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "lime green")
        
    if(game_over == True):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game Over: {score}", fill = "white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 10", text = "\n\n\n\npress space bar to restart", fill = "white")
        
    else:
        canvas.create_text(30, 20, font = "Arial 10", text = f"Score: {score}", fill = "white")
    
    
    window.after(100, draw) #every 100ms, call draw function, basically every 1/10 second we render the snake
    
draw()

window.bind("<KeyRelease>", change_direction)

window.mainloop() #keeps the window on
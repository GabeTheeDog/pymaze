import pygame
import sys
import random
from random import randint
import time

# Define the maze using a 2D grid (each row is a string).
# '#' will represent walls, '.' will represent walkable space.
MAZE = [
    list("############"),
    list("#.@....@...#"),
    list("#.@@@.@@...#"),
    list("#..........#"),
    list("#...@@@.@..#"),
    list("#@@...@....#"),
    list("#....@@@...#"),
    list("#..........#"),
    list("#..+.+.+.+.#"),
    list("#.+.+.+.+..#"),
    list("#..+.+.+.+.#"),
    list("############")
]

TILE_SIZE = 40  # Size of each tile in pixels
ROWS = len(MAZE)
COLS = len(MAZE[0])

COINS = 0
power_up = False

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((COLS * TILE_SIZE, ROWS * TILE_SIZE))
pygame.display.set_caption("Pygame Maze Example")
clock = pygame.time.Clock()

# Player starting position (in MAZE coordinates, not pixels!)
player_x = 1
player_y = 1

def draw_maze():
    """Draw the maze to the screen."""
    for row in range(ROWS):
        for col in range(COLS):
            # If it's a wall (#), draw a black square; otherwise white.
            if MAZE[row][col] == '#':
                color = (0, 0, 0)  # black
            elif MAZE[row][col] == '@':
                color = (139,69,19)  # brown
            elif MAZE[row][col] == '+':
                color = (255, 200, 0) # yellow
            else:
                color = (255, 255, 255)  # white
            pygame.draw.rect(
                screen,
                color,
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )

def draw_player(x, y):
    """Draw the player (red square) at grid position x, y."""
    if power_up == True:
        pygame.draw.rect(
        screen,
        (randint(0,255),randint(0,255) , randint(0,255)),
        (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    )

    else: 
        pygame.draw.rect(
        screen,
        (255,COINS*20 , 0),
        (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    )

def coin_collect(x, y):
    global COINS
    if MAZE[y][x] == '+':
        MAZE[y][x] = '.'
        COINS += 1

def break_wall(x, y):
    global COINS
    global power_up
    
    if COINS == 12:
        power_up = True
    elif COINS == 0:
        power_up = False
    
    if power_up == True and MAZE[y][x] == '@':
        MAZE[y][x] = '.'
        COINS -= 1


def can_move_to(x, y):
    """Check if the player can move to the given grid cell (not a wall)."""
    if 0 <= x < COLS and 0 <= y < ROWS:
        coin_collect(x, y)
        break_wall(x, y)
        return MAZE[y][x] == '.' or MAZE[y][x] == '+'
    return False




# Main game loop
running = True
while running:
    clock.tick(60)  # Limit to 60 frames per second

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Check arrow key presses
            if event.key == pygame.K_LEFT:
                if can_move_to(player_x - 1, player_y):
                    player_x -= 1
            elif event.key == pygame.K_RIGHT:
                if can_move_to(player_x + 1, player_y):
                    player_x += 1
            elif event.key == pygame.K_UP:
                if can_move_to(player_x, player_y - 1):
                    player_y -= 1
            elif event.key == pygame.K_DOWN:
                if can_move_to(player_x, player_y + 1):
                    player_y += 1

    
    # Draw everything
    screen.fill((0, 0, 0))  # Clear screen (black)
    draw_maze()
    draw_player(player_x, player_y)
    pygame.display.flip()

pygame.quit()
sys.exit()

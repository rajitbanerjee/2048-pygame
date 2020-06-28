# 2048-pygame
A pygame implementation of the popular single-player puzzle game, 2048, 
designed by Italian web developer [Gabriele Cirulli](https://github.com/gabrielecirulli).

Inspired by the problem ["2048"](https://open.kattis.com/problems/2048) after solving the basic logic of the puzzle on the [Kattis Problem Archive](https://open.kattis.com/problems/).

## Getting Started
1. Get Python 3.x and clone this repository
2. Get [pip](https://www.makeuseof.com/tag/install-pip-for-python/), then install pygame:\
    ```$ pip install pygame```

3. Run the game:\
    ```$ python main.py```
    
<img src="images/menu.jpg" height=350>      <img src="images/game.jpg" height=350>

## Moves
1. 2048 is played on a gray 4×4 grid, with numbered tiles that slide when a player moves them using the **four arrow keys** or **W A S D**.
2. Press **'n'** to **restart** the game.
3. Join the numbers and get to **2048** to win!

## Game Rules
1. Every turn, a new tile will randomly appear in an empty spot on the board with a value of either 2 or 4.
2. Tiles slide as far as possible in the chosen direction until they are stopped by either another tile or the edge of the grid. 
3. If two tiles of the same number collide while moving, they will merge into a tile with the total value of the two tiles that collided.
4. The resulting tile cannot merge with another tile again in the same move. 
5. If a move causes three consecutive tiles of the same value to slide together, only the two tiles farthest along the direction of motion will combine. 
6. If all four spaces in a row or column are filled with tiles of the same value, a move parallel to that row/column will combine the first two and last two.

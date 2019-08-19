import json
import sys
import time
from copy import deepcopy

import pygame
from pygame.locals import *

from logic import *

#TODO: Add a start screen with difficulty option buttons
#TODO: Add docstrings to functions
#TODO: Add a hovering RULES button on start page
#TODO: Add green colour theme option
difficulty = 2048
col = "green"

def winCheck(status):
    if status != "PLAY":
        size = c["size"]
        # Fill the window with a transparent background
        s = pygame.Surface((size, size), pygame.SRCALPHA)
        s.fill(c["colour"][col]["over"])
        screen.blit(s, (0, 0))

        # Display win/lose status
        screen.blit(my_font.render(
            f"YOU {status}!", 1, (255, 255, 255)), (150, 225))
        pygame.display.update()

        # Wait for 3 seconds before quitting game
        time.sleep(3)
        pygame.quit()
        sys.exit()


def newGame():
    # clear the board to start a new game
    board = [[0] * 4 for _ in range(4)]
    display(board)

    screen.blit(my_font.render(
        f"NEW GAME!", 1, (255, 255, 255)), (130, 225))
    pygame.display.update()
    # wait for 1 second before starting over
    time.sleep(1)

    board = fillTwoOrFour(board, iter=2)
    display(board)
    return board


def display(board):
    screen.fill(tuple(c["colour"][col]["background"]))
    box = c["size"] // 4
    padding = c["padding"]
    for i in range(4):
        for j in range(4):
            colour = tuple(c["colour"][col][str(board[i][j])])
            pygame.draw.rect(screen, colour, (j * box + padding,
                                              i * box + padding,
                                              box - 2 * padding,
                                              box - 2 * padding), 0)
            if board[i][j] != 0:
                if board[i][j] in (2, 4):
                    text_colour = tuple(c["colour"][col]["dark"])
                else:
                    text_colour = tuple(c["colour"][col]["light"])
                # display the number at the centre of the tile
                screen.blit(my_font.render("{:>4}".format(
                    board[i][j]), 1, text_colour),
                    # 2.5 and 7 were obtained by trial and error
                    (j * box + 2.5 * padding, i * box + 7 * padding))
    pygame.display.update()


def main():
    status = "PLAY"
    board = newGame()

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    board = newGame()

                if str(event.key) not in c["keys"]:
                    # no direction key was pressed
                    continue
                else:
                    key = c["keys"][str(event.key)]

                new_board = move(key, deepcopy(board))
                if new_board != board:
                    board = fillTwoOrFour(new_board)
                    display(board)
                    status = checkGameStatus(board, difficulty)
                    winCheck(status)


if __name__ == "__main__":
    # load json data
    c = json.load(open("constants.json", "r"))

    # Set up pygame
    pygame.init()
    screen = pygame.display.set_mode(
        (c["size"], c["size"]))
    pygame.display.set_caption("2048 by Rajit Banerjee")

    icon = pygame.transform.scale(
        pygame.image.load("image/icon.ico"), (32, 32))

    pygame.display.set_icon(icon)
    my_font = pygame.font.SysFont(c["font"], c["font_size"], bold=True)

    # run main game loop
    main()

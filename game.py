import json
import sys
import time
from copy import deepcopy

import pygame
from pygame.locals import *

from logic import *


def winCheck(status):
    if status != "PLAY":
        size = c["dimensions"]["size"]
        # Fill the window with a transparent background
        s = pygame.Surface((size, size), pygame.SRCALPHA)
        s.fill((255, 255, 255, 128))
        screen.blit(s, (0, 0))

        # Display win/lose status
        screen.blit(my_font.render(
            f"YOU {status}!", 1, (255, 255, 255)), (size // 4, size // 2))
        pygame.display.update()

        # Wait for 10 seconds before quitting game
        time.sleep(10)
        pygame.quit()
        sys.exit()


def pr(board):
    print("\n")
    for row in board:
        print(row)


def display(board):
    screen.fill(tuple(c["colour"]["background"]))
    box = c["dimensions"]["size"] // 4
    padding = c["dimensions"]["padding"]
    for i in range(4):
        for j in range(4):
            colour = tuple(c["colour"][str(board[i][j])])
            pygame.draw.rect(screen, colour, (j * box + padding,
                                              i * box + padding,
                                              box - 2 * padding,
                                              box - 2 * padding), 0)
            if board[i][j] != 0:
                if board[i][j] in (2, 4):
                    text_colour = tuple(c["colour"]["dark"])
                else:
                    text_colour = tuple(c["colour"]["light"])
                screen.blit(my_font.render("{:^4}".format(
                    board[i][j]), 1, text_colour),
                    (j * box + 4 * padding, i * box + 5 * padding))
    pygame.display.update()


def main():
    status = "PLAY"
    board = newGame()
    board = fillTwoOrFour(board, iter=2)
    display(board)
    pr(board)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    board = newGame()
                    board = fillTwoOrFour(board, iter=2)
                    display(board)
                    pr(board)

                if str(event.key) not in c["keys"]:
                    # no direction key was pressed
                    continue
                else:
                    desired_key = c["keys"][str(event.key)]

                new_board = move(desired_key, deepcopy(board))
                if new_board != board:
                    board = fillTwoOrFour(new_board)
                    display(board)
                    pr(board)
                    status = checkGameStatus(board)
                    winCheck(status)


if __name__ == "__main__":
    # load json data
    c = json.load(open("constants.json", "r"))
    # Set up pygame
    pygame.init()
    screen = pygame.display.set_mode(
        (c["dimensions"]["size"], c["dimensions"]["size"]))
    pygame.display.set_caption("2048 by Rajit Banerjee")

    icon = pygame.transform.scale(
        pygame.image.load("image/icon.ico"), (32, 32))

    pygame.display.set_icon(icon)
    my_font = pygame.font.SysFont(c["font"], c["font_size"], bold=True)
    # run main game loop
    main()

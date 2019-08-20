import json
import sys
import time
from copy import deepcopy

import pygame
from pygame.locals import *

from logic import *

# TODO: Add difficulty option buttons to start screen
# TODO: Improve start screen interface
# TODO: Add a RULES button on start page

# set up pygame for main gameplay
pygame.init()
c = json.load(open("constants.json", "r"))
screen = pygame.display.set_mode(
    (c["size"], c["size"]))
my_font = pygame.font.SysFont(c["font"], c["font_size"], bold=True)


def winCheck(status, theme):
    """
    Check game status and display win/lose result.

    Parameters:
        status (str): game status
        theme (str): game interface theme
    """
    if status != "PLAY":
        size = c["size"]
        # Fill the window with a transparent background
        s = pygame.Surface((size, size), pygame.SRCALPHA)
        s.fill(c["colour"][theme]["over"])
        screen.blit(s, (0, 0))

        # Display win/lose status
        screen.blit(my_font.render(
            f"YOU {status}!", 1, (255, 255, 255)), (150, 225))
        pygame.display.update()

        # Wait for 1 second before quitting game
        time.sleep(1)
        pygame.quit()
        sys.exit()


def newGame(theme):
    """
    Start a new game by resetting the board.

    Parameters:
        theme (str): game interface theme
    Returns:
        board (list): new game board
    """
    # clear the board to start a new game
    board = [[0] * 4 for _ in range(4)]
    display(board, theme)

    screen.blit(my_font.render(
        f"NEW GAME!", 1, (255, 255, 255)), (130, 225))
    pygame.display.update()
    # wait for 1 second before starting over
    time.sleep(1)

    board = fillTwoOrFour(board, iter=2)
    display(board, theme)
    return board


def display(board, theme):
    """
    Display the board 'matrix' on the game window.

    Parameters:
        board (list): game board
        theme (str): game interface theme
    """
    screen.fill(tuple(c["colour"][theme]["background"]))
    box = c["size"] // 4
    padding = c["padding"]
    for i in range(4):
        for j in range(4):
            colour = tuple(c["colour"][theme][str(board[i][j])])
            pygame.draw.rect(screen, colour, (j * box + padding,
                                              i * box + padding,
                                              box - 2 * padding,
                                              box - 2 * padding), 0)
            if board[i][j] != 0:
                if board[i][j] in (2, 4):
                    text_colour = tuple(c["colour"][theme]["dark"])
                else:
                    text_colour = tuple(c["colour"][theme]["light"])
                # display the number at the centre of the tile
                screen.blit(my_font.render("{:>4}".format(
                    board[i][j]), 1, text_colour),
                    # 2.5 and 7 were obtained by trial and error
                    (j * box + 2.5 * padding, i * box + 7 * padding))
    pygame.display.update()


def playGame(theme, difficulty):
    """
    Main game loop function.

    Parameters:
        theme (str): game interface theme
        difficulty (int): game difficulty, i.e., max. tile to get
    """
    status = "PLAY"
    board = newGame(theme)

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == K_q):
                # exit if q is pressed 
                pygame.quit()
                sys.exit()

            # a key has been pressed
            if event.type == pygame.KEYDOWN:
                # 'n' is pressed to start a new game
                if event.key == pygame.K_n:
                    board = newGame(theme)

                if str(event.key) not in c["keys"]:
                    # no direction key was pressed
                    continue
                else:
                    # convert the pressed key to w/a/s/d
                    key = c["keys"][str(event.key)]

                # obtain new board by performing move on old board's copy
                new_board = move(key, deepcopy(board))

                # proceed if change occurs in the board after making move
                if new_board != board:
                    # fill 2/4 after every move
                    board = fillTwoOrFour(new_board)
                    display(board, theme)
                    # update game status
                    status = checkGameStatus(board, difficulty)
                    # check if the game is over
                    winCheck(status, theme)

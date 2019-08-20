import json
import sys

import pygame
from pygame.locals import *

from game import playGame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Button():
    """
    Class to create a new button in pygame window.
    """
    # initialise the button
    def __init__(self, colour, x, y, width, height, text=""):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    # draw the button on the screen
    def draw(self, win, text_col):
        drawRoundRect(win, self.colour, (self.x, self.y,
                                         self.width, self.height))

        if self.text != "":
            font = pygame.font.SysFont(c["font"], 15, bold=True)
            text = font.render(self.text, 1, text_col)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    # check if the mouse is positioned over the button
    def isOver(self, pos):
        # pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def drawRoundRect(surface, colour, rect, radius=0.4):
    """
    Draw an antialiased rounded filled rectangle on screen

    Parameters:
        surface (pygame.Surface): destination
        colour (tuple): RGB values for rectangle fill colour
        radius (float): 0 <= radius <= 1
    """

    rect = Rect(rect)
    colour = Color(*colour)
    alpha = colour.a
    colour.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, SRCALPHA)

    circle = pygame.Surface([min(rect.size) * 3] * 2, SRCALPHA)
    pygame.draw.ellipse(circle, BLACK, circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(
        circle, [int(min(rect.size)*radius)]*2)

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill(BLACK, rect.inflate(-radius.w, 0))
    rectangle.fill(BLACK, rect.inflate(0, -radius.h))

    rectangle.fill(colour, special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=BLEND_RGBA_MIN)

    surface.blit(rectangle, pos)


def showMenu():
    """
    Display the start screen
    """
    # create light theme button
    light_theme = Button(
        tuple(c["colour"]["light"]["2048"]), 215, 275, 45, 45, "light")
    # create dark theme button
    dark_theme = Button(
        tuple(c["colour"]["dark"]["2048"]), 285, 275, 45, 45, "dark")
    # create play button
    play = Button(tuple(c["colour"]["light"]["2048"]),
                  250, 325, 45, 45, "play")

    # default difficulty
    difficulty = 2048
    # initialise theme
    theme = ""
    theme_selected = False

    # pygame loop for start screen
    while True:
        screen.fill(BLACK)

        screen.blit(pygame.transform.scale(
            pygame.image.load("image/icon2.ico"), (200, 200)), (155, 50))

        font = pygame.font.SysFont(c["font"], 15, bold=True)
        text = font.render("Theme: ", 1, WHITE)
        screen.blit(text, (140, 285))

        light_theme.draw(screen, (197, 255, 215))
        dark_theme.draw(screen, (197, 255, 215))
        play.draw(screen, BLACK)

        pygame.display.update()

        for event in pygame.event.get():
            # store mouse position (coordinates)
            pos = pygame.mouse.get_pos()

            if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == K_q):
                # exit if q is pressed 
                pygame.quit()
                sys.exit()

            # check if a button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # select light theme
                if light_theme.isOver(pos):
                    dark_theme.colour = tuple(c["colour"]["dark"]["2048"])
                    light_theme.colour = tuple(c["colour"]["light"]["64"])
                    theme = "light"
                    theme_selected = True

                # select dark theme
                elif dark_theme.isOver(pos):
                    dark_theme.colour = tuple(c["colour"]["dark"]["1024"])
                    light_theme.colour = tuple(c["colour"]["light"]["2048"])
                    theme = "dark"
                    theme_selected = True

                # play game with selected theme
                if play.isOver(pos):
                    if theme != "":
                        playGame(theme, difficulty)

                # reset theme choice if area outside buttons is clicked
                if not play.isOver(pos) and \
                    not dark_theme.isOver(pos) and \
                        not light_theme.isOver(pos):
                    theme = ""
                    theme_selected = False
                    light_theme.colour = tuple(c["colour"]["light"]["2048"])
                    dark_theme.colour = tuple(c["colour"]["dark"]["2048"])

            # change colour on hovering over buttons
            if event.type == pygame.MOUSEMOTION and not theme_selected:
                if light_theme.isOver(pos):
                    light_theme.colour = tuple(c["colour"]["light"]["64"])
                if not light_theme.isOver(pos):
                    light_theme.colour = tuple(c["colour"]["light"]["2048"])

                if dark_theme.isOver(pos):
                    dark_theme.colour = tuple(c["colour"]["dark"]["1024"])
                if not dark_theme.isOver(pos):
                    dark_theme.colour = tuple(c["colour"]["dark"]["2048"])


if __name__ == "__main__":
    # load json data
    c = json.load(open("constants.json", "r"))

    # set up pygame
    pygame.init()
    # set up screen
    screen = pygame.display.set_mode(
        (c["size"], c["size"]))
    pygame.display.set_caption("2048 by Rajit Banerjee")

    # display game icon in window
    icon = pygame.transform.scale(
        pygame.image.load("image/icon.ico"), (32, 32))
    pygame.display.set_icon(icon)

    # set font according to json data specifications
    my_font = pygame.font.SysFont(c["font"], c["font_size"], bold=True)

    # display the start screen 
    showMenu()

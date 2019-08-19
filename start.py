import json
import sys

import pygame
from pygame import *
from pygame.locals import *

from game import playGame


class Button():
    def __init__(self, colour, x, y, width, height, text=""):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, text_col):
        # draw the button on the screen
        drawRoundRect(win, self.colour, (self.x, self.y,
                                         self.width, self.height))

        if self.text != "":
            font = pygame.font.SysFont(c["font"], 15, bold=True)
            text = font.render(self.text, 1, text_col)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def drawRoundRect(surface, colour, rect, radius=0.4):
    """
    surface : destination
    rect    : rectangle
    colour   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect = Rect(rect)
    colour = Color(*colour)
    alpha = colour.a
    colour.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = Surface(rect.size, SRCALPHA)

    circle = Surface([min(rect.size)*3]*2, SRCALPHA)
    draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = transform.smoothscale(circle, [int(min(rect.size)*radius)]*2)

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

    rectangle.fill(colour, special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle, pos)


def showMenu():

    light_theme = Button(tuple(c["colour"]["light"]["2048"]),
                         190, 275, 45, 45, "light")
    dark_theme = Button(tuple(c["colour"]["dark"]["2048"]),
                        280, 275, 45, 45, "dark")

    difficulty = 2048

    while True:
        screen.fill((0, 0, 0))

        light_theme.draw(screen, (119, 110, 101))
        dark_theme.draw(screen, (197, 255, 215))

        screen.blit(pygame.transform.scale(
            pygame.image.load("image/icon2.ico"), (200, 200)), (155, 50))
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if light_theme.isOver(pos):
                    playGame("light", difficulty)
                elif dark_theme.isOver(pos):
                    playGame("dark", difficulty)


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

    showMenu()

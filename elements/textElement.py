import math

import pygame

import config


class TextElement:
    def __init__(self, name, text, position, bounding_box, duration, font_size, font_type):
        self.name = name
        self.video = None
        self.position = position
        self.text = text
        self.duration = duration
        self.bounding_box = bounding_box
        self.count = 0
        self.font_size = font_size
        self.font_type = font_type

    def render(self, screen):
        length = len(self.text)

        current = math.floor(self.count * length / (self.duration * config.FRAME_RATE))

        my_font = pygame.font.SysFont(self.font_type, self.font_size)
        text_surface = my_font.render(self.text[0:current], False, config.WHITE)
        screen.blit(text_surface, self.position)
        self.count = self.count + 1

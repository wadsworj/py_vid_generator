import math

import pygame

import config


class TextElement:
    def __init__(self, name, text, position, bounding_box, duration, font_size, font_type, text_align, start_time):
        self.name = name
        self.video = None
        self.position = position
        self.text = text
        self.duration = duration
        self.bounding_box = bounding_box
        self.count = 0
        self.font_size = font_size
        self.font_type = font_type
        self.text_align = text_align
        self.start_time = start_time

    def render(self, screen, scene_seconds):
        if self.start_time > scene_seconds:
            return

        length = len(self.text)

        current = math.floor(self.count * length / (self.duration * config.FRAME_RATE))

        my_font = pygame.font.SysFont(self.font_type, self.font_size)
        text_surface = my_font.render(self.text[0:current], True, config.WHITE)
        screen_rect = screen.get_rect()
        if self.text_align == "top_center":
            top_center_rect = pygame.Rect(screen_rect.left, screen_rect.top, screen_rect.width, screen_rect.height / 2)
            text_position = text_surface.get_rect(center = top_center_rect.center)
        elif self.text_align == "center":
            top_center_rect = pygame.Rect(screen_rect.left, screen_rect.top, screen_rect.width, screen_rect.height / 2)
            text_position = text_surface.get_rect(center = screen_rect.center)
        else:
            text_position = self.position

        screen.blit(text_surface, text_position)
        self.count = self.count + 1

import math

import pygame

import config


class TextElement:
    def __init__(self):
        self.name = None
        self.position = None
        self.text = None
        self.duration = None
        self.bounding_box = None
        self.count = 0
        self.font_size = None
        self.font_type = None
        self.text_align = None
        self.start_time = None

    def render(self, screen, scene_seconds):
        if self.start_time > scene_seconds:
            return

        length = len(self.text)

        current = math.floor(self.count * length / (self.duration * config.FRAME_RATE))

        my_font = pygame.font.SysFont(self.font_type, self.font_size)
        text_surface = my_font.render(self.text[0:current], True, config.WHITE)
        text_surface_center = my_font.render(self.text, True, config.WHITE)

        screen_rect = screen.get_rect()
        if self.text_align == "top_center":
            top_center_rect = pygame.Rect(screen_rect.left, screen_rect.top, screen_rect.width, screen_rect.height / 2)
            text_position = text_surface_center.get_rect(center = top_center_rect.center)
        elif self.text_align == "center":
            top_center_rect = pygame.Rect(screen_rect.left, screen_rect.top, screen_rect.width, screen_rect.height / 2)
            text_position = text_surface_center.get_rect(center = screen_rect.center)
        else:
            text_position = self.position

        screen.blit(text_surface, text_position)
        self.count = self.count + 1

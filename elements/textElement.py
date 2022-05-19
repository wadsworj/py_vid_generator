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

        lines = self.text.splitlines()
        line_count = 0

        length = len(self.text)

        if self.duration == 0:
            current = length
        else:
            current = math.floor(self.count * length / (self.duration * config.FRAME_RATE))

        previous_line = 0

        for line in lines:
            current_line_end = 0
            if current - previous_line > 0:
                current_line_end = current - previous_line

            my_font = pygame.font.SysFont(self.font_type, self.font_size)
            text_surface = my_font.render(line[0:current], True, config.WHITE)
            text_surface_center = my_font.render(line, True, config.WHITE)

            screen_rect = screen.get_rect()
            if self.text_align == "top_center":
                top_center_rect = pygame.Rect(screen_rect.left, screen_rect.top, screen_rect.width, screen_rect.height / 2)
                text_position = text_surface_center.get_rect(center = top_center_rect.center)
            elif self.text_align == "center":
                top_center_rect = pygame.Rect(screen_rect.left, screen_rect.top, screen_rect.width, screen_rect.height / 2)
                text_position = text_surface_center.get_rect(center = screen_rect.center)
            else:
                text_position = self.position

            text_surface = my_font.render(line[0:current_line_end], True, config.WHITE)
            screen.blit(text_surface, (text_position.left, (text_position.top + (line_count * self.font_size))))
            line_count = line_count + 1

            previous_line = length = len(line)

        self.count = self.count + 1

import math
from os.path import exists

import pygame

import config


class TextElement:
    def __init__(self):
        self.name = None
        self.position = None
        self.grid_position = None
        self.text = None
        self.duration = None
        self.bounding_box = None
        self.count = 0
        self.font_size = None
        self.font_type = None
        self.font_color = config.WHITE
        self.text_align = None
        self.start_time = None
        self.data = None

    def render(self, screen, scene_seconds, screen_objects):
        if self.start_time and self.start_time > scene_seconds:
            return

        screen_rect = screen.get_rect()

        if not self.position and self.grid_position:
            self.position = [self.grid_position[0] * (screen_rect.width / 16), self.grid_position[1] * (screen_rect.height / 9)]

        lines = self.text.splitlines()
        line_count = 0

        length = len(self.text)

        if self.duration == 0 or not self.duration:
            current = length
        else:
            current = math.floor(self.count * length / (self.duration * config.FRAME_RATE))

        previous_line = 0

        for line in lines:
            current_line_end = 0
            if current - previous_line > 0:
                current_line_end = current - previous_line

            font_exists = exists("fonts/" + self.font_type + ".ttf")

            if font_exists:
                my_font = pygame.font.Font("fonts/" + self.font_type + ".ttf", self.font_size)
            else:
                my_font = pygame.font.SysFont(self.font_type, self.font_size)

            text_surface = my_font.render(line[0:current], True, config.WHITE)
            text_surface_center = my_font.render(line, True, config.WHITE)

            if self.text_align == "top_center":
                top_center_rect = pygame.Rect(screen_rect.left, screen_rect.top, screen_rect.width, screen_rect.height / 2)
                text_position = text_surface_center.get_rect(center = top_center_rect.center)
            elif self.text_align == "top_top_center":
                top_center_rect = pygame.Rect(screen_rect.left, screen_rect.top, screen_rect.width, self.font_size)
                text_position = text_surface_center.get_rect(center=top_center_rect.center)
            elif self.text_align == "center":
                top_center_rect = pygame.Rect(screen_rect.left, screen_rect.top, screen_rect.width, screen_rect.height / 2)
                text_position = text_surface_center.get_rect(center = screen_rect.center)
            else:
                text_position = pygame.Rect(self.position[0], self.position[1], screen_rect.width, screen_rect.height)

            text_surface = my_font.render(line[0:current_line_end], True, self.font_color)
            rect = pygame.Rect(text_position.left, (text_position.top + (line_count * self.font_size)), text_surface.get_width(), text_surface.get_height())
            screen.blit(text_surface, rect)
            screen_objects.append([rect, self.data])

            line_count = line_count + 1

            previous_line = len(line) + previous_line

        self.count = self.count + 1

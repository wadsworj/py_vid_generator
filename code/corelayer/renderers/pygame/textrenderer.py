import math
import os
from os.path import exists
from code.config import config
import pygame

class TextRenderer:
    def __init__(self):
        self.count = 0

    def render(self, element, screen, scene_seconds, screen_objects):
        if element.start_time and element.start_time > scene_seconds:
            return

        screen_rect = screen.get_rect()

        if not element.position and element.grid_position:
            element.position = [element.grid_position[0] * (screen_rect.width / 16),
                             element.grid_position[1] * (screen_rect.height / 9)]

        lines = element.text.splitlines()
        line_count = 0

        length = len(element.text)

        if element.duration == 0 or not element.duration:
            current = length
        else:
            current = math.floor(self.count * length / (element.duration * config.FRAME_RATE))

        previous_line = 0

        for line in lines:
            current_line_end = 0
            if current - previous_line > 0:
                current_line_end = current - previous_line

            font_path = os.path.join(config.RESOURCES_LOCATION, config.RESOURCES_FONTS_LOCATION, element.font_type + ".ttf")
            font_exists = exists(font_path)

            if font_exists:
                my_font = pygame.font.Font(font_path, element.font_size)
            else:
                my_font = pygame.font.SysFont(element.font_type, element.font_size)

            text_surface_center = my_font.render(line, True, config.WHITE)

            if element.text_align == "top_center":
                top_center_rect = pygame.Rect(screen_rect.left, screen_rect.top, screen_rect.width, screen_rect.height / 2)
                text_position = text_surface_center.get_rect(center=top_center_rect.center)
            elif element.text_align == "top_top_center":
                top_center_rect = pygame.Rect(screen_rect.left, screen_rect.top, screen_rect.width, element.font_size)
                text_position = text_surface_center.get_rect(center=top_center_rect.center)
            elif element.text_align == "center":
                top_center_rect = pygame.Rect(screen_rect.left, screen_rect.top, screen_rect.width, screen_rect.height / 2)
                text_position = text_surface_center.get_rect(center=screen_rect.center)
            else:
                text_position = pygame.Rect(element.position[0], element.position[1], screen_rect.width, screen_rect.height)

            text_surface = my_font.render(line[0:current_line_end], True, element.font_color)
            rect = pygame.Rect(text_position.left, (text_position.top + (line_count * element.font_size)),
                               text_surface.get_width(), text_surface.get_height())
            screen.blit(text_surface, rect)
            screen_objects.append([rect, element.data])

            line_count = line_count + 1

            previous_line = len(line) + previous_line

        self.count = self.count + 1

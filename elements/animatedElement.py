import math

import pygame

import config


class AnimatedTextElement:
    def __init__(self):
        self.name = None
        self.text = None
        self.count = 0
        self.font_size = None
        self.font_type = None
        self.font_color = config.WHITE
        self.text_align = None
        self.start_time = None
        self.key_frames = None

    def render(self, screen, scene_seconds):
        print(scene_seconds)

        previous_key_frame = None
        next_key_frame = None

        for key_frame in self.key_frames:
            if not previous_key_frame and key_frame["second"] >= scene_seconds:
                previous_key_frame = key_frame
            if not next_key_frame and key_frame["second"] <= scene_seconds:
                next_key_frame = key_frame

        lines = self.text.splitlines()
        length = len(self.text)

        screen_rect = screen.get_rect()
        position = [key_frame["grid_position"][0] * (screen_rect.width / 16), key_frame["grid_position"][1] * (screen_rect.height / 9)]
        line_count = 0
        for line in lines:
            my_font = pygame.font.SysFont(self.font_type, self.font_size)
            text_surface = my_font.render(line, True, config.WHITE)
            text_surface_center = my_font.render(line, True, config.WHITE)

            text_position = pygame.Rect(position[0], position[1], screen_rect.width, screen_rect.height)

            text_surface = my_font.render(line, True, self.font_color)
            screen.blit(text_surface, (text_position.left, (text_position.top + (line_count * self.font_size))))
            line_count = line_count + 1

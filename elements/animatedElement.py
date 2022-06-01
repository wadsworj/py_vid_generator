import math
from os.path import exists

import pygame

import config
from interpolator import Interpolator


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

    def render(self, screen, scene_seconds, screen_objects):
        key_frames = Interpolator.get_previous_current_frames(self.key_frames, scene_seconds)

        lines = self.text.splitlines()
        length = len(self.text)

        screen_rect = screen.get_rect()
        previous_position_scaled = [key_frames[0]["grid_position"][0] * (screen_rect.width / 16), key_frames[0]["grid_position"][1] * (screen_rect.height / 9)]
        next_position_scaled = [key_frames[1]["grid_position"][0] * (screen_rect.width / 16), key_frames[1]["grid_position"][1] * (screen_rect.height / 9)]

        current_position = Interpolator.interpolate(scene_seconds,
                                            key_frames[0]["second"],
                                            key_frames[1]["second"],
                                            previous_position_scaled,
                                            next_position_scaled)

        if "font_color" in key_frames[1]:
            self.font_color = Interpolator.interpolate(scene_seconds,
                                        key_frames[0]["second"],
                                        key_frames[1]["second"],
                                        key_frames[0]["font_color"],
                                        key_frames[1]["font_color"])

        if "opacity" in key_frames[1]:
            current_opacity = Interpolator.interpolate(scene_seconds,
                                               key_frames[0]["second"],
                                               key_frames[1]["second"],
                                               [key_frames[0]["opacity"]],
                                               [key_frames[1]["opacity"]])[0]
        else:
            current_opacity = 1

        if "font_size" in key_frames[1]:
            self.font_size = Interpolator.interpolate(scene_seconds,
                                               key_frames[0]["second"],
                                               key_frames[1]["second"],
                                               [key_frames[0]["font_size"]],
                                               [key_frames[1]["font_size"]])[0]

        line_count = 0
        for line in lines:
            font_exists = exists("fonts/" + self.font_type + ".ttf")

            if font_exists:
                my_font = pygame.font.Font("fonts/" + self.font_type + ".ttf", int(self.font_size))
            else:
                my_font = pygame.font.SysFont(self.font_type, int(self.font_size))

            text_position = pygame.Rect(current_position[0], current_position[1], screen_rect.width, screen_rect.height)
            text_surface = my_font.render(line, True, self.font_color)
            text_surface.set_alpha(int(255 * current_opacity))
            rect = pygame.Rect(text_position.left, (text_position.top + (line_count * self.font_size)), text_surface.get_width(), text_surface.get_height())
            screen.blit(text_surface, rect)

            screen_objects.append(rect)
            line_count = line_count + 1

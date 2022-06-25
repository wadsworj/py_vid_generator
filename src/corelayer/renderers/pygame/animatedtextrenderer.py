import os
from os.path import exists

import pygame
from src.config import config
from src.corelayer.helpers.interpolator import Interpolator


class AnimatedTextRenderer:
    def __init__(self):
        pass

    def render(self, element, screen, scene_seconds, screen_objects):
        key_frames = Interpolator.get_previous_current_frames(element.key_frames, scene_seconds)

        if not key_frames or len(key_frames) < 2 or not key_frames[0] or not key_frames[1]:
            return

        lines = str(element.text).splitlines()

        screen_rect = screen.get_rect()
        previous_position_scaled = [key_frames[0]["grid_position"][0] * (screen_rect.width / 16),
                                    key_frames[0]["grid_position"][1] * (screen_rect.height / 9)]

        next_position_scaled = [key_frames[1]["grid_position"][0] * (screen_rect.width / 16),
                                key_frames[1]["grid_position"][1] * (screen_rect.height / 9)]

        current_position = Interpolator.interpolate(scene_seconds,
                                                    key_frames[0]["second"],
                                                    key_frames[1]["second"],
                                                    previous_position_scaled,
                                                    next_position_scaled)

        if "font_color" in key_frames[1]:
            element.font_color = Interpolator.interpolate(scene_seconds,
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
            element.font_size = Interpolator.interpolate(scene_seconds,
                                                         key_frames[0]["second"],
                                                         key_frames[1]["second"],
                                                         [key_frames[0]["font_size"]],
                                                         [key_frames[1]["font_size"]])[0]

        font_path = os.path.join(config.RESOURCES_LOCATION, config.RESOURCES_FONTS_LOCATION, element.font_type + ".ttf")
        font_exists = exists(font_path)

        if font_exists:
            my_font = pygame.font.Font(font_path, int(element.font_size))
        else:
            my_font = pygame.font.SysFont(element.font_type, int(element.font_size))

        line_count = 0
        for line in lines:
            text_position = pygame.Rect(current_position[0], current_position[1], screen_rect.width, screen_rect.height)
            text_surface = my_font.render(line, True, element.font_color)
            text_surface.set_alpha(int(255 * current_opacity))
            rect = pygame.Rect(text_position.left, (text_position.top + (line_count * element.font_size)),
                               text_surface.get_width(), text_surface.get_height())
            screen.blit(text_surface, rect)

            screen_objects.append([rect, element.data])
            line_count = line_count + 1

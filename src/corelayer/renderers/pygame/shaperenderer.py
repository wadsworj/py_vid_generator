import os
from os.path import exists

import pygame
from src.config import config
from src.corelayer.helpers.interpolator import Interpolator


class ShapeRenderer:
    def __init__(self):
        pass

    def render(self, element, screen, scene_seconds, screen_objects):
        key_frames = Interpolator.get_previous_current_frames(element.key_frames, scene_seconds)

        screen_rect = screen.get_rect()
        previous_position_scaled = [key_frames[0]["grid_position"][0] * (screen_rect.width / 16),
                                    key_frames[0]["grid_position"][1] * (screen_rect.height / 9)]
        next_position_scaled = [key_frames[1]["grid_position"][0] * (screen_rect.width / 16),
                                key_frames[1]["grid_position"][1] * (screen_rect.height / 9)]

        previous_size_scaled = [key_frames[0]["grid_size"][0] * (screen_rect.width / 16),
                                key_frames[0]["grid_size"][1] * (screen_rect.height / 9)]
        next_size_scaled = [key_frames[1]["grid_size"][0] * (screen_rect.width / 16),
                            key_frames[1]["grid_size"][1] * (screen_rect.height / 9)]

        current_position = Interpolator.interpolate(scene_seconds,
                                                    key_frames[0]["second"],
                                                    key_frames[1]["second"],
                                                    previous_position_scaled,
                                                    next_position_scaled)

        current_size = Interpolator.interpolate(scene_seconds,
                                                key_frames[0]["second"],
                                                key_frames[1]["second"],
                                                previous_size_scaled,
                                                next_size_scaled)

        current_color = Interpolator.interpolate(scene_seconds,
                                                 key_frames[0]["second"],
                                                 key_frames[1]["second"],
                                                 key_frames[0]["color"],
                                                 key_frames[1]["color"])

        if "opacity" in key_frames[1]:
            current_opacity = Interpolator.interpolate(scene_seconds,
                                                       key_frames[0]["second"],
                                                       key_frames[1]["second"],
                                                       [key_frames[0]["opacity"]],
                                                       [key_frames[1]["opacity"]])[0]
        else:
            current_opacity = 1

        s = pygame.Surface((current_size))
        s.set_alpha(int(current_opacity * 255))
        s.fill(current_color)
        screen.blit(s, current_position)

        screen_objects.append([pygame.Rect(current_position, current_size), element.data])

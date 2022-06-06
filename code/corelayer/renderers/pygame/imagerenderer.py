import os
from os.path import exists

import pygame
from code.config import config
from code.corelayer.helpers.interpolator import Interpolator


class ImageRenderer:
    def __init__(self):
        pass

    def render(self, element, screen, scene_seconds, screen_objects):
        if not element.image:
            image_location = os.path.join(config.RESOURCES_LOCATION, "images", element.image_string)
            element.image = pygame.image.load(image_location)

        key_frames = Interpolator.get_previous_current_frames(element.key_frames, scene_seconds)

        screen_rect = screen.get_rect()

        if not element.position and element.grid_position:
            element.position = [element.grid_position[0] * (screen_rect.width / 16), element.grid_position[1] * (screen_rect.height / 9)]

        previous_position_scaled = [key_frames[0]["grid_position"][0] * (screen_rect.width / 16),
                                    key_frames[0]["grid_position"][1] * (screen_rect.height / 9)]
        next_position_scaled = [key_frames[1]["grid_position"][0] * (screen_rect.width / 16),
                                key_frames[1]["grid_position"][1] * (screen_rect.height / 9)]

        current_position = Interpolator.interpolate(scene_seconds,
                                            key_frames[0]["second"],
                                            key_frames[1]["second"],
                                            previous_position_scaled,
                                            next_position_scaled)

        if "opacity" in key_frames[1]:
            current_opacity = Interpolator.interpolate(scene_seconds,
                                               key_frames[0]["second"],
                                               key_frames[1]["second"],
                                               [key_frames[0]["opacity"]],
                                               [key_frames[1]["opacity"]])[0]
        else:
            current_opacity = 1

        element.image.set_alpha(current_opacity * 255)
        rect = pygame.Rect(current_position[0], current_position[1], element.image.get_width(), element.image.get_height())
        screen.blit(element.image, (current_position[0], current_position[1]))

        screen_objects.append([rect, element.data])

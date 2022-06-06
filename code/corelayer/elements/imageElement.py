import os

import pygame
from config import config
from code.corelayer.helpers.interpolator import Interpolator

class ImageElement:
    def __init__(self):
        self.name = None
        self.position = None
        self.grid_position = None
        self.duration = None
        self.count = 0
        self.start_time = None
        self.image_string = None
        self.image = None
        self.data = None

    def render(self, screen, scene_seconds, screen_objects):
        if not self.image:
            image_location = os.path.join(config.RESOURCES_LOCATION, "images", self.image_string)
            self.image = pygame.image.load(image_location)

        key_frames = Interpolator.get_previous_current_frames(self.key_frames, scene_seconds)

        screen_rect = screen.get_rect()

        if not self.position and self.grid_position:
            self.position = [self.grid_position[0] * (screen_rect.width / 16), self.grid_position[1] * (screen_rect.height / 9)]

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

        self.image.set_alpha(current_opacity * 255)
        rect = pygame.Rect(current_position[0], current_position[1], self.image.get_width(), self.image.get_height())
        screen.blit(self.image, (current_position[0], current_position[1]))

        screen_objects.append([rect, self.data])

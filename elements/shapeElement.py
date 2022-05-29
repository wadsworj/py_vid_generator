import math
from os.path import exists

import pygame

import config


class ShapeElement:
    def __init__(self):
        self.name = None
        self.count = 0
        self.key_frames = None

    # https://stackoverflow.com/questions/46732939/how-to-interpolate-2-d-points-between-two-timesteps
    def interpolate(self, t, time_1, time_2, point_1, point_2):
        if t <= time_1:
            return point_1

        if time_1 == time_2:
            return point_1

        dt = (t - time_1) / (time_2 - time_1)
        returned_points = []

        for i in range(len(point_1)):
            interpolated_point = point_2[i] - point_1[i]
            returned_points.append(dt * interpolated_point + point_1[i])

        return returned_points

    def render(self, screen, scene_seconds):
        key_frames = self.get_previous_current_frames(scene_seconds)

        screen_rect = screen.get_rect()
        previous_position_scaled = [key_frames[0]["grid_position"][0] * (screen_rect.width / 16), key_frames[0]["grid_position"][1] * (screen_rect.height / 9)]
        next_position_scaled = [key_frames[1]["grid_position"][0] * (screen_rect.width / 16), key_frames[1]["grid_position"][1] * (screen_rect.height / 9)]

        previous_size_scaled = [key_frames[0]["grid_size"][0] * (screen_rect.width / 16),
                                    key_frames[0]["grid_size"][1] * (screen_rect.height / 9)]
        next_size_scaled = [key_frames[1]["grid_size"][0] * (screen_rect.width / 16),
                                key_frames[1]["grid_size"][1] * (screen_rect.height / 9)]

        current_position = self.interpolate(scene_seconds,
                                            key_frames[0]["second"],
                                            key_frames[1]["second"],
                                            previous_position_scaled,
                                            next_position_scaled)

        current_size = self.interpolate(scene_seconds,
                                            key_frames[0]["second"],
                                            key_frames[1]["second"],
                                            previous_size_scaled,
                                            next_size_scaled)

        current_color = self.interpolate(scene_seconds,
                                        key_frames[0]["second"],
                                        key_frames[1]["second"],
                                        key_frames[0]["color"],
                                        key_frames[1]["color"])

        if "opacity" in key_frames[1]:
            current_opacity = self.interpolate(scene_seconds,
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

    def get_previous_current_frames(self, scene_seconds):
        previous_key_frame = None
        next_key_frame = None
        for key_frame in self.key_frames:
            if scene_seconds >= key_frame["second"] or not previous_key_frame:
                previous_key_frame = key_frame
            elif not next_key_frame and scene_seconds <= key_frame["second"]:
                next_key_frame = key_frame

        # if done next animation then set to previous
        if not next_key_frame:
            next_key_frame = previous_key_frame

        return [previous_key_frame, next_key_frame]
